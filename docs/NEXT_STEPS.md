# Hoja de ruta — Data Fútbol Lab

Este documento lista los próximos pasos recomendados, organizados por fases.
El objetivo es avanzar de forma incremental, validando en cada etapa antes de pasar a la siguiente.

---

## Fase 1 — Mejorar datos locales (CSV)

Objetivo: tener datos demo coherentes y un flujo de actualización manual claro.

- [ ] Corregir inconsistencias entre `matches.csv` y `teams.csv` (grupos de equipos)
- [ ] Ampliar `matches.csv` con los partidos completos del torneo (fase de grupos)
- [ ] Asegurar que `standings.csv` refleja los resultados de `matches.csv` de forma consistente
- [ ] Añadir columna `notes` en `matches.csv` para notas editoriales breves por partido
- [ ] Documentar el proceso manual de actualización de los CSV en `docs/DATA_UPDATE.md`
- [ ] Revisar que todos los registros tienen `source = DEMO` o `source = MANUAL` según corresponda

---

## Fase 2 — Mejorar diseño del dashboard

Objetivo: que el dashboard luzca publicable y sea fácil de leer en pantalla y en capturas.

- [ ] Corregir el subtítulo: cambiar "en tiempo real" por algo más honesto mientras los datos son manuales
- [ ] Añadir manejo de errores en la carga de datos (try/except con mensaje amigable al usuario)
- [ ] Agregar validación básica de esquema de CSV al arrancar
- [ ] Añadir una captura de pantalla del dashboard al `README.md`
- [ ] Revisar la sección "Qué mirar hoy" para que el análisis orientativo sea más rico cuando hay partidos
- [ ] Personalizar la URL de Ko-fi con la página real del proyecto
- [ ] Evaluar agregar un gráfico simple (barras de goles por grupo, por ejemplo)
- [ ] Añadir fecha y hora de última actualización visible en el dashboard

---

## Fase 3 — Preparar para GitHub ✅ COMPLETADA

Objetivo: que el repositorio sea legible y usable por cualquier persona que lo visite.

- [x] Crear el repositorio en GitHub → `https://github.com/apruiz16/data-futbol-lab`
- [x] Hacer el primer commit limpio con todos los archivos actuales
- [ ] Añadir `.github/` con un `ISSUE_TEMPLATE.md` básico (opcional pero profesional)
- [x] Revisar que no hay credenciales, datos privados ni archivos sensibles en el repo
- [ ] Añadir etiquetas al repositorio: `python`, `streamlit`, `football`, `data-analysis`
- [ ] Escribir una descripción corta del repositorio en GitHub

---

## Fase 4 — Desplegar en Streamlit Community Cloud ✅ COMPLETADA

Objetivo: tener una URL pública funcional y compartible.

- [x] Crear cuenta en [streamlit.io](https://streamlit.io) (gratuita)
- [x] Conectar el repositorio de GitHub a Streamlit Cloud
- [x] Verificar que `requirements.txt` lista exactamente las versiones correctas
- [x] Confirmar que las rutas de datos (`Path(__file__)` en `utils.py`) funcionan en el entorno cloud
- [x] Hacer el primer deploy y verificar todas las secciones en producción
- [x] Compartir la URL del dashboard como primera versión pública → [https://data-futbol-lab.streamlit.app](https://data-futbol-lab.streamlit.app)
- [x] Documentar la URL en el `README.md`

---

## Fase 5 — Evaluar fuente de datos real o semi-automatizada

Objetivo: reducir el trabajo manual de actualización y aumentar la confiabilidad de los datos.

### Opción A — API gratuita (recomendada para empezar)
- [ ] Explorar [football-data.org](https://www.football-data.org/) (tier gratuito disponible)
- [ ] Evaluar cobertura: ¿cubre el torneo objetivo? ¿con qué latencia se actualizan los datos?
- [ ] Crear un script `scripts/fetch_data.py` que descargue y transforme los datos al formato CSV existente
- [ ] Guardar la API key en `.streamlit/secrets.toml` (ya en `.gitignore`)
- [ ] Marcar los datos como `source = API` en lugar de `DEMO`

### Opción B — Actualización manual estructurada
- [ ] Crear un formulario simple en `scripts/update_match.py` para actualizar resultados por terminal
- [ ] Documentar el proceso en `docs/DATA_UPDATE.md`

### Opción C — Google Sheets como backend ligero
- [ ] Mantener los CSV en Google Sheets (edición fácil desde móvil)
- [ ] Usar `gspread` para leer las hojas directamente en Streamlit
- [ ] Requiere credenciales de Google API

---

## Fase 6 — Monetización liviana / donaciones

Objetivo: generar valor y, opcionalmente, algún ingreso mínimo sin comprometer la independencia del proyecto.

- [ ] Crear página real en [Ko-fi](https://ko-fi.com) y actualizar el botón en `app.py`
- [ ] Considerar [Buy Me a Coffee](https://www.buymeacoffee.com/) como alternativa a Ko-fi
- [ ] Evaluar generar reportes PDF por torneo o jornada (usando `reportlab` o `fpdf2`)
  - Posible producto: "Resumen de jornada PDF" para bares, restaurantes o grupos de WhatsApp
- [ ] Evaluar ofrecer el dashboard como servicio white-label para negocios locales:
  - Bares, restaurantes, grupos deportivos
  - Precio simbólico por temporada o torneo
- [ ] Si el proyecto crece, evaluar un tier de suscripción vía Substack o Patreon para análisis más detallados
- [ ] Nunca incluir: picks de apuestas, pronósticos con dinero, afiliados de casas de apuestas

---

## Criterios para considerar el proyecto "listo para mostrar"

- [x] Corre sin errores en producción (Streamlit Cloud)
- [x] Tiene URL pública compartible → [https://data-futbol-lab.streamlit.app](https://data-futbol-lab.streamlit.app)
- [ ] Los datos están actualizados (manual o automáticamente) — *pendiente: aún en modo DEMO*
- [x] El disclaimer legal es visible en todas las pantallas
- [x] No hay datos DEMO mezclados con datos reales sin indicación clara
- [x] El README explica claramente qué es, cómo usarlo y que es independiente
