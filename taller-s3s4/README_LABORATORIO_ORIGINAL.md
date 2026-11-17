# Título de tu proyecto de investigación

**Autor/a:** Nombre y apellidos · Escuela de Posgrado, Universidad Peruana Unión
**Curso:** Ciencia de Datos e IA Aplicada

## Pregunta de investigación

Escribe aquí tu pregunta de investigación y tus hipótesis principales.

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| `analisis/` | Documentos Quarto (`.qmd`, parte 1 en R) y sus informes renderizados (`.html`) |
| `notebooks/` | Cuadernos de Google Colab (`.ipynb`, parte 2 en Python) |
| `data/raw/` | Datos originales, sin modificar (no se suben a GitHub; ver `data/raw/README.md`) |
| `data/processed/` | Datos curados y listos para modelar |
| `R/` | Funciones o scripts auxiliares |
| `extras/` | Automatización opcional con GitHub Actions |

## Cómo reproducir el análisis

1. Clona el repositorio y abre el archivo `.Rproj` en RStudio.
2. Instala los paquetes indicados en el bloque `a0-0-instalar` del documento de la parte 1.
3. Abre `analisis/S3S4_parte1.qmd` y pulsa **Render**.
4. Abre `notebooks/S3S4_parte2.ipynb` en Google Colab y ejecuta las celdas en orden.

## Automatización

- `analisis/eda_automatico.qmd`: informe exploratorio parametrizado. En la consola: `quarto::quarto_render("analisis/eda_automatico.qmd", execute_params = list(archivo = "data/processed/mi_dataset.csv", respuesta = "mi_variable"))`.
- `extras/publicar-quarto.yml`: render y publicación automáticos con GitHub Actions (opcional).

## Uso de herramientas de IA

Describe qué herramientas usaste, para qué y cómo verificaste sus resultados.
