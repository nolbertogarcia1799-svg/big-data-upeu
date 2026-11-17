# Taller de automatización del análisis — Sesiones 3 y 4

**Asignatura:** Ciencia de Datos e IA Aplicada — UPeU  
**Autor:** Nolberto García Valdez  
**Modalidad:** Desarrollo individual; se ejecutaron y verificaron las tareas de los tres roles.  
**Datos:** Breast Cancer Wisconsin (Diagnostic), `wdbc_limpio.csv` del proyecto de clase.

**Alcance metodológico:** El ZIP proporcionado contiene el archivo R `eda_automatico.qmd` y el CSV oficial, pero no el cuaderno Python B6 ni las salidas de B2/B3. Por tanto, la comparación predictiva siguiente es una **implementación alternativa reproducible**, no una ejecución de la función original `analisis_automatico`. Las actividades 2 y 4 reutilizan los datos de clase, alternativa admitida por la guía en ausencia de un segundo CSV.

## Actividad 1. EDA automático — datos de clase

### 1.1. Estructura y calidad
Se analizaron **569 casos, 32 columnas en el archivo** (`id`, `diagnosis` y **30 predictoras numéricas**). Una vez excluido `id`, el análisis incluye 31 columnas, contando la respuesta. No existen valores faltantes ni filas duplicadas.

### 1.2. Distribución y desbalance
Se registran **357 benignos (62,74 %) y 212 malignos (37,26 %)**. El informe activa alerta cuando la clase minoritaria es menor que el **30 %**, umbral no alcanzado: no corresponde emitir alerta de desbalance. La estratificación y la sensibilidad para malignos siguen siendo relevantes.

### 1.3. Variables con mayor diferenciación
Por d de Cohen, con el grupo maligno menos el benigno, destacan `concave_points_worst` (**2,693**), `perimeter_worst` (**2,598**) y `concave_points_mean` (**2,545**). El material de parte 1 menciona `concave_points_mean` entre las variables destacadas esperadas por Boruta, pero no conserva su salida real; la coincidencia con Boruta **no se pudo verificar de forma completa**.

### 1.4. Dos alertas y resolución
- **Asimetría:** `area_se` alcanza asimetría próxima a **5,43**, superior al criterio absoluto de 1. Se considera log1p para valores no negativos o Yeo–Johnson, ajustando la transformación solo en el entrenamiento; no se eliminan casos extremos sin justificación.
- **Redundancia:** `radius_mean` y `perimeter_mean` alcanzan correlación aproximadamente **0,998**, superior a 0,90. Un filtro de correlaciones o PCA dentro de validación cruzada ayuda a evitar redundancia sin contaminar la estimación.

## Actividad 2. EDA con dataset seleccionado

### 2.1. Descripción
Se reutilizó `wdbc_limpio.csv`: **569 casos; 30 predictoras numéricas, respuesta categórica binaria `diagnosis` con valores Benigno y Maligno**. Se excluye `id` del modelado.

### 2.2. Alertas prioritarias
Hay numerosas alertas de asimetría y **21 pares con correlación absoluta superior a 0,90**. La redundancia se prioriza por su efecto sobre estabilidad e interpretación. Se plantea selección integrada al entrenamiento y comparación con regularización, evitando decidir el filtrado con el conjunto completo.

### 2.3. Propuesta crítica
**Propuesta evaluada:** descartar todas las variables con |r| superior a 0,90 y transformar automáticamente todas las variables asimétricas. **Decisión: MODIFICAR.** Las correlaciones y asimetrías justifican examinar tratamientos, no la supresión indiscriminada de indicadores potencialmente relevantes. Cada tratamiento deberá formar parte de los pliegues de validación. Esta observación se contrastó con el contenido y los umbrales de `eda_automatico.qmd` y con el CSV.

## Actividad 3. Comparación automática de modelos — datos de clase

**Evaluación alternativa reproducible:** partición estratificada entrenamiento/prueba **426/143**, semilla **42**, cinco pliegues estratificados sobre entrenamiento. La clase positiva es Maligno y la métrica principal es **AUC ROC**. Elastic Net usa estandarización dentro del pipeline.

| Modelo | AUC CV | AUC prueba | Sensibilidad (maligno) |
|:--|--:|--:|--:|
| LightGBM | 0,9921 | 0,9958 | 0,8868 |
| Elastic Net | 0,9910 | 0,9975 | 0,9245 |
| XGBoost | 0,9909 | 0,9952 | 0,9057 |
| Random Forest | 0,9872 | 0,9960 | 0,9057 |

### 3.1. Recomendación y criterio
LightGBM logra el AUC CV más alto (**0,9921**). Si se aplica el criterio de parsimonia de elegir Elastic Net cuando su AUC queda a menos de 0,005 del mejor, se selecciona **Elastic Net** (AUC CV **0,9910**). Esta decisión es del procedimiento alternativo, no una salida verificada de B6.

### 3.2. Comparación con B2/B3
No existe un registro comprobable de las métricas previas B2/B3 en el ZIP. Con el mismo algoritmo, preprocesamiento, semilla y partición deben obtenerse resultados iguales o muy próximos; **no se afirma haber comprobado esa coincidencia**.

### 3.3. Elección médica para ΔAUC inferior a 0,005
Se preferiría el modelo interpretable y parsimonioso, sin sacrificar la sensibilidad a malignos, y con evaluación clínica de errores y calibración. En esta partición, Elastic Net presenta sensibilidad **0,9245**, frente a **0,8868** de LightGBM. Es una comparación exploratoria, no validación clínica.

## Actividad 4. Comparación con el dataset elegido

### 4.1. Tipo, métrica y recomendación
Es **clasificación binaria**. Se utilizó AUC ROC; el modelo elegido por la regla de parsimonia alternativa fue **Elastic Net**. Como se empleó exactamente el mismo CSV de clase y configuración, los archivos `comparacion_caso_clase.csv` y `comparacion_mi_dataset.csv` son iguales. No son dos muestras independientes.

### 4.2. Validación cruzada frente a prueba
Las diferencias absolutas entre AUC de prueba y media CV fueron entre **0,0037 y 0,0088**, todas favorables a prueba. No se aprecia degradación evidente en esta partición, pero una sola división no descarta sobreajuste; hacen falta sensibilidad, calibración e intervalos de confianza.

### 4.3. Decisión automática
La división **75/25 estratificada** conserva aproximadamente las proporciones de Benigno y Maligno y es adecuada para clasificación; los escaladores de Elastic Net fueron aprendidos únicamente dentro de cada fold. Se excluyó `id` para evitar utilizar un identificador ajeno al fenómeno clínico.

## Conclusión
El CSV tiene completitud alta, sin duplicados, pero presenta multicolinealidad considerable. Los cuatro modelos lograron buena discriminación, con diferencias pequeñas de AUC. La sensibilidad clínica y la parsimonia importan junto al rendimiento agregado. Las evaluaciones B6 y Boruta **requieren aún el cuaderno y los resultados originales** para ser declaradas reproducciones exactas.

**Material fuente:** `s3s4-laboratorio-main.zip` y `TALLER CLASES.pdf` proporcionados en el curso.
