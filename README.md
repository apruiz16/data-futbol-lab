# ⚽ Data Fútbol Lab

> **Proyecto en modo DEMO** — los datos actuales son ficticios y se usan solo para pruebas. No representan resultados reales ni oficiales.

Dashboard independiente de análisis de fútbol internacional, construido con Python y Streamlit.
Ofrece tablas de grupos, resultados del día, próximos partidos, ranking de selecciones y escenarios de clasificación.

**Este proyecto es independiente y no está afiliado a ninguna organización oficial de fútbol.**

---

## Stack tecnológico

- **Python 3.11+**
- **pandas** — procesamiento de datos
- **Streamlit** — interfaz web
- **CSV** — almacenamiento de datos (fase inicial)

---

## Estructura del proyecto

```
data-futbol-lab/
├── data/
│   ├── matches.csv       # Partidos: resultados y programados (DEMO)
│   ├── teams.csv         # Selecciones participantes (DEMO)
│   └── standings.csv     # Tabla de posiciones por grupo (DEMO)
├── src/
│   ├── __init__.py
│   ├── utils.py          # Carga y transformación de datos
│   └── standings.py      # Lógica de tablas, ranking y escenarios
├── docs/
│   ├── CHECKPOINT_01.md  # Estado del proyecto en v0.1
│   └── NEXT_STEPS.md     # Hoja de ruta por fases
├── app.py                # Dashboard principal (Streamlit)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Cómo correr el proyecto localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/data-futbol-lab.git
cd data-futbol-lab

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # Mac / Linux
# venv\Scripts\activate       # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Lanzar el dashboard
streamlit run app.py
```

Abre tu navegador en [http://localhost:8501](http://localhost:8501).

---

## Qué incluye el dashboard (v0.1 DEMO)

| Sección | Descripción |
|---|---|
| Banner DEMO | Aviso visible cuando los datos son ficticios |
| Partidos de hoy | Cards con resultado o estado |
| Próximos partidos | Tabla con fecha, hora, grupo y sede |
| Tablas de grupos | 8 tabs navegables con posiciones |
| Escenarios de clasificación | Estado estimado por equipo |
| Ranking FIFA | Top 16 selecciones del torneo |
| Qué mirar hoy | Análisis breve por partido |
| Donación | Botón Ko-fi |
| Disclaimer | Aviso legal al pie de página |

---

## Aviso legal

Data Fútbol Lab es un proyecto **independiente e informativo**, no afiliado a ninguna organización oficial de fútbol (FIFA, UEFA, CONMEBOL ni otras). No se realizan predicciones, picks ni recomendaciones de apuestas de ningún tipo. Los nombres de equipos y selecciones se usan con fines informativos únicamente.
