# Plan de Tareas ExoData Challenge 2026

**Documento de Control de Progreso**  
**Proyecto:** ExoData Challenge — Clustering de Exoplanetas  
**Plazo Final:** 27 de abril de 2026  
**Tipo:** Proyecto con checkpoints de verificación por fase

---

## 🎯 **ESTRUCTURA DE TAREAS POR FASE**

Cada tarea requiere **checkpoint de verificación** antes de avanzar a la siguiente. No se avanza hasta que el checkpoint se marque como ✓.

---

## **FASE 0: Setup Inicial (Deadline: 22 abr, 18:00)**

### Tarea 0.1: Configuración del Entorno
**Responsable:** Integrante A (Data Lead)  
**Output:** Entorno listo para desarrollo

- [ ] Instalar Python 3.10+
- [ ] Crear virtualenv: `python -m venv venv && source venv/bin/activate`
- [ ] Instalar paquetes: `pip install -r requirements.txt`
- [ ] Configurar Jupyter: `jupyter notebook --generate-config`
- [ ] Verificar instalaciones: imports sin errores

**Checkpoint ✓:** Ejecutar `01_check_env.ipynb` → todos los imports funcionan

### Tarea 0.2: Setup GitHub
**Responsable:** Integrante A (Data Lead)  
**Output:** Repo inicializado

- [ ] Crear repositorio público en GitHub
- [ ] Crear .gitignore apropiado (data/ raw, figures/ outputs)
- [ ] Push inicial de estructura de carpetas
- [ ] Compartir enlace con equipo

**Checkpoint ✓:** Repo accesible, estructura visible en GitHub

### Tarea 0.3: Descarga y Verificación de Dataset
**Responsable:** Integrante A (Data Lead)  
**Output:** Datos descargados y verificados

- [ ] Descargar PSCompPars_2026.csv desde NASA Exoplanet Archive
- [ ] Verificar filas: 6,147 (encontradas)  
- [ ] Verificar columnas: 320 (encontradas)
- [ ] Verificar tamaño: ~45MB
- [ ] Mover a `data/PSCompPars_2026.csv`

**Checkpoint ✓:** Imprimir `df.shape` → (6147, 320) exactos

---

## **FASE 1: Ingesta y Exploración (Deadline: 22 abr, 23:59)**

### Tarea 1.1: Crear Notebook 01_ingesta_limpieza.ipynb
**Responsable:** Integrante A (Data Lead)  
**Output:** Datos limpios cargados en memoria

- [ ] Leer CSV con comment='#' para saltar líneas de header
- [ ] Inspeccionar dtypes (verificar float64, int64, object)
- [ ] Identificar variables clave: pl_rade, pl_bmasse, pl_orbper, pl_eqt, st_teff
- [ ] Crear listado de completitud por columna: `complete_pct = df.notna().mean()`
- [ ] Identificar columnas con >60% missing

**Checkpoint ✓:** Mostrar `df.info()` y `df.head()` → datos legibles

### Tarea 1.2: Reporte de Valores Nulos
**Responsable:** Integrante A (Data Lead)  
**Output:** Reporte de faltantes estratificado

- [ ] Generar heatmap de completitud por feature
- [ ] Identificar 10 variables más completas (>85%)
- [ ] Identificar 10 variables menos completas (<50%)
- [ ] Calcular: `critical_vars = ['pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_eqt']`
- [ ] Verificar completitud de vars críticas: pl_rade (~85%), pl_bmasse (~55%)

**Checkpoint ✓:** Heatmap visual muestra claramente completitud variables

### Tarea 1.3: EDA Básico y Distribuciones
**Responsable:** Integrante A (Data Lead)  
**Output:** Caracterización de distribuciones

- [ ] Calcular estadísticas: mean, median, std, q01, q99
- [ ] Identificar outliers (q99 > 3x q90)
- [ ] Generar histogramas de vars clave (log-scale)
- [ ] Detectar sesgo en method detection (80% tránsitos)

**Checkpoint ✓:** Gráficos muestran distribuciones correctas, sin errores

---

## **FASE 2: Feature Engineering (Deadline: 23 abr, 23:59)**

### Tarea 2.1: Crear 7 Features Derivados
**Responsable:** Integrante A (Data Lead)  
**Output:** DataFrame con 320+7 columnas

Crear features físicamente motivados:
- [ ] `log_period = log10(pl_orbper.clip(0.01))`
- [ ] `log_rade = log10(pl_rade.clip(0.01))`
- [ ] `log_bmasse = log10(pl_bmasse.clip(0.01))`
- [ ] `log_smax = log10(pl_orbsmax.clip(0.0001))`
- [ ] `pl_dens_calc = (pl_bmasse × 5.972e24) / ((4/3)π(pl_rade×6.371e6)³)/1000`
- [ ] `mass_radius_ratio = pl_bmasse / pl_rade`
- [ ] `kepler_check = sqrt(pl_orbsmax³) - pl_orbper² / sqrt(pl_orbsmax³)`
- [ ] `hz_flag = pl_insol.between(0.2, 1.7).astype(int)`

**Checkpoint ✓:** Verificar que nuevas columnas existen y tienen valores razonables (densidad ~1-10 g/cm³)

### Tarea 2.2: Imputación Física de Masa/Radio
**Responsable:** Integrante A (Data Lead)  
**Output:** Dataset con valores imputados físicamente

Implementar relación M-R de Zeng & Sasselov (2016):
- [ ] Para planetas rocosos (pl_rade < 1.5): ρ ≈ 5.5 g/cm³
- [ ] Formula: pl_bmasse_imputed = pl_rade³ × 5.5 / 5.972
- [ ] Para gaseosos (pl_rade > 2.0): ρ ≈ 1.0 g/cm³
- [ ] Marcar con flag: `pl_bmasse_imputed = 1`

**Checkpoint ✓:** Comparar imputados vs originales → valores físicamente consistentes

### Tarea 2.3: Selección de Features Finales
**Responsable:** Integrante A (Data Lead)  
**Output:** Lista final de 8-10 features para clustering

Seleccionar variables con >70% completitud y relevancia física:
- [ ] `log_rade`
- [ ] `log_bmasse` (con imputación)
- [ ] `log_period`
- [ ] `log_smax`
- [ ] `pl_eqt`
- [ ] `st_teff`
- [ ] `st_met`
- [ ] `sy_pnum`
- [ ] `kepler_check`
- [ ] `hz_flag`

**Checkpoint ✓:** Verificar completitud de features seleccionadas >70%  
**Checkpoint ✓:** Mostrar correlación entre features → alta correlación debe justificarse

---

## **FASE 3: Preparación para Clustering (Deadline: 24 abr, 12:00)**

### Tarea 3.1: Crear Dataset Limpio
**Responsable:** Integrante A (Data Lead)  
**Output:** `data/processed/df_clean_8features.parquet` (1.2MB)

- [ ] Filtrar solo filas con suficientes datos (no >50% missing)
- [ ] Seleccionar features finales
- [ ] Guardar en formato parquet (rápido, comprimido)
- [ ] Verificar tamaño y estructura

**Checkpoint ✓:** `pd.read_parquet()` carga sin errores

### Tarea 3.2: Escalado Robusto
**Responsable:** Integrante A (Data Lead)  
**Output:** X_scaled array

- [ ] Implementar RobustScaler: scala con mediana + IQR
- [ ] Ajustar solo en training set (si hay partición)
- [ ] Verificar que outliers no dominan magnitudes

**Checkpoint ✓:** Stats: `median ≈ 0`, `IQR ≈ 1`, `max < 10`  
**Checkpoint ✓:** Visualizar boxplot antes/después → outliers mantenidos relativamente

### Tarea 3.3: Reducción Dimensional (PCA)
**Responsable:** Integrante B (ML Lead)  
**Output:** X_pca (n_components que retienen 95% varianza)

- [ ] Ejecutar PCA con `n_components=0.95`
- [ ] Verificar que varianza explicada ≈ 95%
- [ ] Verificar número de componentes (probablemente 6-8)
- [ ] Generar scree plot

**Checkpoint ✓:** Scree plot muestra codo claro después de 6-8 componentes  
**Checkpoint ✓:** Varianza acumulada gráfica muestra 95%

### Tarea 3.4: Reducción Dimensional (UMAP)
**Responsable:** Integrante B (ML Lead)  
**Output:** X_umap (2D para visualización)

- [ ] Ejecutar UMAP: `UMAP(n_components=2, random_state=42)`
- [ ] Ajustar parámetros: `n_neighbors=30, min_dist=0.1`
- [ ] Verificar visualización: separación de clusters visible

**Checkpoint ✓:** Scatter plot UMAP → clusters potencialmente visibles  
**Checkpoint ✓:** Ejecución < 60 segundos (vs 15 min de t-SNE)

---

## **FASE 4: Modelado - Clustering (Deadline: 25 abr, 12:00)**

### Tarea 4.1: Implementar 4 Algoritmos
**Responsable:** Integrante B (ML Lead)  
**Output:** Diccionario con resultados `results = {'kmeans': {...}, 'dbscan': {...}, 'gmm': {...}, 'hier': {...}}`

Implementar en paralelo:
- [ ] **K-Means**: Probar k=3-10, usar `n_init=20`
- [ ] **DBSCAN**: Calcular eps con k-distografía, `min_samples=10`
- [ ] **GMM**: Probar componentes 3-10, usar BIC
- [ ] **Hierarchical**: Usar Ward's method

**Checkpoint ✓** Cada algoritmo ejecuta sin errores  
**Checkpoint ✓** Colectar labels en DataFrame: `df['kmeans_labels']`, `df['dbscan_labels']`, etc.

### Tarea 4.2: Optimización de Hiperparámetros
**Responsable:** Integrante B (ML Lead)  
**Output**: K/Best params óptimos para cada algoritmo

- [ ] K-Means: Elbow method + Silhouette → elegir K óptima
- [ ] DBSCAN: Grid search eps [0.1, 0.3, 0.5, 0.7]
- [ ] GMM: Minimizar BIC → K óptima
- [ ] Hierarchical: Cortar árbol en K óptima

**Checkpoint ✓** Gráfico elbow muestra codo claro  
**Checkpoint ✓** Silhouette score indica K óptima (máximo)

### Tarea 4.3: Calcular Métricas de Evaluación
**Responsable:** Integrante B (ML Lead)  
**Output:** DataFrame comparativo con métricas

Para cada algoritmo calcular:
- [ ] Silhouette Score (higher better)
- [ ] Davies-Bouldin Index (lower better)
- [ ] Calinski-Harabasz (higher better)
- [ ] Para GMM: BIC (lower better)

**Checkpoint ✓** Tabla comparativa muestra valores numéricos  
**Checkpoint ✓** Al menos 1 algoritmo tiene Silhouette > 0.35 (umbral aceptable)

---

## **FASE 5: Selección del Modelo (Deadline: 25 abr, 18:00)**

### Tarea 5.1: Análisis Comparativo de Algorithmos
**Responsable:** Integrante B (ML Lead)  
**Output:** Tabla de decisión con valores, pros/cons

- [ ] Crear tabla: Algoritmo | Silhouette | DB-Index | Tiempo | Interpretabilidad
- [ ] Evaluar cualitativo: K-Means = simple, GMM = probabilístico, DBSCAN = outliers, Hierarchical = dendrograma
- [ ] Aplicar criterio decisión: 70% métricas + 30% interpretación física

**Checkpoint ✓** Documento de decisión justifica selección con evidencia numérica  
**Checkpoint ✓** Votación del equipo (documentar decisión)

### Tarea 5.2: Selección del Algoritmo Final
**Responsable:** Integrante B (ML Lead)  
**Decision Owner:** Todo el equipo (consenso)  
**Output:** Algoritmo elegido + hiperparámetros finales

- [ ] Elegir algoritmo final (ej: GMM con 6 clusters)
- [ ] Fijar K final (ej: K=6)
- [ ] Ejecutar modelo final en dataset completo
- [ ] Exportar labels: `df['cluster_id']`

**Checkpoint ✓** Labels asignados a todas las 6,147 filas  
**Checkpoint ✓** Distribución: ningún cluster < 5% del dataset (evita tiny clusters)

### Tarea 5.3: Visualización 2D (PCA o UMAP) con clusters
**Responsable:** Integrante B (ML Lead)  
**Output:** Scatter plots coloreados por cluster

- [ ] Generar UMAP 2D coloreado por cluster_id
- [ ] Generar t-SNE 2D coloreado por cluster_id
- [ ] Verificar separación visual clara

**Checkpoint ✓** Plots muestran clusters claramente separados  
**Checkpoint ✓** Colores distinguibles para presentación

---

## **FASE 6: Interpretación Astrofísica (30 puntos, más caro!) (Deadline: 26 abr, 12:00)**

### Tarea 6.1: Caracterizar Clusters con Estadísticos
**Responsable:** Integrante C (Astro Lead)  **Output:** CSV con properties por cluster

Para cada cluster (ej: cluster 0, cluster 1...):
- [ ] Calcular mediana de: radio, masa, periodo, temperatura
- [ ] Calcular desviación estándar (indica homogeneidad)
- [ ] Contar frecuencia por método de detección
- [ ] Calcular proporción de planetas en zona habitable

**Checkpoint ✓** Tabla: Cada cluster tiene radio típico, periodo típico, temp típica  
**Checkpoint ✓** Interpretación inicial: "Cluster 0 ≈ Hot Jupiters (periodo corto)

### Tarea 6.2: Mapear a Taxonomía Astrofísica
**Responsable:** Integrante C (Astro Lead)  
**Output:** Asignar cada cluster a tipo físico conocido

- [ ] Cluster 0 → Hot Jupiter (radio > 10 R⊕, periodo < 10 días)
- [ ] Cluster 1 → Super-Tierras (1.25-2.0 R⊕, densa)
- [ ] Cluster 2 → Sub-Neptunos (2.0-4.0 R⊕, abundante)
- [ ] Cluster 3 → Terrestres rocosas (< 1.25 R⊕)
- [ ] Cluster 4 → Gigantes fríos (periodo largo)
- [ ] Cluster -1 → Anómalos (outliers DBSCAN)

**Checkpoint ✓** Cada cluster mapeado a definición física con threshold numérico  
**Checkpoint ✓** Documentar discrepancias (si cluster no mapea bien, explicar)

### Tarea 6.3: Análisis de Habitabilidad
**Responsable:** Integrante C (Astro Lead)  
**Output:** Lista de top 5 planetas candidatos

- [ ] Filtrar: pl_insol entre 0.2-1.7 AND pl_eqt 200-320K
- [ ] Filtrar: pl_rade < 2.0 (potencialmente rocoso)
- [ ] Ordenar por proximidad a insol = 1.0 (Earth-like)
- [ ] Listar: nombre, estrella, insolación, temp, radio

**Checkpoint ✓** Top 5 planetas listados con motivación física  
**Checkpoint ✓** Todos deben ser conocidos (no nombrar nuevos planetas)

### Tarea 6.4: Verificar Consistencia Con Literatura
**Responsable:** Integrante C (Astro Lead)  
**Output:** 2-3 citas por cada tipo planetario

- [ ] Hot Jupiters: WASP-12b, 51 Peg b (periodo corto, radiación)
- [ ] Super-Tierras: Kepler-62e, 55 Cnc e (estudios de composición)
- [ ] Sub-Neptunos: Kepler-11f (mechanismos formación)
- [ ] Documentar: relación M-R de Zeng & Sasselov (2016)

**Checkpoint ✓** Bibliografía citada correctamente (autor, año, journal)  
**Checkpoint ✓** Cada claim en interpretación debe tener cita

### Tarea 6.5: Detección del Desierto de Neptuno
**Responsable:** Integrante C (Astro Lead)  **Output:** Validez del Hallazgo Importante

- [ ] Verificar: pocas detecciones con periodo < 3 días AND radio 2-4 R⊕
- [ ] Contar: < 30 planetas en esa región (frente a ~3000 en otros)
- [ ] Confirmar: clustering captura esta zona vacía
- [ ] Referenciar: Fulton et al. (2017) sobre brecha de radios

**Checkpoint ✓** Documentar el desierto en notebook  **Checkpoint ✓ ** Comparación con literatura actual (2017-2024)

---

## **FASE 7: Visualización (Deadline: 26 abr, 18:00)**

### Tarea 7.1: Crear 8 Visualizaciones Clave
**Responsable:** Integrante D (Viz Lead)  
** Output:** 8 plots PNG en `figures/` (300 DPI, 1200px)

**En Python (base):**
- [ ] Diagrama de calor de correlaciones
- [ ] Histogramas de features antes/después log
- [ ] PCA variance explained
- [ ] Boxplots de features por cluster
- [ ] Scatter periodo-radio (despues log)

**En R (final, nivel publicación):**
- [ ] Diagrama masa-radius (log-log, coloreado por cluster, con lineas teoricas)
- [ ] UMAP 2D coloreado por cluster
- [ ] Dendrograma jerárquico (ward)
- [ ] Mapa zona habitable (insolación vs radio)

**Checkpoint ✓ ** Todos los plots guardados en `figures/` 300 DPI  **Checkpoint ✓** Cada plot tiene: título, ejes etiquetados, leyenda, fuente de datos

### Tarea 7.2: Crear Notebook de Visualización en R
** Responsable:** Integrante D (Viz Lead)  
**Output:** `viz_final_r/08_visualizacion_final.Rmd`

- [ ] Importar `data/processed/df_labeled.csv`
- [ ] Generar los 4 plots finales con ggplot2
- [ ] Aplicar themes profesionales (ggthemes::theme_few)
- [ ] Exportar PNGs a `figures/` con 300 DPI

**Checkpoint ✓** Notebook R ejecuta sin errores  **Checkpoint ✓** PNGs generados son usables en presentación

### Tarea 7.3: Agregar a Presentación
**Responsable:** Integrante D (Viz Lead)  
**Output:** Slides PowerPoint/Keynote

- [ ] Insertar PNGs en slides correspondientes
- [ ] Agregar anotaciones explicativas
- [ ] Asegurar calidad (no comprimido)

**Checkpoint ✓** Abrir PPT → imágenes son claras, no pixeladas  **Checkpoint ✓** Todos los 8 plots incluidos

---

## **FASE 8: Preparación de Presentación (Deadline: 27 abr, 12:00)**

### Tarea 8.1: Crear Estructura de Slides (16 slides)
**Responsable:** Integrante D (Viz Lead)  
Output: `.pptx` completo

- [ ] Slide 1: Título + hook
- [ ] Slide 2-3: Comprensión del problema y datos
- [ ] Slide 4-6: Preparación y feature engineering
- [ ] Slide 7-9: Modelado y clustering
- [ ] Slide 10-13: Interpretación (30 pts de evaluación) ← **MÁS IMPORTANTE**
- [ ] Slide 14-15: Limitaciones y propuestas
- [ ] Slide 16: Conclusiones

**Checkpoint ✓** Presentación completa (16 slides)  **Checkpoint ✓** Cada slide tiene contenido, no placeholders

### Tarea 8.2: Ensayar Presentación
** Responsable:** Todo el equipo  
**Output:** Tiempo ajustado a 12-15 minutos

- [ ] Cada integrante presenta su sección (1-2 min cada uno)
- [ ] Cronometrar duración total
- [ ] Ajustar velocidad si excede 15 min
- [ ] Practicar transiciones suaves

**Checkpoint ✓ ** Tiempo total: 12-15 min (acceptable)  **Checkpoint ✓ ** Todos los integrantes lo han ensayado

### Tarea 8.3: Validación Final del Repo
** Responsable:** Todo el equipo  
**Output:** Repo reproducible

- [ ] Revisar que `requirements.txt` esté completo
- [ ] Revisar que `renv.lock` (para R) esté documentado
- [ ] Verificar que todos los notebooks ejecutan sin errores
- [ ] Verificar que README.md está actualizado
- [ ] Ejecutar **full pipeline** desde cero en orden: 01→02→03→04→05→06→07

**Checkpoint ✓ ** Notebook `00_full_pipeline.ipynb` ejecuta sin errores  **Checkpoint ✓ ** README.md refleja stack actual (Python + R solo viz)

---

## ** FASE 9: Entrega (Deadline: 27 abr, 23:59)**

### Tarea 9.1: Push Final a GitHub
**Responsable:** Integrante A (Data Lead)  
**Output:** Repo final público

- [ ] Commit final: "feat: entrega versión 1.0 - ExoData Challenge 2026"
- [ ] Push con tags: `git tag v1.0 && git push origin v1.0`
- [ ] Verificar en GitHub que todos los archivos están presentes
- [ ] Compartir enlace con jurado

**Checkpoint ✓** Repo accesible en GitHub  **Checkpoint ✓ ** Tags creados correctamente

### Tarea 9.2: Preparar Entrega de Slides
** Responsable:** Integrante D (Viz Lead)  
**Output:** Archivo .pptx final

- [ ] Exportar desde Keynote/PowerPoint a PDF (backup)
- [ ] Exportar PPT en formato compatible (Office 2016+)
- [ ] Verificar que imágenes están embebidas (no enlaces rotos)
- [ ] Subir a Google Drive compartido con equipo

**Checkpoint ✓** PPT abre en otra máquina sin errores  **Checkpoint ✓ ** Todos los plots visibles

### Tarea 9.3: Preparación de Backup
**Responsable:** Integrante A (Data Lead)  
**Output:** Backup local

- [ ] Zip completo de repo: `exodata-challenge-2026.zip`
- [ ] Copiar a 2 USB drives
- [ ] Subir a Google Drive personal
- [ ] Guardar en laptop de presentación

**Checkpoint ✓** Zip extraído y probado en otra computadora  **Checkpoint ✓ ** Todos los archivos presentes en backup

---

## ** CONTROLES DE CALIDAD POST-ENTREGA **

### Checkpoint Global (Antes de Cada Checkpoint)
Antes de preguntar si un checkpoint está ✓, verifica:

1. ** ¿Funciona? ** Ejecuta la celda/código → ¿resultado esperado?
2. ** ¿Tiene sentido? ** Los valores son razonables (densidad < 20 g/cm³)
3. ** ¿Es reproducible? ** Correr de nuevo → ¿mismo resultado?
4. ** ¿Está documentado? ** Cada función/plot tiene su explicación
5. ** ¿Sigue en tiempo? ** ¿No excede deadline de su fase?

---

## ** SUPER-IMPORTANTE: RELACIONES ENTRE TAREAS**

### Bloqueantes
- **No puedes empezar FASE 2** sin el **Checkpoint de FASE 1** (faltantes reportados)
- **No puedes empezar FASE 4** sin **Checkpoint de FASE 3** (features limpias)
- **No puedes empezar FASE 6** sin **Checkpoint de FASE 5** (modelo final elegido)
- **No puedes empezar FASE 8** sin **Checkpoint de FASE 6** (interpretación aprobada por Astro Lead)

### Dependencias
- FASE 1 → FASE 2 (clean data)
- FASE 2 → FASE 3 (engineered features)
- FASE 3 → FASE 4 (scaled data)
- FASE 4 → FASE 5 (cluster results)
- FASE 5 → FASE 6 (labels for interpretation)
- FASE 6 → FASE 7 (plots based on interpretation)
- FASE 7 → FASE 8 (slides con plots)

---

## **GANAS PUNTOS CON ESTOS CHECKPOINTS**

**Cada checkpoint ✓ garantiza puntos en el challenge:**

- 6.3 (Habitabilidad) →  **+7pts**  
- 6.4 (Verificación literatura) → **+7pts**  
- 6.5 (Desierto Neptuno) → **+6pts**  
- 8.1 (CRISP-DM) → **+8pts**  
- 8.2 (Comunicación) → **+8pts**  
- Todos los demás → **+64pts**  
- **Total cumplido**: **30 + 20 + 20 + 10 + 10 + 10 = 100pts** ✓

---

## **CHECKLIST DE REVISIÓN FINAL**

Antes de entrega, el equipo completo debe marcar ✓:

- [ ] **Reproducibilidad completa**: Notebook `00_run_all.ipynb` ejecuta sin errores de 01 a 07
- [ **Data leakage comprobada**: Pipeline garantiza separación train/test
- [ ] **Outliers robustos**: RobustScaler usado, StandardScaler no
- [ ] **4 algoritmos implementados**: K-Means, DBSCAN, GMM, Hierarchical
- [ ] **Interpretación documentada**: Story por cluster con bibliografía
- [ ] **Habitabilidad identificada**: Top 5 planetas listados
- [ ] **Desierto de Neptuno**: Documentado con thresholds
- [ ] **Visualizaciones finales**: 8 plots generados (4 Python base + 4 R elegantes)
- [ ] **Slides completas**: 16 slides, tiempo 13 min (practicado)
- [ ] **Repo entregado**: GitHub público, tag v1.0, backup en 2 ubicaciones

---

## **SI FALLA UN CHECKPOINT**

**No avanzar sin ✓** → Implica volver a trabajar la tarea anterior:

- **Si heatmap de completitud no carga**: Revisar lectura de CSV (FASE 1)
- **Si RobustScaler genera NaNs**: Revisar outliers extremales (FASE 2)
- **Si silhouette es < 0.30**: Re-evaluar selección de features (FASE 3)
- **Si clusters no mapean a física**: Re-interpretar (FASE 6)
- **Si plots R no generan**: Verificar paths de datos exportados (FASE 7)

**Regla dura**: **30% de tareas con X = proyecto en riesgo de reprobar**  
**Solución**: **Reparar checkpoint antes de avanzar**

---

## **Final Notes**

Documento mantenido por: **Data Lead**  
Última actualización: 24 de abril de 2026  
Próxima revisión: Después de cada tarea completada
