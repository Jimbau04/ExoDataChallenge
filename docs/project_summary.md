# Resumen Ejecutivo — ExoData Challenge 2026

## ¿Qué es?
Un análisis de **6,147 exoplanetas** del NASA Exoplanet Archive usando **clustering no supervisado** para descubrir la taxonomía natural de los planetas extrasolares.

## Equipo
- **4 integrantes** con roles definidos: Data Lead, ML Lead, Astro Lead, Viz & Presentation Lead
- **Deadline**: 27 de abril (entrega) | **Presentación**: 29 de abril en el Planetario de Puebla

## Objetivo Principal
Construir clusters que sean:
1. **Estadísticamente válidos** (métricas: Silhouette, Davies-Bouldin, Calinski-Harabasz)
2. **Físicamente interpretables** (alineados con tipologías: Hot Jupiters, super-Tierras, sub-Neptunos)
3. **Narrativamente impactantes** (con historia astrofísica para cada cluster)

## Datasheet Clave
- **Dataset**: PSCompPars (Planetary Systems Composite Parameters)
- **Tamaño**: 6,147 filas × 320 columnas
- **Variables principales**: radio, masa, periodo orbital, semi-eje mayor, temperatura, metalicidad estelar
- **Problema**: Datos heterogéneos, múltiples valores nulos, sesgos de detección

## Estrategia de Ganar (Diferenciadores)
1. **Multi-algoritmo**: K-Means + DBSCAN + GMM + Jerárquico (comparativa completa)
2. **Imputación científica**: Usar relaciones físicas reales (Zeng & Sasselov M-R) en lugar de medias
3. **Ingeniería avanzada**: 7 features derivados con sentido físico (densidad, insolación, ratio Kepler)
4. **Análisis de sesgo**: Corrección por método de detección (tránsito vs. velocidad radial)
5. **Habitabilidad**: Identificar planetas en zona habitable usando `pl_insol` y `pl_eqt`
6. **Visualización nivel publicación**: Diagrama masa-radio, t-SNE, H-R, desierto de Neptuno

## Pipeline de Análisis en Python (8 pasos CRISP-DM)
1. Ingesta & limpieza con pandas
2. EDA exploratorio con pandas + matplotlib/seaborn
3. Feature engineering con pandas + numpy
4. Escalado robusto con RobustScaler (median + IQR)
5. Reducción dimensional con PCA (95%) + t-SNE/UMAP
6. Clustering (4 algoritmos: KMeans, DBSCAN, GaussianMixture, Agglomerative)
7. Evaluación (Silhouette, Davies-Bouldin, Calinski-Harabasz)
8. Interpretación astrofísica

## Stack Técnico
**Lenguaje Principal:** Python (versión 3.10+)
**Paquetes Clave:** pandas, numpy, scikit-learn, umap-learn, matplotlib, seaborn, jupyter
**Visualización Final (R):** tidyverse, ggplot2, scales (solo para plots nivel publicación final)

## Estructura de la Presentación (CRISP-DM, 16 slides)
- Hook emocional (1 min)
- Comprensión de datos (2 min)
- Preparación & features (3 min)
- Modelado & métricas (3 min)
- **Interpretación astrofísica (3 min)** ← **Peso más alto: 30 pts**
- Conclusiones (1 min)

## Taxonomía Esperada
- Planetas tipo Tierra (< 1.25 R⊕)
- Super-Tierras (1.25-2.0 R⊕)
- Sub-Neptunos (2.0-4.0 R⊕)
- Hot Jupiters (> 10 R⊕, periodos cortos)
- Gigantes fríos (periodos largos)
- Planetas anómalos (outliers, DBSCAN)

## Hallazgo Diferenciador
El **"desierto de Neptuno"**: planetas con radios 2-4 R⊕ y periodos < 3 días son extremadamente raros. Si el clustering lo captura → resultado astrofísicamente significativo que el jurado reconocerá.

---
**En una frase**: Mientras otros equipos hacen K-Means básico, ustedes cuentan la historia de 6,147 mundos desconocidos, encuentran candidatos a Tierra 2.0 y presentan resultados con rigor científico real.
