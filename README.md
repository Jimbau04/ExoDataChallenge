# ExoData Challenge 2026 — Análisis de Exoplanetas

> **ENTREGA: Lunes 27 de abril de 2026 (3 días restantes)**  
> **Presentación: Miércoles 29 de abril de 2026**  
> **Fase actual:** Fase 1 (Ingesta y Auditoría) — Retraso de ~2 días respecto al plan

---

| Fecha | Día | Fase planeada | Estado real |
|-------|-----|---------------|-------------|
| 22 abr (Mié) | Día 1 | Ingesta, exploración, paquetes | ✅ Completado (parcial) |
| 23 abr (Jue) | Día 2 | Feature engineering, EDA, imputación | ❌ No iniciado |
| 24 abr (Vie) | Día 3 | Clustering, PCA, reducción dimensional | ❌ No iniciado |
| **25 abr (Sáb)** | **Día 4** | **Evaluación métricas, selección final** | ❌ Pendiente |
| **26 abr (Dom)** | **Día 5** | **Interpretación, HZ, visualizaciones** | ❌ Pendiente |
| **27 abr (Lun)** | **Día 6** | **Entrega repositorio, ensayo** | **DEADLINE** |
| 28 abr (Mar) | Día 7 | Ensayos finales | — |
| 29 abr (Mié) | Día 8 | **PRESENTACIÓN** final | — |

---

## Descripción del Proyecto

**Objetivo:** Descubrir la taxonomía natural de 6,147 exoplanetas confirmados mediante clustering no supervisado con análisis astrofísico profundo.

**Evento:** Feria de Puebla 2026 — Planetario de Puebla

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

### Estado actual (24 abril 2026)

```
├── data/
│   ├── PSCompPars_2026.csv            ✅ Dataset completo (46MB)
│   └── Dataset Reducido.csv           ✅ Dataset reducido (4MB)
├── docs/
│   ├── tareas_proyecto.md             ✅ Plan de trabajo detallado
│   ├── project_brief.md               ✅ Brief del proyecto
│   ├── project_summary.md             ✅ Resumen ejecutivo
│   ├── top20_completitud.csv          ✅ Reporte de completitud
│   ├── critical_vars_completitud.csv  ✅ Variables críticas (incluye pl_insol)
│   ├── detection_method_distribution.csv ✅ Sesgo por método de detección
│   └── archivos/                      ✅ PDFs de referencia (NASA, guías, PRD)
├── notebooks/
│   └── 01_ingesta_limpieza.ipynb      ✅ Fase 1: Ingesta y auditoría
├── src/
│   └── .gitkeep                       ⬜ Módulos Python pendientes
├── requirements.txt                   ✅ Dependencias Python
└── README.md                          ✅ Este archivo
```

### Pendiente por crear

```
├── data/
│   └── processed/                     ⬜ Datos procesados
├── notebooks/
│   ├── 02_feature_engineering.ipynb   ⬜ Fase 2: EDA + features derivados
│   ├── 03_clustering_comparativo.ipynb ⬜ Fase 3-4: 4 algoritmos
│   ├── 04_evaluacion_modelos.ipynb    ⬜ Fase 5: Métricas
│   ├── 05_interpretacion.ipynb        ⬜ Fase 6: Taxonomía astrofísica
│   └── 06_visualizaciones.ipynb       ⬜ Fase 7: Plots base Python
├── src/
│   ├── utils.py                       ⬜ Funciones auxiliares
│   ├── features.py                    ⬜ Feature engineering
│   ├── imputacion_fisica.py           ⬜ Imputación Zeng & Sasselov
│   └── clustering.py                  ⬜ Pipeline clustering
├── viz_final_r/
│   └── 08_visualizacion_final.Rmd     ⬜ ggplot2 final plots
├── figures/                           ⬜ Diagramas de salida
├── presentation/
│   └── ExoData_Challenge_2026.pptx    ⬜ Presentación final
└── .venv/                             ⬜ Entorno virtual (no en git)
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

## Progreso y Estado

### Completado (24 abr 2026)
- [x] Documentación del proyecto (`docs/tareas_proyecto.md`, `project_brief.md`, `project_summary.md`, `python_vs_r_analysis.md`)
- [x] PDFs de referencia (NASA, guía astrofísica, PRD)
- [x] `requirements.txt` con dependencias Python
- [x] Fase 1: Carga y auditoría del dataset (`notebooks/01_ingesta_limpieza.ipynb`)
- [x] Reportes CSV: `top20_completitud.csv`, `critical_vars_completitud.csv`, `detection_method_distribution.csv`
- [x] Auditoría de fallos documentada en `tareas_proyecto.md` (Sección 12)

### Pendiente (prioridad descendente)
1. **Fase 2** — Feature engineering + imputación física Zeng & Sasselov + RobustScaler
2. **Fase 3** — PCA (95%) + UMAP + t-SNE
3. **Fase 4** — K-Means, DBSCAN, GMM, Hierarchical clustering
4. **Fase 5** — Evaluación (Silhouette, Davies-Bouldin, Calinski-Harabasz, BIC) + modelo final
5. **Fase 6** — Interpretación astrofísica (taxonomía, sesgos, "Neptune Desert", HZ)
6. **Fase 7** — Visualizaciones (8 requeridas)
7. **Fase 8** — Presentación (12-16 slides)
8. **Fase 9** — Entrega final y ensayo

## Contacto

- **Proyecto**: ExoData Challenge 2026 — Feria de Puebla
- **Dataset**: NASA Exoplanet Archive PSCompPars
- **Fecha**: 24 de abril de 2026
