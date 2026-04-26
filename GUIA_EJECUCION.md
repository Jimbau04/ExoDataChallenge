# ExoData Challenge 2026 — Guía de Ejecución y Revisión

> **Deadline:** 27-abr-2026 | **Presentación:** 29-abr-2026 (Planetario de Puebla)  
> **Duración estimada de ejecución completa:** ~20 minutos

---

## Paso 0: Clonar y preparar entorno (5 min)

```bash
git clone <url-del-repo> ExoDataChallenge
cd ExoDataChallenge
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

**Verificar:**
```bash
python3 -c "import pandas, numpy, sklearn, umap; print('OK')"
# Debe imprimir: OK
```

---

## Paso 1: Auditoría de datos — Fase 1 (2 min)

```bash
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 01_ingesta_limpieza.ipynb
```

O ábrelo en Jupyter y ejecuta todas las celdas (Run All).

**Qué revisar:**
- [ ] El notebook corre de arriba a abajo sin errores
- [ ] Shape confirmado: 6,160 planetas × 320 columnas
- [ ] `pl_insol` aparece en el reporte de variables críticas (69.9% completitud)
- [ ] Reportes generados en `docs/critical_vars_completitud.csv`, `top20_completitud.csv`, `detection_method_distribution.csv`
- [ ] Sesgo de detección documentado: 73.4% Tránsito

---

## Paso 2: Feature Engineering — Fase 2 (3 min)

```bash
cd notebooks
jupyter nbconvert --to notebook --execute --inplace 02_feature_engineering.ipynb
```

**Qué revisar:**
- [ ] Imputación científica ejecutada (NO medias estadísticas)
  - 24 masas imputadas desde radio (relación M-R)
  - 43 radios imputados desde masa
  - 1,321 insolaciones estimadas
  - 1,098 temperaturas de equilibrio estimadas
- [ ] 6 features derivados: `log_rade`, `log_dens`, `log_period`, `log_eqt`, `st_met`, `sy_pnum`
- [ ] 5,610 planetas con features completos (88.8%)
- [ ] 34 candidatos a zona habitable (criterio conservador)
- [ ] Archivos generados: `data/processed/df_clean_features.csv`, `data/processed/X_features.csv`

---

## Paso 3: Clustering — Fases 3-6 (5 min)

Si ejecutaste el notebook de la Fase 2, los datos ya están procesados. Ahora corre el clustering:

```bash
# Desde la raíz del proyecto
source .venv/bin/activate
python3 -c "
import pandas as pd, numpy as np, sys
sys.path.insert(0, 'src')
from sklearn.preprocessing import RobustScaler
from sklearn.mixture import GaussianMixture

# Cargar features
X = pd.read_csv('data/processed/X_features.csv')
X_scaled = RobustScaler().fit_transform(X)

# GMM n=6 (modelo seleccionado)
gmm = GaussianMixture(n_components=6, random_state=42, n_init=5, covariance_type='full')
labels = gmm.fit_predict(X_scaled)

# Guardar labels
pd.DataFrame({'cluster': labels}).to_csv('data/processed/cluster_labels.csv', index=False)
print(f'Clustering completado: {len(set(labels))} clusters')
for c in sorted(set(labels)):
    n = (labels == c).sum()
    print(f'  Cluster {c}: {n} planetas ({n/len(labels)*100:.1f}%)')
"
```

**Qué revisar:**
- [ ] 6 clusters con distribución balanceada (~200 a ~2,500 planetas cada uno)
- [ ] Los nombres de los clusters están en `docs/cluster_taxonomy.csv`

---

## Paso 4: Visualizaciones — Fase 7 (3 min)

### 4a. Generar coordenadas UMAP y exportar datos para R

```bash
source .venv/bin/activate
python3 << 'PYEOF'
import pandas as pd, numpy as np, sys
sys.path.insert(0, 'src')
from features import engineer_all_features, CLUSTERING_FEATURES
from imputation import run_scientific_imputation
from sklearn.preprocessing import RobustScaler
from sklearn.mixture import GaussianMixture
import umap

df = pd.read_csv('data/PSCompPars_2026.csv', comment='#', low_memory=False)
df = run_scientific_imputation(df)
df = engineer_all_features(df)
mask = df[CLUSTERING_FEATURES].notna().all(axis=1)

X = df[mask][CLUSTERING_FEATURES].copy()
X_scaled = RobustScaler().fit_transform(X)

# Cluster
gmm = GaussianMixture(n_components=6, random_state=42, n_init=5, covariance_type='full')
df.loc[mask, 'cluster'] = gmm.fit_predict(X_scaled)

# UMAP
reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=30, min_dist=0.1)
coords = reducer.fit_transform(X_scaled)
df.loc[mask, 'umap_x'] = coords[:, 0]
df.loc[mask, 'umap_y'] = coords[:, 1]

# Nombres de clusters
names = {0:'Sub-Neptunes',1:'Super-Earths (multi)',2:'Cold/Warm Jupiters',
         3:'Mini-Neptunes',4:'Puffy Neptunes',5:'Earth-sized Rocky'}
df['cluster_name'] = df['cluster'].map(names)

# Agrupar métodos de detección
top_methods = ['Transit','Radial Velocity','Microlensing','Imaging','Transit Timing Variations']
df['method_group'] = df['discoverymethod'].apply(lambda x: x if x in top_methods else 'Other')

# Exportar
cols = ['pl_name','hostname','discoverymethod','disc_year',
        'pl_rade','pl_bmasse','pl_orbper','pl_orbsmax','pl_eqt','pl_insol',
        'st_teff','st_met','st_rad','sy_pnum',
        'pl_dens_calc','mass_radius_ratio','hz_flag',
        'log_rade','log_dens','log_period','log_smax','log_eqt',
        'cluster','cluster_name','umap_x','umap_y','method_group']
df[[c for c in cols if c in df.columns]].to_csv('viz_final_r/exoplanets_labeled.csv', index=False)
print('✓ Datos exportados para R')
PYEOF
```

### 4b. Generar gráficas en R

```bash
cd viz_final_r
Rscript 07_visualizaciones_finales.R
cd ..
```

### 4c. Generar dendrograma en Python

```bash
source .venv/bin/activate
python3 << 'PYEOF'
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import RobustScaler

X = pd.read_csv('data/processed/X_features.csv')
X_scaled = RobustScaler().fit_transform(X)
idx = np.random.RandomState(42).choice(len(X_scaled), 500, replace=False)
Z = linkage(X_scaled[idx], method='ward')

fig, ax = plt.subplots(figsize=(14, 6))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90, leaf_font_size=9,
           color_threshold=0.5 * max(Z[:, 2]), ax=ax)
ax.set_title('Hierarchical Clustering Dendrogram (Ward, n=500)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/08_dendrogram.png', dpi=300, bbox_inches='tight')
print('✓ Dendrograma generado')
PYEOF
```

**Verificar:**
- [ ] 10 archivos PNG en `figures/`
- [ ] Todas las gráficas se ven bien (abrir una por una)

---

## Paso 5: Revisión final del proyecto (5 min)

### Checklist de archivos

```bash
# Desde la raíz del proyecto, verifica que existan:
ls data/PSCompPars_2026.csv                    # Dataset original
ls data/processed/X_features.csv               # Matriz de features (5,610 × 6)
ls data/processed/df_labeled.csv               # Dataset con labels de cluster
ls docs/critical_vars_completitud.csv           # Reporte de completitud
ls docs/cluster_taxonomy.csv                    # Tabla de taxonomía
ls figures/*.png                                # 10 visualizaciones
ls notebooks/01_ingesta_limpieza.ipynb          # Notebook Fase 1
ls notebooks/02_feature_engineering.ipynb       # Notebook Fase 2
ls src/features.py                              # Módulo de features
ls src/imputation.py                            # Módulo de imputación
ls src/clustering.py                            # Módulo de clustering
ls viz_final_r/07_visualizaciones_finales.R     # Script de visualización R
```

### Checklist de calidad

- [ ] El notebook de Fase 2 corre de principio a fin sin errores
- [ ] La imputación es científica (NO `fillna(mean())`) — check flags `_imputed`
- [ ] Los 6 clusters tienen interpretación astrofísica (revisar `docs/cluster_taxonomy.csv`)
- [ ] El sesgo de detección está documentado (73.4% Tránsito)
- [ ] La zona habitable tiene 34 candidatos con criterios claros
- [ ] Las gráficas usan colores consistentes por cluster
- [ ] `.venv/` y `data/processed/` NO están en git (revisar `.gitignore`)

---

## Paso 6: Commit y push

```bash
git add -A
git status  # Revisar qué se va a commitear
git commit -m "feat: Complete pipeline — clustering + visualizations

- GMM n=6 clustering (silhouette ~0.12 on balanced log features)
- 6 astrophysical clusters identified and named
- 10 publication-quality figures (R/ggplot2 + Python)
- Scientific imputation (M-R relation, not statistical means)
- 34 habitable zone candidates identified
- CRISP-DM methodology documented throughout"
git push origin main
```

---

## Paso 7: Preparar presentación (trabajo en equipo)

### Estructura sugerida (12-16 slides, 10-15 min)

| Slide | Tema | Quién |
|-------|------|-------|
| 1 | Portada + equipo | Viz Lead |
| 2 | Problema y objetivo (CRISP-DM) | Cualquiera |
| 3 | Dataset: NASA Exoplanet Archive, 6,160 planetas, 320 variables | Data Lead |
| 4 | Auditoría: completitud, sesgo de detección (73% tránsito) | Data Lead |
| 5 | Feature Engineering: logs, densidad, imputación científica | Data Lead |
| 6 | Metodología: 4 algoritmos comparados (K-Means, DBSCAN, GMM, Jerárquico) | ML Lead |
| 7 | Modelo seleccionado: GMM n=6 (justificación con BIC) | ML Lead |
| 8 | **MASS-RADIUS DIAGRAM** (la gráfica más importante) | Astro Lead |
| 9 | Taxonomía de clusters (tabla con 6 tipos) | Astro Lead |
| 10 | **PERIOD-RADIUS + Neptune Desert** (hallazgo astrofísico) | Astro Lead |
| 11 | Sesgo de detección por cluster | Astro Lead |
| 12 | Zona Habitable — 34 candidatos | Astro Lead |
| 13 | UMAP projections (clusters + detección) | ML Lead |
| 14 | Limitaciones (silhouette modesto, artefactos de imputación) | ML Lead |
| 15 | Conclusiones | Cualquiera |
| 16 | Referencias | Astro Lead |

### Puntos clave para la presentación

1. **CRISP-DM va primero.** Muestra el ciclo: Business Understanding → Data Understanding → Data Prep → Modeling → Evaluation → Deployment
2. **La imputación científica es diferenciador.** Enfatizar que usamos relaciones M-R de Zeng & Sasselov, NO medias
3. **El Neptune Desert es el hallazgo estrella.** Si el clustering captura esa zona vacía, es resultado astrofísico real
4. **Sesgo de detección.** 73% tránsito → los clusters están inevitablemente sesgados. Reconocerlo suma puntos
5. **Densidad ≈ composición.** Cluster 5 (Earth-sized) tiene ρ = 5.49 g/cm³ — idéntica a la Tierra. Cluster 4 tiene ρ = 1.60 — atmósfera gruesa
6. **34 candidatos habitables.** Es el gancho emocional. Mostrar la tabla con nombres

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: pandas` | Activar el venv: `source .venv/bin/activate` |
| R no encuentra ggplot2 | `Rscript -e 'install.packages(c("ggplot2","dplyr","tidyr","scales","scattermore"), repos="https://cran.r-project.org")'` |
| UMAP tarda mucho | Normal, ~30 segundos para 5,610 muestras. No cancelar |
| `data/processed/` no existe | Se crea automáticamente al ejecutar los scripts |
| Error de permisos en git push | Revisar credenciales de GitHub. Si falla, compartir el repo por zip |
