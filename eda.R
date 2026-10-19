
# EDA basico
library(tidyverse)

# 1. Estructura y resumen
glimpse(datos)
summary(datos)

# 2. Valores faltantes
colSums(is.na(datos))

# 3. Estadisticas principales
datos %>%
  summarise(
    vehiculos_min = min(vehiculos),
    vehiculos_max = max(vehiculos),
    vehiculos_media = mean(vehiculos),
    velocidad_min = min(velocidad_kmh),
    velocidad_max = max(velocidad_kmh),
    velocidad_media = mean(velocidad_kmh)
  )

# 4. Trafico por hora
datos %>%
  group_by(hora) %>%
  summarise(
    vehiculos = mean(vehiculos),
    velocidad = mean(velocidad_kmh),
    .groups = "drop"
  )

# 5. Nivel de congestion
datos %>%
  count(congestion)

# 6. Registros por punto
datos %>%
  count(punto)
