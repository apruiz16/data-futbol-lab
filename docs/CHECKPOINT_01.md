# Checkpoint 01 — Data Fútbol Lab v0.1 DEMO

**Fecha:** 2026-06-12  
**Estado:** Funcional en local · No desplegado · Datos 100% ficticios (DEMO)  
**Versión:** 0.1

---

## Resumen del estado actual

El proyecto corre correctamente con `streamlit run app.py` desde la raíz.
Todas las secciones del dashboard se renderizan sin errores.
Los datos son completamente ficticios y están marcados como `DEMO` tanto en los CSV (columna `source`) como en el banner del dashboard.

---

## Estructura del proyecto

```
data-futbol-lab/
├── data/
│   ├── matches.csv       # 10 partidos de ejemplo (DEMO)
│   ├── teams.csv         # 32 selecciones con ranking y grupo (DEMO)
│   └── standings.csv     # Posiciones de 8 grupos (DEMO)
├── src/
│   ├── __init__.py
│   ├── utils.py          # Carga de CSV, filtros de fecha, detección DEMO
│   └── standings.py      # Tablas de grupo, ranking global, escenarios
├── docs/
│   ├── CHECKPOINT_01.md  # Este archivo
│   └── NEXT_STEPS.md     # Hoja de ruta
├── app.py                # Dashboard principal (Streamlit)
├── requirements.txt      # streamlit + pandas únicamente
├── .gitignore
└── README.md
```

---

## Secciones del dashboard (v0.1)

| Sección | Estado | Notas |
|---|---|---|
| Banner DEMO | ✅ Funciona | Se activa automáticamente si `source == DEMO` en todos los registros |
| Encabezado y descripción | ✅ Funciona | Texto independiente, sin afiliación |
| Partidos de hoy | ✅ Funciona | Filtra por fecha del sistema. Muestra cards con resultado o estado |
| Próximos partidos | ✅ Funciona | Tabla con hasta 7 días adelante de partidos `Programado` |
| Tablas de grupos | ✅ Funciona | 8 tabs navegables, ordenados por pts/DG/GF |
| Escenarios de clasificación | ✅ Funciona | Lógica simple: pos 1-2 clasifican, pos 3 posible tercer mejor, pos 4 necesita ayuda |
| Ranking FIFA | ✅ Funciona | Top 16 selecciones por ranking demo |
| Qué mirar hoy | ✅ Funciona | Expander por partido con análisis orientativo. Aviso de no-apuestas incluido |
| Donación | ✅ Funciona | Botón Ko-fi (URL genérica — pendiente personalizar) |
| Disclaimer legal | ✅ Funciona | Al pie de página, cubre no-afiliación y no-apuestas |

---

## Estado de los datos demo

| Archivo | Registros | Fuente | Notas |
|---|---|---|---|
| `matches.csv` | 10 partidos | DEMO | Fechas centradas en 2026-06-12 al 2026-06-15 |
| `teams.csv` | 32 selecciones | DEMO | Rankings ficticios, grupos asignados manualmente |
| `standings.csv` | 32 filas (8 grupos × 4) | DEMO | Solo Grupo A y B tienen datos parciales jugados |

Todos los CSV tienen columna `source = DEMO`. La función `is_demo_data()` en `utils.py` detecta esto y activa el banner automáticamente.

---

## Cómo correr el proyecto localmente

```bash
# Requiere Python 3.11+
python -m venv venv
source venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
```

Abre: [http://localhost:8501](http://localhost:8501)

---

## Correcciones aplicadas en este checkpoint

| # | Problema | Severidad | Acción |
|---|---|---|---|
| 1 | `matches.csv` línea 4: grupo era `" C"` (con espacio) en vez de `"C"` | **Alta** — rompía la tab Grupo C | Corregido |
| 2 | `standings.py` importaba `load_standings` y `load_teams` sin usarlos | Baja — imports muertos | Eliminados |
| 3 | `README.md` no incluía `__init__.py` ni carpeta `docs/` en el árbol | Cosmético | Actualizado |

---

## Riesgos y puntos débiles documentados

### 1. Inconsistencia entre matches.csv y teams.csv (DEMO)
Algunos partidos en `matches.csv` asignan equipos a grupos que no coinciden con su grupo en `teams.csv`.  
Ejemplo: Colombia aparece en Grupo G en `matches.csv` pero en Grupo F en `teams.csv`.  
**Impacto:** Ninguno en DEMO — no afecta la lógica actual ya que la tabla de posiciones se carga independientemente de los partidos. Al conectar datos reales, esto debe resolverse.

### 2. Ko-fi URL genérica
El botón de donación apunta a `https://ko-fi.com` en lugar de la página personal del proyecto.  
**Acción necesaria:** Actualizar la URL cuando se cree la página Ko-fi del proyecto.

### 3. Sin validación de esquema de CSV
Si se modifica un CSV y falta una columna, la app lanza un `KeyError` sin mensaje útil al usuario.  
**Riesgo:** Bajo mientras los datos sean manuales. A resolver antes de conectar fuentes externas.

### 4. `@st.cache_data(ttl=300)` en modo local
El caché de 5 minutos es apropiado para producción pero puede confundir durante desarrollo si se modifican los CSV y los cambios no se ven reflejados.  
**Workaround:** Usar `streamlit run app.py --server.runOnSave true` o hacer "Clear cache" desde el menú de Streamlit.

### 5. Sin manejo de errores en carga de datos
Si un CSV no existe o está malformado, la app falla al arrancar sin mensaje descriptivo.  
**A resolver en Fase 2** antes de desplegar.

### 6. Subtitle dice "en tiempo real"
El subtítulo del header dice "Tablas, partidos y escenarios en tiempo real" pero los datos son DEMO y estáticos.  
**Riesgo:** Bajo, ya que el banner DEMO es visible. Corregir el texto cuando se conecten datos reales.

---

## No se tocó

- Arquitectura de módulos (`src/`)
- Lógica de Streamlit en `app.py`
- Diseño visual (CSS embebido)
- Datos demo (solo se corrigió el espacio en el grupo " C")
- `requirements.txt` — ya estaba mínimo y correcto
- `.gitignore` — correcto y suficiente para esta etapa

---

## ¿Listo para subir a GitHub?

**Casi.** Antes de hacer el primer `git push`:

1. Confirmar que `.gitignore` incluye `venv/` (ya lo hace ✅)
2. Personalizar la URL de Ko-fi en `app.py`
3. Opcional: agregar una imagen de preview del dashboard al README
4. Crear el repositorio en GitHub y hacer el primer commit

Ver `NEXT_STEPS.md` para la hoja de ruta completa.
