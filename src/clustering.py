"""
clustering.py — Clustering pipeline for exoplanet taxonomy.

Implements and compares four algorithms:
  - K-Means (baseline, K=3..10)
  - DBSCAN (outlier/anomaly detection)
  - Gaussian Mixture Models (probabilistic, overlapping clusters)
  - Hierarchical / Agglomerative (dendrogram-friendly)

All wrapped with RobustScaler + PCA for a clean pipeline.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import warnings
warnings.filterwarnings("ignore")


def scale_and_reduce(X, n_components=5, random_state=42):
    """
    RobustScaler → PCA with explicit n_components.

    We force n_components even when PC1 dominates, because the subtle
    dimensions (PC2-PC5) encode the cluster-defining differences between
    planets of similar size.

    Returns:
        X_scaled: scaled features (for DBSCAN on full dimensionality)
        X_pca: PCA-reduced features (for K-Means, GMM, Hierarchical)
        pca: fitted PCA object
        scaler: fitted RobustScaler
    """
    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(X)

    max_comp = min(n_components, X.shape[1])
    pca = PCA(n_components=max_comp, random_state=random_state)
    X_pca = pca.fit_transform(X_scaled)

    print(f"PCA: {X.shape[1]} features → {X_pca.shape[1]} components")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"  PC{i+1}: {ratio*100:.1f}%")
    print(f"  Cumulative: {pca.explained_variance_ratio_.sum()*100:.1f}%")

    return X_scaled, X_pca, pca, scaler


def run_kmeans(X, k_range=range(3, 11), random_state=42):
    """
    K-Means for K in k_range. Returns inertia, silhouette, labels for best K.
    """
    results = {"k": [], "inertia": [], "silhouette": [], "davies_bouldin": [], "calinski_harabasz": []}
    models = {}

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        labels = km.fit_predict(X)
        models[k] = (km, labels)

        results["k"].append(k)
        results["inertia"].append(km.inertia_)
        results["silhouette"].append(silhouette_score(X, labels))
        results["davies_bouldin"].append(davies_bouldin_score(X, labels))
        results["calinski_harabasz"].append(calinski_harabasz_score(X, labels))
        print(f"  K={k}: inertia={km.inertia_:.1f}, silhouette={results['silhouette'][-1]:.4f}, DB={results['davies_bouldin'][-1]:.4f}")

    # Best by silhouette
    best_k_idx = np.argmax(results["silhouette"])
    best_k = results["k"][best_k_idx]
    print(f"\n  Best K={best_k} (silhouette={results['silhouette'][best_k_idx]:.4f})")

    return pd.DataFrame(results), models[best_k][0], models[best_k][1]


def run_dbscan(X, eps_values=None, min_samples_values=None):
    """
    DBSCAN with grid search over eps and min_samples.
    High silhouette isn't always the goal — we want meaningful noise points.
    """
    if eps_values is None:
        eps_values = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
    if min_samples_values is None:
        min_samples_values = [3, 5, 10, 15]

    best_score = -1
    best_model = None
    best_labels = None
    best_params = {}

    results = []
    for eps in eps_values:
        for ms in min_samples_values:
            db = DBSCAN(eps=eps, min_samples=ms)
            labels = db.fit_predict(X)

            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = (labels == -1).sum()

            # Only score if we have at least 2 clusters
            if n_clusters >= 2:
                mask = labels != -1
                if mask.sum() > n_clusters:
                    sil = silhouette_score(X[mask], labels[mask])
                    db_score = davies_bouldin_score(X[mask], labels[mask])
                else:
                    sil = -1
                    db_score = 999
            else:
                sil = -1
                db_score = 999

            results.append({
                "eps": eps, "min_samples": ms,
                "n_clusters": n_clusters, "n_noise": n_noise,
                "silhouette": sil, "davies_bouldin": db_score
            })

            print(f"  eps={eps}, min_samples={ms}: {n_clusters} clusters, {n_noise} noise, sil={sil:.4f}")

            # Prefer meaningful clusters over pure silhouette
            if sil > best_score and n_clusters >= 3:
                best_score = sil
                best_model = db
                best_labels = labels
                best_params = {"eps": eps, "min_samples": ms}

    if best_model is None:
        # Fallback: default DBSCAN
        best_model = DBSCAN(eps=0.5, min_samples=5)
        best_labels = best_model.fit_predict(X)
        best_params = {"eps": 0.5, "min_samples": 5}
        print("  ⚠️ No good DBSCAN config found — using defaults")

    print(f"\n  Best: eps={best_params['eps']}, min_samples={best_params['min_samples']}")
    return pd.DataFrame(results), best_model, best_labels


def run_gmm(X, n_range=range(2, 11), random_state=42):
    """
    Gaussian Mixture Models with BIC/AIC for component selection.
    GMM allows elliptical, overlapping clusters — more realistic for planets.
    """
    results = {"n": [], "bic": [], "aic": [], "silhouette": [], "davies_bouldin": []}
    models = {}

    for n in n_range:
        gmm = GaussianMixture(n_components=n, random_state=random_state, n_init=5)
        labels = gmm.fit_predict(X)
        models[n] = (gmm, labels)

        results["n"].append(n)
        results["bic"].append(gmm.bic(X))
        results["aic"].append(gmm.aic(X))
        sil = silhouette_score(X, labels)
        results["silhouette"].append(sil)
        results["davies_bouldin"].append(davies_bouldin_score(X, labels))
        print(f"  n={n}: BIC={gmm.bic(X):.1f}, AIC={gmm.aic(X):.1f}, silhouette={sil:.4f}")

    # Best by BIC (lower is better — balances fit vs. complexity)
    best_n_idx = np.argmin(results["bic"])
    best_n = results["n"][best_n_idx]
    print(f"\n  Best n={best_n} (BIC={results['bic'][best_n_idx]:.1f})")

    return pd.DataFrame(results), models[best_n][0], models[best_n][1]


def run_hierarchical(X, n_range=range(2, 11)):
    """
    Agglomerative clustering with Ward's method (minimizes intra-cluster variance).
    Produces a dendrogram-friendly structure.
    """
    results = {"n": [], "silhouette": [], "davies_bouldin": [], "calinski_harabasz": []}
    models = {}

    for n in n_range:
        agg = AgglomerativeClustering(n_clusters=n, linkage="ward")
        labels = agg.fit_predict(X)
        models[n] = (agg, labels)

        results["n"].append(n)
        sil = silhouette_score(X, labels)
        results["silhouette"].append(sil)
        results["davies_bouldin"].append(davies_bouldin_score(X, labels))
        results["calinski_harabasz"].append(calinski_harabasz_score(X, labels))
        print(f"  n={n}: silhouette={sil:.4f}")

    best_n_idx = np.argmax(results["silhouette"])
    best_n = results["n"][best_n_idx]
    print(f"\n  Best n={best_n} (silhouette={results['silhouette'][best_n_idx]:.4f})")

    return pd.DataFrame(results), models[best_n][0], models[best_n][1]


def run_all_clustering(X_pca, X_scaled, random_state=42):
    """
    Run all four algorithms and return comparison results.
    """
    print("=" * 60)
    print("1. K-MEANS (on PCA-reduced data)")
    print("=" * 60)
    km_results, km_model, km_labels = run_kmeans(X_pca)

    print("\n" + "=" * 60)
    print("2. DBSCAN (on scaled data — needs full dimensionality for density)")
    print("=" * 60)
    db_results, db_model, db_labels = run_dbscan(X_scaled)

    print("\n" + "=" * 60)
    print("3. GAUSSIAN MIXTURE MODELS (on PCA-reduced data)")
    print("=" * 60)
    gmm_results, gmm_model, gmm_labels = run_gmm(X_pca)

    print("\n" + "=" * 60)
    print("4. HIERARCHICAL / AGGLOMERATIVE (on PCA-reduced data)")
    print("=" * 60)
    hc_results, hc_model, hc_labels = run_hierarchical(X_pca)

    return {
        "kmeans": (km_results, km_model, km_labels),
        "dbscan": (db_results, db_model, db_labels),
        "gmm": (gmm_results, gmm_model, gmm_labels),
        "hierarchical": (hc_results, hc_model, hc_labels),
    }
