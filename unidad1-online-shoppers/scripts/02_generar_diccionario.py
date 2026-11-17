#!/usr/bin/env python3
"""Genera diccionario y auditoría con trazabilidad para Unidad I."""
import csv, json, hashlib
from pathlib import Path
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
root=Path(__file__).resolve().parents[1]
raw=root/"data/raw/online_shoppers_intention.csv"
processed=root/"data/processed/online_shoppers_curado.csv"
original=list(csv.DictReader(raw.open(encoding="utf-8-sig", newline="")))
rows=list(csv.DictReader(processed.open(encoding="utf-8-sig", newline="")))
assert len(original)==len(rows)==12330 and len(original[0])==18 and len(rows[0])==25
desc={
"Administrative":"Páginas administrativas visitadas","Administrative_Duration":"Tiempo en páginas administrativas",
"Informational":"Páginas informativas visitadas","Informational_Duration":"Tiempo en páginas informativas",
"ProductRelated":"Páginas de producto visitadas","ProductRelated_Duration":"Tiempo en páginas de producto",
"BounceRates":"Tasa de rebote","ExitRates":"Tasa de salida",
"PageValues":"Valor de páginas antes de la transacción; riesgo de fuga temporal",
"SpecialDay":"Proximidad a fecha especial","Month":"Mes de la sesión",
"OperatingSystems":"Categoría codificada de sistema operativo","Browser":"Categoría codificada de navegador",
"Region":"Categoría codificada de región","TrafficType":"Tipo de tráfico codificado",
"VisitorType":"Tipo de visitante","Weekend":"Sesión en fin de semana","Revenue":"Sesión culminó en compra",
"Revenue_bin":"Indicador binario de compra derivado","total_paginas":"Suma de páginas visitadas",
"total_duracion":"Suma de tiempos de visita","duracion_por_pagina":"Duración total / páginas visitadas; cero si ninguna",
"log1p_Administrative_Duration":"log(1 + duración administrativa)",
"log1p_Informational_Duration":"log(1 + duración informativa)",
"log1p_ProductRelated_Duration":"log(1 + duración productos)"}
original_headers=list(original[0]); new_headers=list(rows[0])
assert set(new_headers)==set(desc)
w=Workbook(); s=w.active;s.title="Diccionario"
s.append(["Variable","Descripción","Tipo","Escala/unidad","Valores válidos (regla)","Fuente","Transformación"])
for k in new_headers:
    is_derived=k not in original_headers
    typ="Categórica" if k in ("Month","OperatingSystems","Browser","Region","TrafficType","VisitorType","Weekend","Revenue","Revenue_bin") else "Numérica"
    unit=("segundos" if "Duration" in k and not k.startswith("log1p") else "proporción" if k in ("BounceRates","ExitRates","SpecialDay") else "conteo" if k in ("Administrative","Informational","ProductRelated","total_paginas") else "código o etiqueta" if typ=="Categórica" else "valor derivado")
    rule="0 a 1" if k in ("BounceRates","ExitRates","SpecialDay") else "0 o 1" if k=="Revenue_bin" else "No negativo o categoría definida"
    s.append([k,desc[k],typ,unit,rule,"Derivada del dataset original" if is_derived else "UCI dataset 468", "Ver scripts/01_preparacion.R" if is_derived else "Ninguna"])
s.freeze_panes="A2";s.auto_filter.ref=s.dimensions
a=w.create_sheet("Auditoria"); dup=len(original)-len({tuple(r.values()) for r in original})
a.append(["Indicador","Valor","Interpretación"])
for val in [("Registros",len(original),"Sesiones"),("Variables originales",len(original_headers),"Sin cambios en data/raw"),("Variables curadas",len(new_headers),"Transformaciones documentadas"),("Valores faltantes",sum(sum(x=="NA" or x=="" for x in r.values()) for r in original),"No se imputan"),("Filas idénticas",dup,"Se conservan al no tener ID de sesión"),("Compras",sum(r["Revenue"].upper()=="TRUE" for r in original),"Variable respuesta"),("SHA-256 original",hashlib.sha256(raw.read_bytes()).hexdigest(),"Verificar contra archivo suministrado")]:a.append(val)
b=w.create_sheet("Decisiones");b.append(["Decisión","Justificación","Alternativa descartada","Efecto"])
for row in [
("Conservar originales","Trazabilidad","Sobrescribir datos brutos","18 columnas intactas"),
("Conservar filas idénticas","Sesiones distintas pueden compartir métricas","Eliminar por igualdad exacta","n no cambia"),
("No imputar","Ausencia de datos faltantes","Imputación innecesaria","n no cambia"),
("Crear Revenue_bin","Respuesta binaria para algoritmos","Modificar Revenue original","+1 columna"),
("Calcular totales y tiempo por página","Síntesis de intensidad de navegación","Eliminar componentes originales","+3 columnas"),
("Transformar tres duraciones con log1p","Asimetría y valores cero","Log natural sin corrección","+3 columnas"),
("PCA solo exploratorio","Redundancia entre ocho métricas","Conservar automáticamente dos PC","Modelado posterior recalcula PCA dentro de folds")
]:b.append(row)
for sh in w:
 sh.sheet_view.showGridLines=False;sh.freeze_panes="A2"
 for c in sh[1]:c.fill=PatternFill("solid",fgColor="142B55");c.font=Font(color="FFFFFF",bold=True);c.alignment=Alignment(wrap_text=True)
 for col in sh.columns:
  letter=col[0].column_letter
  sh.column_dimensions[letter].width=min(68,max(17,max(len(str(cell.value or "")) for cell in col)+3))
 for row in sh.iter_rows(min_row=2):
  for cell in row:cell.alignment=Alignment(vertical="top",wrap_text=True)
 for i in range(2,sh.max_row+1):sh.row_dimensions[i].height=31 if sh==s else 42
out=root/"docs/diccionario_datos.xlsx";out.parent.mkdir(parents=True,exist_ok=True);w.save(out)
print("Diccionario:",out,"Filas:",len(original),"Duplicadas:",dup)
