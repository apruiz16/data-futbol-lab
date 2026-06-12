# Guía de actualización manual de datos — Data Fútbol Lab

Esta guía explica cómo reemplazar datos DEMO por datos reales verificados,
paso a paso, sin escribir código.

> **Regla fundamental:** nunca marques un dato como `verified` si no puedes
> respaldar su fuente. Si no estás seguro, usa `pending`.

---

## Estructura de carpeta `data/`

```
data/
├── matches.csv      ← Partidos (resultados + programados)
├── teams.csv        ← Selecciones participantes
├── standings.csv    ← Tabla de posiciones por grupo
├── sources.csv      ← Registro de fuentes utilizadas
└── README.md        ← Descripción de columnas
```

---

## Columnas de trazabilidad (obligatorias en todo registro)

| Columna | Valores válidos | Qué poner |
|---|---|---|
| `data_status` | `demo` / `verified` / `pending` | `demo` si es ficticio. `verified` si lo verificaste tú en una fuente. `pending` si lo ingresaste pero falta confirmar. |
| `source_name` | Texto libre | Nombre de la fuente. Ej: `FIFA.com`, `ESPN`, `Transfermarkt`, `Manual` |
| `source_url` | URL o vacío | URL exacta donde verificaste el dato. Puede quedar vacío. |
| `last_updated` | `YYYY-MM-DD` | Fecha en que actualizaste el registro. Ej: `2026-06-15` |
| `notes` | Texto libre o vacío | Cualquier aclaración. Ej: `"Resultado confirmado en diferido"` |

---

## Cómo actualizar resultados de partidos (`matches.csv`)

### Columnas obligatorias

```
match_id, date, time, home_team, away_team, group, stage, venue, status, data_status
```

### Columnas de resultado (solo en partidos finalizados)

```
home_score, away_score
```

### Pasos

1. Abre `data/matches.csv` en tu editor preferido (VS Code, Excel, Google Sheets)
2. Busca el partido por `match_id` o por `home_team` + `away_team`
3. Completa o corrige estos campos:
   - `home_score` y `away_score` → enteros (Ej: `2`, `1`)
   - `status` → cambia `Programado` a `Finalizado`
   - `data_status` → cambia `demo` a `verified`
   - `source_name` → nombre de la fuente (Ej: `FIFA.com`)
   - `source_url` → URL donde verificaste (puede quedar vacío)
   - `last_updated` → fecha de hoy (`YYYY-MM-DD`)
4. Guarda el archivo

### Ejemplo de fila antes y después

**Antes (demo):**
```
3,2026-06-12,21:00,Francia,Alemania,,,C,Grupo,AT&T Stadium,Programado,demo,Demo,,2026-06-12,
```

**Después (verificado):**
```
3,2026-06-12,21:00,Francia,Alemania,2,0,C,Grupo,AT&T Stadium,Finalizado,verified,FIFA.com,https://fifa.com/...,2026-06-12,Resultado final
```

---

## Cómo actualizar la tabla de posiciones (`standings.csv`)

### Columnas obligatorias

```
group, position, team_name, flag_emoji, played, won, drawn, lost,
goals_for, goals_against, goal_diff, points, data_status
```

### Pasos

1. Abre `data/standings.csv`
2. Actualiza las filas del grupo que cambió
3. Recalcula manualmente:
   - `played` = partidos jugados
   - `won` / `drawn` / `lost` = resultados
   - `goals_for` / `goals_against` = goles acumulados
   - `goal_diff` = `goals_for` - `goals_against`
   - `points` = (`won` × 3) + (`drawn` × 1)
4. Reordena las filas del grupo por `points` → `goal_diff` → `goals_for` (mayor a menor)
5. Actualiza `position` (1, 2, 3, 4)
6. Cambia `data_status` a `verified` en las filas actualizadas

---

## Cómo actualizar selecciones (`teams.csv`)

Úsalo principalmente para actualizar el **ranking FIFA** cuando cambien posiciones.

### Columnas obligatorias

```
team_id, team_name, confederation, fifa_ranking, group, flag_emoji, data_status
```

### Pasos

1. Abre `data/teams.csv`
2. Actualiza `fifa_ranking` con el valor oficial más reciente
3. Cambia `data_status` a `verified`
4. Registra la fuente en `source_name` (Ej: `FIFA Rankings Agosto 2026`)

---

## Cómo registrar una fuente nueva (`sources.csv`)

Cada vez que uses una fuente nueva, agrégala aquí.

### Estructura

```
source_id, source_name, source_url, data_type, description, verified_by, date_added, notes
```

### Ejemplo

```
FIFA_OFFICIAL,FIFA.com,https://fifa.com,matches,Sitio oficial de resultados FIFA,Alex R.,2026-06-15,
```

---

## Cómo validar que no rompiste la app

### Opción 1 — Validación visual rápida (recomendada)

```bash
streamlit run app.py
```

Revisa:
- [ ] El banner superior cambió de amarillo (DEMO) a naranja (mixto) o verde (todo verificado)
- [ ] Las tablas de grupos muestran los datos nuevos
- [ ] No hay mensajes de error en la pantalla
- [ ] Los partidos de hoy aparecen si corresponde

Si hay advertencias de esquema, aparecerán en la barra lateral izquierda.

### Opción 2 — Validación por Python

```bash
cd data-futbol-lab
source venv/bin/activate
python -c "
from src.utils import load_matches, load_teams, load_standings, validate_all_csvs
m, t, s = load_matches(), load_teams(), load_standings()
issues = validate_all_csvs(m, t, s)
if issues:
    for i in issues: print('⚠️', i)
else:
    print('✅ Sin problemas detectados')
"
```

---

## Cómo publicar los cambios (push a GitHub → Streamlit Cloud)

```bash
git status
git add data/
git commit -m "Update match results YYYY-MM-DD — source: NOMBRE_FUENTE"
git push
```

Streamlit Cloud detecta el push automáticamente y re-deploya en ~30 segundos.

---

## Errores comunes y cómo resolverlos

| Error en la app | Causa probable | Solución |
|---|---|---|
| `KeyError: 'group'` | Columna `group` eliminada o renombrada | Verificar que el CSV tiene la columna exactamente como `group` |
| Tab de grupo vacía | Valor en `group` tiene espacio extra (`" C"`) | Revisar y eliminar espacios con `str.strip()` o editar manualmente |
| `ValueError: invalid literal for int()` | Score con texto en lugar de número | Los campos `home_score` / `away_score` deben ser enteros o estar vacíos |
| Partido no aparece en "hoy" | Fecha en formato incorrecto | Usar formato `YYYY-MM-DD` exactamente. Ej: `2026-06-15` |
| Banner sigue amarillo después de verificar | El caché de Streamlit no se actualizó | Ir a menú ☰ → "Clear cache" y recargar |

---

## Buenas prácticas

- **Un commit por jornada:** agrupa todas las actualizaciones de una fecha en un solo commit
- **Mensaje descriptivo:** `Update results matchday 3 — source: FIFA.com 2026-06-20`
- **Nunca mezcles datos sin marcarlos:** si un partido es verificado y otro sigue siendo demo, el dashboard lo indica en naranja
- **Siempre registra la fuente:** aunque sea solo `Manual` o `ESPN`
- **No inventes datos:** si no tienes el resultado, deja `status = Programado` y `data_status = pending`
