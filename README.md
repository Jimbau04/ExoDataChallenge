# ExoData Challenge 2026 — Análisis de Exoplanetas

## Descripción del Proyecto

**Objetivo:** Descubrir la taxonomía natural de 6,147 exoplanetas confirmados mediante clustering no supervisado con análisis astrofísico profundo.

**Evento:** Feria de Puebla 2026 — Planetario de Puebla  
**Fecha de presentación:** 29 de abril de 2026  
**Entrega de resultados:** 27 de abril de 2026

## Stack Técnico

**Lenguaje Principal:** Python (versión 3.10+)

### Paquetes de Python Requeridos:
```bash
pip install:
  - pandas>=1.5        # Data manipulation
  - numpy>=1.23        # Numerical computing
  - scikit-learn>=1.2  # ML clustering pipeline
  - umap-learn>=0.5    # Fast dimensionality reduction
  - matplotlib>=3.6    # Base plotting
  - seaborn>=0.12      # Statistical visualization
  - jupyter>=1.0       # Notebooks
  - plotly>=5.10       # Interactive (optional)
```

### Visualización Final (R) - SOLO para plots de alta calidad:
**R versión 4.3+:** para visualización final con ggplot2
```r
# Paquetes R solo para visualización:
- tidyverse  (ggplot2, dplyr, scales)  # Plots nivel publicación
- ggthemes   # Themes profesionales
- gridExtra  # Multi-paneles
- patchwork  # Compose plots
```

**Rationale**: Python provides robust ML pipeline + data integrity; R/ggplot2 provides superior aesthetic quality for final publication plots.

**Workflow**: Python notebooks → export processed data → Load in R → Generate final plots → Embed in presentation
```r
tidyverse        # dplyr, ggplot2, tidyr, purrr
cluster          # kmeans, diana, pam
factoextra       # Visualización clustering
dbscan           # DBSCAN para outliers
mclust           # Gaussian Mixture Models
umap             # Reducción dimensional
Rtsne            # t-SNE
scales           # Formato de ejes logarítmicos
ggthemes         # Themes profesionales
renv             # Reproducibilidad
```

## Estructura del Repositorio

```
├── data/
│   ├── PSCompPars_2026.csv           # Dataset completo (45MB)
│   ├── processed/                      # Datos procesados
│   └── imputations/                    # Relaciones de imputación
├── notebooks/
│   ├── 01_ingesta_limpieza.ipynb       # Ingesta y limpieza
│   ├── 02_analisis_exploratorio.ipynb  # EDA
│   ├── 03_ingenieria_features.ipynb    # Features derivados
│   ├── 04_clustering_comparativo.ipynb # Los 4 algoritmos
│   ├── 05_evaluacion_metricas.ipynb    # Silhouette, DB, CH
│   ├── 06_interpretacion.ipynb         # Taxonomía astrofísica
│   └── 07_visualizacion_python.ipynb   # Plots base Python
├── src/
│   ├── utils.py                       # Funciones auxiliares
│   └── imputacion_fisica.py           # Imputación Zeng & Sasselov
├── viz_final_r/
│   └── 08_visualizacion_final.Rmd     # ggplot2 final plots
├── figures/
│   ├── diagrama_masa_radio.png       # Output clave
│   ├── tsne_clusters.png
│   ├── dendrograma_jerarquico.png
│   └── candidatos_habitable.png
├── presentation/
│   └── ExoData_Challenge_2026.pptx    # Presentación
└── requirements.txt                   # Paquetes Python
```

## Instrucciones de Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-repo/exodata-challenge-2026
cd exodata-challenge-2026

# 2. Instalar Python
python3 -m pip install -r requirements.txt

# 3. Instalar R (SOLO para visualización final)
## Opción A: Con conda/brew
conda install -c conda-forge r-base r-tidyverse
## Opción B: Descargar de r-project.org

# 4. Abrir proyecto
## Para ML + data (Python):
jupyter notebook notebooks/  

## Para visualización final (R):
Rstudio viz_final_r/08_visualizacion_final.Rmd
```

## Pipeline de Análisis (8 Pasos CRISP-DM)

**Fases 1-7 (Python):**
1. **Ingesta**: pandas lee PSCompPars, manejo de comentarios
2. **Limpieza**: Identificar valores nulos, tipos de datos
3. **Feature Engineering**: Crear 7+ variables derivadas
4. **Escalado**: RobustScaler (median + IQR)
5. **Reducción Dimensional**: PCA (95%) + t-SNE + UMAP
6. **Clustering**: K-Means + DBSCAN + GMM + Hierarchical
7. **Evaluación**: Silhouette, Davies-Bouldin, Calinski-Harabasz
8. **Visualización Final (R)**: ggplot2 para plots nivel publicación

**Workflow**: Python 90% → R 10% (solo plots finales)

## Alcance del Proyecto

### Algoritmos Implementados
- **k-means**: k=3-10, método del codo + Silhouette
- **DBSCAN**: eps optimizado con k-dist graph
- **Gaussian Mixture**: BIC para selección de componentes
- **Hierarchical**: Ward's method, dendrograma

### Métricas de Evaluación
- Silhouette Score (cohesión)
- Davies-Bouldin Index (separación)
- Calinski-Harabasz Score (varianza)
- Pureza por método de detección (análisis de sesgo)

### Visualizaciones Clave
1. Diagrama masa-radio (log-log, coloreado por cluster)
2. t-SNE 2D con clusters
3. Dendrograma jerárquico
4. Distribuciones por cluster (boxplots)
5. Mapa de zona habitable
6. Análisis de sesgo por método de detección

## Criterios de Éxito (Puntuación)

- **Interpretación astrofísica**: 30/100pts (más alto)
- **Clustering correcto**: 20/100pts
- **Creatividad del modelo**: 20/100pts
- **Estructura CRISP-DM**: 10/100pts
- **Comunicación de resultados**: 10/100pts
- **Viabilidad**: 10/100pts

## Expected Clusters

- Planetas tipo Tierra (< 1.25 R⊕)
- Super-Tierras (1.25-2.0 R⊕)
- Sub-Neptunos (2.0-4.0 R⊕)
- Hot Jupiters (> 10 R⊕, periodos cortos)
- Gigantes fríos (periodos largos)
- Planetas anómalos (outliers)

## Team Structure

- **Integrante A (Data Lead)**: Ingesta, limpieza, feature engineering
- **Integrante B (ML Lead)**: Clustering, optimización, métricas
- **Integrante C (Astro Lead)**: Interpretación, taxonomía, zona habitable
- **Integrante D (Viz Lead)**: Visualizaciones, presentación, slides

## Diferenciadores P.E.R.F.E.C.T

- **P**rocess robusto: Imputación científica, no medias
- **E**valuación multi-algoritmo: 4 métodos comparados
- **R**igurosidad: Pipeline sin leakage
- **F**eature engineering: 7+ variables físicas
- **E**stética: Visualizaciones nivel publicación
- **C**lustering: Detección de desierto de Neptuno
- **T**axonomía: Mapeo directo a literatura astrofísica

## Timeline

- **Día 1 (22 abr)**: Ingesta, exploración, instalación paquetes
- **Día 2 (23 abr)**: Feature engineering, EDA, imputación física
- **Día 3 (24 abr)**: Clustering, PCA, dimensionality reduction
- **Día 4 (25 abr)**: Evaluación métricas, selección final
- **Día 5 (26 abr)**: Interpretación, zona habitable, visualizaciones
- **Día 6 (27 abr)**: Entrega repositorio, ensayo
- **Día 7-8 (28-29 abr)**: Presentación final

## Contacto

- **Proyecto**: ExoData Challenge 2026 — Feria de Puebla
- **Dataset**: NASA Exoplanet Archive PSCompPars
- **Fecha**: 24 de abril de 2026
