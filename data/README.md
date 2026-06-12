# Datos — Data Fútbol Lab

Esta carpeta contiene los archivos CSV que alimentan el dashboard.

> ⚠️ **Estado actual: DEMO** — todos los datos son ficticios y se usan solo para pruebas.

---

## Archivos

| Archivo | Descripción | Columnas clave |
|---|---|---|
| `matches.csv` | Partidos del torneo (resultados y programados) | `match_id`, `date`, `status`, `data_status` |
| `teams.csv` | Selecciones participantes con ranking | `team_id`, `team_name`, `group`, `data_status` |
| `standings.csv` | Tabla de posiciones por grupo | `group`, `team_name`, `points`, `data_status` |
| `sources.csv` | Registro de fuentes utilizadas | `source_id`, `source_name`, `source_url` |

---

## Columnas de trazabilidad (en todos los archivos)

| Columna | Valores válidos | Descripción |
|---|---|---|
| `data_status` | `demo` / `verified` / `pending` | Calidad del dato. `demo` = ficticio. `verified` = verificado manualmente. `pending` = dato ingresado pero sin verificar aún. |
| `source_name` | Texto libre | Nombre de la fuente. Ej: `FIFA Official`, `ESPN`, `Manual` |
| `source_url` | URL o vacío | URL donde se verificó el dato |
| `last_updated` | `YYYY-MM-DD` | Fecha de última actualización del registro |
| `notes` | Texto libre o vacío | Notas editoriales. Ej: "pendiente confirmar sede" |

---

## Flujo de actualización manual

Ver guía completa en `docs/DATA_UPDATE_GUIDE.md`.

**Resumen del proceso:**

1. Editar el CSV correspondiente en un editor de texto o Excel/Google Sheets
2. Cambiar `data_status` de `demo` → `verified` en los registros actualizados
3. Completar `source_name`, `source_url` y `last_updated`
4. Registrar la fuente en `sources.csv` si es nueva
5. Correr `python scripts/validate_data.py` para verificar integridad
6. Correr `streamlit run app.py` y revisar el dashboard localmente
7. Hacer `git add data/ && git commit -m "Update match results YYYY-MM-DD"` y `git push`
8. Streamlit Cloud se actualiza automáticamente con el push

---

## Valores válidos para `status` en `matches.csv`

| Valor | Significado |
|---|---|
| `Programado` | Partido aún no jugado |
| `En juego` | Partido en curso (actualización en tiempo real — no aplica en modo CSV) |
| `Finalizado` | Resultado definitivo |
| `Suspendido` | Partido suspendido |
| `Aplazado` | Partido reprogramado |
