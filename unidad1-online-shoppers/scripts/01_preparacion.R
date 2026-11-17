# Script reproducible - UPeU Unidad I - Requiere R >= 4.1 (solo base R)
# Ejecutar desde la raiz del proyecto: Rscript scripts/01_preparacion.R
options(stringsAsFactors = FALSE)
raw_path <- file.path('data','raw','online_shoppers_intention.csv')
out_path <- file.path('data','processed','online_shoppers_curado.csv')
if (!file.exists(raw_path)) stop('Ejecute desde la raiz del proyecto.')
d <- read.csv(raw_path, check.names = FALSE, stringsAsFactors = FALSE)
stopifnot(ncol(d)==18L, all(c('Revenue','ProductRelated','ExitRates') %in% names(d)))
stopifnot(all(complete.cases(d)), all(d$Revenue %in% c(TRUE,FALSE)))
# Las 125 coincidencias exactas NO se eliminan: no existe identificador de sesion.
d$Revenue_bin <- as.integer(d$Revenue)
d$total_paginas <- d$Administrative + d$Informational + d$ProductRelated
d$total_duracion <- d$Administrative_Duration + d$Informational_Duration + d$ProductRelated_Duration
d$duracion_por_pagina <- ifelse(d$total_paginas > 0, d$total_duracion / d$total_paginas, 0)
for (nm in c('Administrative_Duration','Informational_Duration','ProductRelated_Duration')) {
  d[[paste0('log1p_',nm)]] <- log1p(d[[nm]])
}
dir.create(dirname(out_path), showWarnings=FALSE, recursive=TRUE)
write.csv(d, out_path, row.names=FALSE, na='')
cat('Filas:',nrow(d),' Columnas:',ncol(d),' Nulos:',sum(is.na(d)),'\n')
cat('La base original permanece intacta. Archivo:',out_path,'\n')
