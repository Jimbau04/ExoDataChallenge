# ExoData Challenge 2026 — Project Brief

## Project Overview

**Name**: ExoData Challenge 2026  
**Event**: Feria de Puebla (Planetario de Puebla)  
**Presentation Date**: 29 de abril de 2026  
**Dataset**: NASA Exoplanet Archive — PSCompPars  
**Total Planets**: 6,147  
**Total Features**: 320  
**Goal**: Unsupervised clustering to discover natural taxonomy of exoplanets

---

## Core Problem Statement

The NASA Exoplanet Archive contains 6,147 confirmed exoplanets with heterogeneous data, multiple missing values, and detection biases. The challenge is to group them meaningfully and translate these clusters into real astrophysical knowledge that goes beyond classical categories.

### Success Criteria
1. **Statistically Valid**: High internal metrics (Silhouette, Davies-Bouldin, Calinski-Harabasz)
2. **Physically Interpretable**: Clusters align with known planet types (Hot Jupiters, super-Earths, etc.)
3. **Scientifically Narrative**: Each cluster tells a coherent astrophysical story

---

## Key Technical Requirements

### Data Dimensions
- **Primary Variables**: pl_rade (radius), pl_bmasse (mass), pl_orbper (period), pl_orbsmax (semi-major axis), pl_eqt (equilibrium temperature), st_teff (stellar temperature), st_met (metallicity), sy_pnum (number of planets), discoverymethod
- **Completeness**: Varies from 45% to 95% depending on variable
- **Missing Data Strategy**: Scientific imputation using physical relationships (Zeng & Sasselov M-R relation), not statistical means

### Derived Features
1. **pl_dens_calc**: Calculated density from mass/radius (g/cm³)
2. **log_period**: Log10 of orbital period to handle skewed distribution
3. **log_rade**: Log10 of planet radius
4. **log_bmasse**: Log10 of planet mass
5. **log_smax**: Log10 of semi-major axis
6. **mass_radius_ratio**: Proxy for composition (high = rocky)
7. **kepler_check**: Validates T² ∝ a³ (Kepler's law consistency)
8. **hz_flag**: Conservative habitable zone flag (0.2 ≤ pl_insol ≤ 1.7)

### Machine Learning Pipeline
1. **Ingestion**: Read PSCompPars CSV (skip comment lines)
2. **EDA**: Distribution analysis, correlation heatmap, missing data patterns
3. **Feature Engineering**: Create 7+ derived features with physical meaning
4. **Scaling**: RobustScaler (handles outliers better than StandardScaler)
5. **Dimensionality Reduction**: PCA (95% variance) + t-SNE/UMAP for visualization
6. **Clustering**: Four algorithms compared (K-Means, DBSCAN, GMM, Hierarchical)
7. **Evaluation**: Multiple metrics (Silhouette, DB Index, Calinski-Harabasz, BIC)
8. **Interpretation**: Map clusters to astrophysical taxonomy

---

## Algorithm Selection Strategy

### Four Algorithms to Implement

1. **K-Means (Baseline)**
   - Test K=3 to 10
   - Elbow method + Silhouette for optimal K
   - Assumes spherical clusters, but interpretable

2. **DBSCAN (Outlier Detection)**
   - Finds "anomalous" planets (direct imaging, circumbinary, free-floating)
   - Noise points (-1) are valuable astrophysical information
   - No need to specify K

3. **Gaussian Mixture Models**
   - Probabilistic clustering
   - Allows elliptical and overlapping clusters
   - Ideal for gradual transitions (sub-Neptune ↔ Neptune)
   - BIC for component selection

4. **Hierarchical Clustering**
   - Dendrogram shows relationships between types
   - Excellent for visual presentation
   - Ward's method minimizes intra-cluster variance

### Evaluation Metrics
- **Silhouette Score**: Cohesion vs separation (higher is better)
- **Davies-Bouldin Index**: Intra-cluster spread / centroid distance (lower is better)
- **Calinski-Harabasz**: Inter / intra variance ratio (higher is better)
- **BIC**: For GMM model selection (lower is better)
- **Detection Method Purity**: Are clusters contaminated by detection bias?

---

## Expected Taxonomy

| Cluster Name | Radius Range (R⊕) | Mass Range (M⊕) | Key Characteristics |
|--------------|-------------------|-----------------|---------------------|
| Terrestrial (Earth-like) | < 1.25 | 0.1 - 10 | High density, moderate temperature |
| Super-Earths | 1.25 - 2.0 | 2 - 15 | Rocky or thin gas envelope |
| Sub-Neptunes | 2.0 - 4.0 | 5 - 50 | Most abundant in Kepler sample |
| Hot Jupiters | > 10 (0.5 R♃) | > 100 | Short periods (<10 days), high temperature |
| Cold Giants | > 10 | 50 - 4000 | Long periods, analogs to Jupiter/Saturn |
| Anomalies | Variable | Variable | Direct imaging, circumbinary, free-floating |

### Key Astrophysical Discovery
**"Neptune Desert"**: Planets with radii 2-4 R⊕ and periods < 3 days are extremely rare. If clustering captures this as a low-density region, it's a significant astrophysical result.

---

## Habitability Analysis

### Conservative Habitable Zone
- **Insolation flux**: 0.2 ≤ pl_insol ≤ 1.7 (Earth flux units)
- **Radius constraint**: pl_rade < 2 R⊕ (potentially rocky)
- **Temperature**: pl_eqt between 200K - 320K (for liquid water with albedo ~0.3)

### Top Candidates
Generate list of best habitable zone candidates with planet name, system, equilibrium temperature, and insolation flux. This is the emotional hook for the jury.

---

## Visualizations (8 required)

1. **Mass-Radius Diagram** (most important): Log-log scatter with theoretical composition lines
2. **t-SNE/UMAP 2D**: Colored by cluster + colored by detection method (bias analysis)
3. **Period-Radius Diagram**: Shows Neptune desert and Fulton gap (~1.8 R⊕)
4. **Extended H-R Diagram**: Stellar effective temperature vs. luminosity/radius, colored by planet type
5. **Correlation Heatmap**: Between all selected features (log-transformed)
6. **Hierarchical Dendrogram**: Truncated tree for visual presentation
7. **Boxplots by Cluster**: Distribution of key variables per cluster
8. **Habitable Zone Map**: Insolation flux vs. radius, marking conservative/optimistic HZ

---

## Scoring Rubric (100 points total)

| Criterion | Points | Strategy |
|-----------|--------|----------|
| Interpretación astrofísica | 30 | **Highest weight** - Deep physical narrative per cluster |
| Clustering correctness | 20 | Multi-algorithm comparison, proper validation |
| Model creativity | 20 | Scientific imputation, engineered features, bias correction |
| CRISP-DM structure | 10 | Clear methodology presentation |
| Communication | 10 | Visual storytelling, publication-level plots |
| Proposal viability | 10 | Realistic limitations and future improvements |

---

## Team Structure & Responsibilities

### Integrante A — Data Lead
- CSV cleaning, header fixing, data types
- EDA: distributions, correlations, outliers
- Feature engineering: logs, density, insolation, Kepler ratio
- Scientific imputation of missing mass/radius
- Normalization and scaling

### Integrante B — ML Lead
- Implement K-Means (K=3-10), DBSCAN, GMM, Hierarchical
- Hyperparameter optimization
- Calculate all evaluation metrics
- PCA + t-SNE/UMAP for visualization
- Final model selection and justification

### Integrante C — Astro Lead
- Map clusters to known astrophysical types
- Analyze detection method biases
- Calculate habitable zone candidates
- Write astrophysical narrative per cluster
- Verify consistency with literature

### Integrante D — Viz & Presentation Lead
- Create all visualizations (mass-radius, H-R, t-SNE, etc.)
- Design presentation slide deck (Keynote/PowerPoint)
- CRISP-DM structure
- Coordinate oral presentation rehearsal

---

## Technology Stack Decision

### Decisión Final: Trabajar con Python con R solo para visualización

**Fecha de Decisión**: 24 de abril de 2026

El equipo ha decidido utilizar **Python como lenguaje principal** para todo el pipeline de machine learning y análisis de datos, reservando **R únicamente para la etapa final de visualización** debido a la superior calidad estética de ggplot2.

**Justificación de la decisión:**

1. **Robustez y pipeline integrado**: Python con scikit-learn garantiza no data leakage y escalado robusto nativo (critical para outliers astronómicos)
2. **Velocidad de ejecución**: UMAP en Python (30s) vs t-SNE (15min) permite iteración rápida
3. **Memoria eficiente**: Operaciones en espacio reducido vs R que requiere matrices de distancia completas
4. **Visualización superior**: ggplot2 produce plots visualmente superiores para presentación final

### **VERDICT DEL PROYECTO: Python (90%) + R solo para visualización final (10%)**

**Stack Técnico Principal (Python):**
```python
# Paquetes fundamentales
pandas>=1.5          # Data manipulation
numpy>=1.23          # Numerical computing
scikit-learn>=1.2    # ML clustering pipeline
umap-learn>=0.5      # Fast dimensionality reduction
matplotlib>=3.6      # Base plotting
seaborn>=0.12        # Statistical visualization
jupyter>=1.0         # Notebooks
```

**Stack para Visualización Final (R):**
```r
# Paquetes solo para plots finales
tidyverse (ggplot2)  # Plots nivel publicación
scales               # Formatos logarítmicos
ggthemes             # Themes profesionales
```

**Workflow Implementado:**
```python
# Fases 1-7 completas en Python:
# 1. Ingesta → pandas read_csv
# 2. Limpieza → pandas operations
# 3. Feature engineering → pandas + numpy
# 4. Scaling → RobustScaler
# 5. Reduction → PCA + UMAP
# 6. Clustering → KMeans, DBSCAN, GMM, Agglomerative
# 7. Evaluation → metrics + interpretation

# Fase 8 (Visualización):
# → Exportar data_processed.csv
# → load in R → ggplot2 plots → save to figures/
```

**Adaptaciones para Stack Híbrido:**

1. **RobustScaler**: Nativo en scipy/sklearn
```python
from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

2. **Pipeline preventa leakage**: Nativo en sklearn
```python
from sklearn.pipeline import Pipeline
pipe = Pipeline([('scaler', RobustScaler()), ('pca', PCA()), ('kmeans', KMeans())])
pipe.fit(X_train)  # Solo ve training data
```

3. **Memory management**: Operaciones en espacio reducido (PCA 95% → 8 dims)

4. **Visualización final**: Usar R/ggplot2 en `viz_final_r/` notebook separado

**Próximos pasos:**
- [ ] Crear requirements.txt con dependencias de Python
- [ ] Implementar utils.py con robust_scaler_astro()
- [ ] Crear notebook 01_ingesta_limpieza.ipynb
- [ ] Crear viz_final_r/08_visualizacion_final.Rmd para plots finales


---

## Timeline & Milestones

### Week 1 (Apr 22-27) — Development
- **Day 1**: Setup GitHub, read CSV, basic cleaning, missing data report
- **Day 2**: Feature engineering (logs, density, hz_flag), M-R imputation
- **Day 3**: Feature scaling, PCA, t-SNE, run all 4 clustering algorithms
- **Day 4**: Select best model, bias analysis by detection method, refine clusters
- **Day 5**: Finalize interpretation, create all visualizations, complete slides 1-10
- **Day 6**: Complete slides 11-16, final rehearsal, GitHub submission

### Week 2 (Apr 28-29) — Presentation
- **Day 7**: Final rehearsals, technical checks
- **Day 8**: **PRESENTATION** (10-15 minutes at Planetario de Puebla)

### Repository Structure
```
exodata-challenge-2026/
├── README.md
├── data/
│   ├── PSCompPars_2026.csv
│   └── processed/
├── notebooks/
│   ├── 01_ingesta_limpieza.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_clustering.ipynb
│   ├── 05_interpretacion.ipynb
│   └── 06_visualizaciones.ipynb
├── src/
│   ├── utils.py
│   └── imputation.py
├── figures/
├── presentation/
│   └── ExoData_Challenge_2026.pptx
└── requirements.txt
```

---

## Critical Success Factors

1. **Don't drop rows prematurely**: Impute scientifically to preserve sample size (maximize from ~55% to ~85% usable data)
2. **Log transforms are essential**: Astronomical data has power-law distributions
3. **Scientific imputation**: Use Zeng & Sasselov (2016) M-R relation for rocky planets
4. **Multi-algorithm**: Don't settle for K-Means, compare all four methods rigorously
5. **Bias analysis**: Explicitly show detection method affects clustering
6. **Habitability hook**: Top 5 habitable zone candidates are emotional high point
7. **Narrative**: Each cluster must have a physical story, not just statistics
8. **Visual quality**: Publication-level plots (think Nature Astronomy style)
9. **Presentation practice**: Rehearse 3+ times to stay within 10-15 minute limit
10. **CRISP-DM structure**: Frame the entire presentation as scientific methodology

---

## Contact & References

- **Dataset**: NASA Exoplanet Archive — PSCompPars (downloaded 22-Apr-2026)
- **Methodology**: CRISP-DM
- **Key Papers**: Zeng & Sasselov (2016) for M-R relation, Fulton et al. (2017) for radius gap
- **Competition**: Feria de Puebla 2026 — ExoData Challenge

---
**Estado del proyecto**: En fase de planificación y desarrollo  
**Última actualización**: 24 de abril de 2026
