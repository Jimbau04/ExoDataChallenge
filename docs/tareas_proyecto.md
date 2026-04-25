# Plan de Trabajo Colaborativo - ExoData Challenge 2026

**Proyecto:** ExoData Challenge - Clustering de Exoplanetas  
**Entrega:** 27 de abril de 2026  
**Presentacion:** 29 de abril de 2026  
**Modo de trabajo:** Equipo distribuido, cada integrante en su propia PC  
**Stack principal:** Python para analisis/modelado, R opcional solo para visualizacion final

---

## 1. Enfoque de Cooperacion

Este proyecto no debe depender de una sola computadora ni de un solo entorno virtual compartido. Cada integrante trabaja localmente en su PC, pero todos sincronizan codigo, notebooks, documentacion y resultados mediante GitHub.

### Entorno recomendado

**Recomendacion principal:** GitHub + entornos locales por integrante.

- GitHub para codigo, notebooks, documentacion, issues y ramas.
- Cada integrante crea su propio `.venv` local.
- El entorno virtual no se sube al repositorio.
- `requirements.txt` es la fuente comun de dependencias.
- Los datasets pesados se mantienen en `data/`, pero se documenta de donde salieron.
- Los resultados compartidos van a `data/processed/`, `figures/` y `docs/`.
- La presentacion puede vivir en `presentation/`, pero si pesa mucho se comparte tambien por Drive.

## 2. Roles del Equipo

### Integrante A - Data Lead

**Nombre de la parte:** Lider de Datos  
**Responsabilidad:** ingesta, limpieza, completitud, variables criticas, features derivados e imputacion fisica.

Entregables:

- `notebooks/01_ingesta_limpieza.ipynb`
- `notebooks/02_feature_engineering.ipynb`
- `data/processed/df_clean_features.csv` o `.parquet`
- reportes en `docs/`

### Integrante B - ML Lead

**Nombre de la parte:** Lider de Machine Learning  
**Responsabilidad:** escalado, PCA/UMAP, clustering, comparacion de algoritmos y metricas.

Entregables:

- `notebooks/03_clustering_comparativo.ipynb`
- `notebooks/04_evaluacion_modelos.ipynb`
- `data/processed/df_labeled.csv`
- tabla de metricas en `docs/model_metrics.csv`

### Integrante C - Astro Lead

**Nombre de la parte:** Lider de Interpretacion Astrofisica  
**Responsabilidad:** explicar clusters, habitabilidad, sesgos de deteccion, desierto de Neptuno y soporte bibliografico.

Entregables:

- `notebooks/05_interpretacion_astrofisica.ipynb`
- `docs/cluster_taxonomy.md`
- `docs/habitability_candidates.csv`
- citas y referencias usadas en la presentacion

### Integrante D - Viz Lead

**Nombre de la parte:** Lider de Visualizacion y Presentacion  
**Responsabilidad:** graficas finales, narrativa visual, slides y ensayo.

Entregables:

- `notebooks/06_visualizaciones_python.ipynb`
- `viz_final_r/08_visualizacion_final.Rmd` si se usa R
- `figures/`
- `presentation/ExoData_Challenge_2026.pptx`

---

## 3. Flujo de Trabajo Git para Varias PCs

### Ramas sugeridas

- `main`: version estable, solo se integra codigo revisado.
- `data-lead`: trabajo de limpieza/features.
- `ml-lead`: trabajo de clustering/modelos.
- `astro-lead`: interpretacion cientifica.
- `viz-lead`: visualizaciones y presentacion.

### Rutina diaria minima

1. Antes de trabajar: `git pull origin main`
2. Trabajar en la rama personal.
3. Guardar cambios con commits pequenos y claros.
4. Subir cambios: `git push origin nombre-rama`
5. Integrar a `main` solo cuando el entregable corra o sea revisable.

### Convencion de commits

Usar mensajes simples:

- `docs: actualizar plan colaborativo`
- `feat: agregar features fisicos`
- `feat: implementar clustering kmeans gmm`
- `fix: corregir rutas de notebooks`
- `viz: agregar figura masa-radio`

### Regla importante sobre notebooks

Evitar que dos personas editen el mismo notebook al mismo tiempo. Los notebooks generan conflictos dificiles de resolver.

Mejor:

- Cada lider trabaja su propio notebook.
- La logica repetida va a `src/`.
- Los resultados compartidos se exportan a CSV/parquet.

---

## 4. Setup Realista por Integrante

Cada integrante hace su propio entorno local.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Checkpoint de entorno

El entorno esta listo si estos imports funcionan:

```python
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
```

`umap` puede ser opcional hasta la fase de reduccion dimensional.

---

## 5. Estructura de Carpetas Objetivo

```text
ExoDataChallenge/
├── data/
│   ├── PSCompPars_2026.csv
│   ├── Dataset Reducido.csv
│   └── processed/
├── docs/
│   ├── tareas_proyecto.md
│   ├── project_brief.md
│   ├── project_summary.md
│   ├── cluster_taxonomy.md
│   └── model_metrics.csv
├── figures/
├── notebooks/
│   ├── 01_ingesta_limpieza.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_clustering_comparativo.ipynb
│   ├── 04_evaluacion_modelos.ipynb
│   ├── 05_interpretacion_astrofisica.ipynb
│   └── 06_visualizaciones_python.ipynb
├── presentation/
├── src/
│   ├── utils.py
│   ├── features.py
│   ├── imputation.py
│   └── clustering.py
├── viz_final_r/
├── README.md
└── requirements.txt
```

No todas las carpetas tienen que existir desde el dia 1, pero esta es la estructura hacia la entrega.

---

## 6. Plan por Fases con Checkpoints Cortos

### Fase 0 - Coordinacion Inicial

**Responsables:** Todo el equipo  
**Objetivo:** que todos puedan abrir el proyecto y trabajar sin pisarse.

Tareas:

- [ ] Confirmar quien es Data Lead, ML Lead, Astro Lead y Viz Lead.
- [x] Confirmar que todos tienen acceso al repo.
- [x] Crear `.gitignore` con `.venv/`, checkpoints y cache.

**Checkpoint corto:** cada integrante puede ejecutar imports basicos y hacer `git pull`.

---

### Fase 1 - Ingesta y Auditoria de Datos

**Responsable principal:** Data Lead  
**Apoyo:** Astro Lead valida que las variables tengan sentido fisico.

Tareas:

- [x] Leer `data/PSCompPars_2026.csv` ignorando comentarios.
- [x] Confirmar shape real del dataset (`6160 x 320`).
- [ ] Identificar variables criticas (pendiente incluir `pl_insol` en el reporte de variables criticas).
  - `pl_name`
  - `discoverymethod`
  - `pl_rade`
  - `pl_bmasse`
  - `pl_orbper`
  - `pl_orbsmax`
  - `pl_eqt`
  - `pl_insol`
  - `st_teff`
  - `st_met`
  - `sy_pnum`
- [x] Generar reporte de completitud.
- [x] Revisar distribucion por metodo de deteccion.
- [x] Detectar outliers extremos sin eliminarlos todavia.

Entregables:

- `notebooks/01_ingesta_limpieza.ipynb`
- `docs/top20_completitud.csv`
- `docs/critical_vars_completitud.csv`
- `docs/detection_method_distribution.csv`

**Checkpoint corto:** [ ] dataset carga sin error, shape documentado y variables criticas tienen reporte de completitud.

Estado actual rapido:

- Carga y auditoria basica completadas.
- Los CSV de `docs/` existen, pero el notebook muestra errores por ruta de guardado al usar `docs/...` desde `notebooks/`.
- Falta incluir `pl_insol` en el reporte de variables criticas para cerrar Fase 1 al 100%.

---

### Fase 2 - Limpieza y Feature Engineering

**Responsable principal:** Data Lead  
**Apoyo:** ML Lead revisa que las features sirvan para clustering.

Tareas:

- Corregir rutas de notebooks para que funcionen desde la carpeta del proyecto.
- Crear features derivados:
  - `log_period`
  - `log_rade`
  - `log_bmasse`
  - `log_smax`
  - `pl_dens_calc`
  - `mass_radius_ratio`
  - `hz_flag`
- Imputar masa/radio solo cuando tenga sentido fisico.
- Agregar flags para saber que fue imputado.
- Seleccionar 8-10 features finales.
- Exportar dataset procesado.

Entregables:

- `notebooks/02_feature_engineering.ipynb`
- `src/features.py`
- `src/imputation.py`
- `data/processed/df_clean_features.csv` o `.parquet`

**Checkpoint corto:** el archivo procesado existe, carga en otra PC y no contiene NaN en las features finales.

---

### Fase 3 - Preparacion para Modelado

**Responsable principal:** ML Lead  
**Apoyo:** Data Lead valida que no se rompan las variables.

Tareas:

- Cargar `df_clean_features`.
- Escalar con `RobustScaler`.
- Ejecutar PCA para conservar cerca de 95% de varianza.
- Generar UMAP 2D para visualizacion.
- Guardar matrices o columnas reducidas si son necesarias.

Entregables:

- `notebooks/03_clustering_comparativo.ipynb`
- columnas PCA/UMAP en dataset procesado o archivos auxiliares

**Checkpoint corto:** escalado, PCA y UMAP corren sin error y producen salidas con el mismo numero de filas que el dataset limpio.

---

### Fase 4 - Clustering Comparativo

**Responsable principal:** ML Lead  
**Apoyo:** Astro Lead revisa si los grupos tienen sentido fisico.

Tareas:

- Probar K-Means con varios valores de K.
- Probar Gaussian Mixture Models con BIC.
- Probar DBSCAN para detectar outliers.
- Probar clustering jerarquico si el tiempo/memoria lo permite.
- Guardar labels por algoritmo.
- Comparar resultados con metricas.

Metricas minimas:

- Silhouette Score
- Davies-Bouldin Index
- Calinski-Harabasz Score
- BIC para GMM

Entregables:

- `notebooks/03_clustering_comparativo.ipynb`
- `notebooks/04_evaluacion_modelos.ipynb`
- `docs/model_metrics.csv`

**Checkpoint corto:** al menos tres algoritmos corren, hay tabla de metricas y se puede justificar un modelo final.

---

### Fase 5 - Seleccion del Modelo Final

**Responsables:** ML Lead + Astro Lead  
**Decision:** equipo completo.

Tareas:

- Elegir algoritmo final.
- Definir numero de clusters o parametros finales.
- Crear columna `cluster_id`.
- Exportar dataset final etiquetado.
- Verificar distribucion de clusters.

Entregables:

- `data/processed/df_labeled.csv`
- `docs/model_decision.md`

**Checkpoint corto:** cada planeta tiene `cluster_id` y la decision del modelo esta explicada con metricas y sentido fisico.

---

### Fase 6 - Interpretacion Astrofisica

**Responsable principal:** Astro Lead  
**Apoyo:** ML Lead y Data Lead.

Tareas:

- Calcular medianas por cluster:
  - radio
  - masa
  - periodo
  - temperatura
  - insolacion
- Mapear clusters a posibles tipos:
  - terrestres
  - super-Tierras
  - sub-Neptunos
  - Hot Jupiters
  - gigantes frios
  - outliers/anomalos
- Analizar sesgo por metodo de deteccion.
- Identificar candidatos habitables.
- Revisar si aparece el desierto de Neptuno.
- Agregar 2-3 referencias cientificas clave.

Entregables:

- `notebooks/05_interpretacion_astrofisica.ipynb`
- `docs/cluster_taxonomy.md`
- `docs/habitability_candidates.csv`

**Checkpoint corto:** cada cluster tiene nombre fisico, estadisticas y una explicacion defendible.

---

### Fase 7 - Visualizaciones

**Responsable principal:** Viz Lead  
**Apoyo:** todos revisan claridad.

Tareas:

- Crear graficas base en Python.
- Crear graficas finales en R solo si aporta calidad y hay tiempo.
- Exportar figuras en alta resolucion.

Graficas prioritarias:

- Masa-radio por cluster.
- UMAP/PCA por cluster.
- Periodo-radio para mostrar zonas vacias o patrones.
- Boxplots de variables por cluster.
- Mapa de habitabilidad.
- Distribucion de metodo de deteccion por cluster.

Entregables:

- `notebooks/06_visualizaciones_python.ipynb`
- `figures/*.png`
- `viz_final_r/08_visualizacion_final.Rmd` si aplica

**Checkpoint corto:** hay minimo 5 figuras claras, guardadas en `figures/`, listas para slides.

---

### Fase 8 - Presentacion

**Responsable principal:** Viz Lead  
**Apoyo:** todo el equipo.

Tareas:

- Armar presentacion de 12-16 slides.
- Repartir quien presenta cada parte.
- Ensayar con cronometro.
- Ajustar historia para 10-15 minutos.

Estructura sugerida:

1. Problema y objetivo.
2. Dataset y variables.
3. Limpieza y features.
4. Modelos comparados.
5. Modelo elegido.
6. Interpretacion de clusters.
7. Habitabilidad.
8. Hallazgos importantes.
9. Limitaciones.
10. Conclusiones.

Entregables:

- `presentation/ExoData_Challenge_2026.pptx`
- PDF de respaldo

**Checkpoint corto:** presentacion abre en otra PC, dura menos de 15 minutos y cada integrante sabe su parte.

---

### Fase 9 - Entrega Final

**Responsable:** todo el equipo, con un integrador final.

Tareas:

- Verificar que README esta actualizado.
- Verificar que los notebooks principales corren o tienen outputs confiables.
- Revisar que no se subio `.venv`.
- Hacer commit final.
- Subir tag o release si aplica.
- Guardar backup del repo y presentacion.

**Checkpoint corto:** repo limpio, presentacion lista, datos/figuras clave incluidos y backup probado.

---

## 7. Dependencias entre Integrantes

Para evitar bloqueos:

- Data Lead debe entregar `df_clean_features` antes de que ML Lead cierre clustering.
- ML Lead debe entregar `df_labeled` antes de que Astro Lead cierre interpretacion.
- Astro Lead debe entregar nombres de clusters antes de que Viz Lead cierre graficas finales.
- Viz Lead puede avanzar en plantilla, estilo y slides aunque aun no esten todos los datos finales.

Trabajo que puede hacerse en paralelo:

- Astro Lead puede investigar taxonomias y referencias desde el inicio.
- Viz Lead puede preparar estructura de slides desde el inicio.
- ML Lead puede crear funciones de clustering con un dataset de prueba.
- Data Lead puede limpiar y exportar versiones incrementales.

---

## 8. Criterios de Calidad

Antes de considerar una fase terminada:

- El notebook corre desde arriba hasta abajo o tiene instrucciones claras.
- Las rutas son relativas al proyecto, no a una PC especifica.
- El output principal se guarda en una carpeta compartida del repo.
- Las variables tienen nombres consistentes.
- Las decisiones importantes quedan documentadas.
- Los resultados tienen sentido fisico, no solo estadistico.

---

## 9. Riesgos Reales y Mitigacion

### Riesgo: conflictos en notebooks

Mitigacion:

- Un notebook por responsable.
- No editar notebooks ajenos sin avisar.
- Mover funciones reutilizables a `src/`.

### Riesgo: cada PC tiene paquetes diferentes

Mitigacion:

- Usar `requirements.txt`.
- Documentar version de Python usada.
- No subir `.venv`.

### Riesgo: dataset con shape diferente

Mitigacion:

- Documentar shape real del CSV usado.
- Guardar fecha/fuente de descarga.
- No asumir que siempre son 6,147 planetas si el archivo actual tiene otro numero.

### Riesgo: falta de tiempo para R

Mitigacion:

- Python produce todas las graficas necesarias.
- R queda como mejora estetica opcional.

### Riesgo: clustering estadisticamente bueno pero fisicamente malo

Mitigacion:

- Astro Lead revisa clusters antes de cerrar modelo.
- La decision final usa metricas y sentido fisico.

---

## 10. Checklist Final Compacto

- [ ] Todos pueden correr el entorno local.
- [x] Dataset principal carga y su shape esta documentado.
- [ ] Existe dataset procesado con features finales.
- [ ] Hay comparacion de minimo tres algoritmos.
- [ ] Hay modelo final con `cluster_id`.
- [ ] Cada cluster tiene interpretacion astrofisica.
- [ ] Hay candidatos habitables documentados.
- [ ] Hay minimo 5 figuras listas para presentacion.
- [ ] La presentacion dura menos de 15 minutos.
- [ ] README y repo estan limpios para entrega.

---

## 12. Fallas Detectadas en la Auditoria (24-abr-2026)

Prioridad alta (corregir primero):

1. El notebook `notebooks/01_ingesta_limpieza.ipynb` intenta guardar en `docs/...` y falla al ejecutarse desde la carpeta `notebooks/`; debe usar `../docs/...` o rutas construidas con `pathlib`.
2. El listado de variables criticas en el notebook no incluye `pl_insol`, pero el plan de Fase 1 si lo exige.
3. El README documenta una estructura y entregables que aun no existen (varios notebooks de fases 2-7, modulos en `src/`, `figures/`, `presentation/`, `viz_final_r/`), lo que puede confundir al equipo.

Prioridad media:

1. `src/` no tiene modulos implementados todavia, lo que dificulta reutilizar logica y evitar conflictos entre notebooks.
2. No existe aun `data/processed/` ni salidas versionadas de features/modelado.
3. La seccion "Algoritmos Implementados" en README esta adelantada respecto al estado real del repositorio.

Prioridad baja:

1. Revisar consistencia de versionado y formato en `requirements.txt` (limpiar espacios vacios finales).
2. Alinear cifra objetivo en docs (6147) con shape observado del CSV actual (6160) para evitar contradicciones en la presentacion.

---

## 11. Prioridad si Falta Tiempo

Si el equipo se queda corto de tiempo, priorizar en este orden:

1. Dataset limpio con features fisicas.
2. Un modelo final defendible.
3. Interpretacion astrofisica clara.
4. Visualizaciones principales.
5. Presentacion ensayada.
6. Mejoras esteticas en R.
7. Algoritmos extra o analisis secundarios.

La interpretacion fisica vale mas que probar demasiados modelos sin historia clara.

