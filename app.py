"""
Data Fútbol Lab — Dashboard principal
Proyecto independiente, informativo y sin afiliación oficial.
"""

import streamlit as st
import pandas as pd
from src.utils import (
    load_matches,
    load_teams,
    load_standings,
    get_today_matches,
    get_upcoming_matches,
    format_result,
    is_demo_data,
)
from src.standings import get_group_table, get_global_ranking, get_classification_scenarios

# ─── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Fútbol Lab",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Estilos personalizados ────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1a1a2e;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        margin-top: 0.2rem;
    }
    .demo-badge {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 6px;
        padding: 8px 14px;
        font-size: 0.85rem;
        color: #856404;
    }
    .disclaimer {
        background: #f8f9fa;
        border-left: 4px solid #6c757d;
        border-radius: 4px;
        padding: 12px 16px;
        font-size: 0.82rem;
        color: #555;
        margin-top: 1rem;
    }
    .match-card {
        background: #f0f4ff;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-left: 4px solid #4361ee;
    }
    .match-result {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1a1a2e;
        border-bottom: 2px solid #4361ee;
        padding-bottom: 4px;
        margin-bottom: 12px;
    }
    .donate-box {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        border-radius: 10px;
        padding: 18px 24px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ─── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_all_data():
    matches = load_matches()
    teams = load_teams()
    standings = load_standings()
    return matches, teams, standings

matches, teams, standings = load_all_data()

demo_mode = is_demo_data(matches)
today_matches = get_today_matches(matches)
upcoming_matches = get_upcoming_matches(matches, days_ahead=7)
groups = sorted(standings["group"].unique())

# ─── Encabezado ────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">⚽ Data Fútbol Lab</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Análisis independiente de fútbol internacional · '
    'Tablas, partidos y escenarios en tiempo real</p>',
    unsafe_allow_html=True
)

if demo_mode:
    st.markdown(
        '<div class="demo-badge">⚠️ <strong>Modo DEMO</strong> — '
        'Los datos mostrados son ficticios y se usan solo para pruebas. '
        'No representan resultados oficiales.</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ─── Sección 1: Partidos de hoy ────────────────────────────────────────────────
st.markdown('<p class="section-header">📅 Partidos de hoy</p>', unsafe_allow_html=True)

if today_matches.empty:
    st.info("No hay partidos registrados para hoy.")
else:
    cols = st.columns(min(len(today_matches), 3))
    for idx, (_, row) in enumerate(today_matches.iterrows()):
        col = cols[idx % len(cols)]
        result = format_result(row)
        with col:
            st.markdown(f"""
            <div class="match-card">
                <div style="font-size:0.78rem; color:#888;">Grupo {row['group']} · {row['time']} hs</div>
                <div class="match-result">{row['home_team']} vs {row['away_team']}</div>
                <div style="font-size:1rem; color:#4361ee; font-weight:600;">{result}</div>
                <div style="font-size:0.75rem; color:#aaa; margin-top:4px;">{row['venue']}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Sección 2: Próximos partidos ──────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">🗓️ Próximos partidos</p>', unsafe_allow_html=True)

if upcoming_matches.empty:
    st.info("No hay próximos partidos cargados.")
else:
    display_upcoming = upcoming_matches.copy()
    display_upcoming["Fecha"] = display_upcoming["date"].dt.strftime("%d/%m")
    display_upcoming["Hora"] = display_upcoming["time"]
    display_upcoming["Partido"] = (
        display_upcoming["home_team"] + " vs " + display_upcoming["away_team"]
    )
    display_upcoming["Grupo"] = display_upcoming["group"]
    display_upcoming["Sede"] = display_upcoming["venue"]
    st.dataframe(
        display_upcoming[["Fecha", "Hora", "Partido", "Grupo", "Sede"]],
        use_container_width=True,
        hide_index=True,
    )

# ─── Sección 3: Tabla de grupos ────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">📊 Tablas de grupos</p>', unsafe_allow_html=True)

tab_labels = [f"Grupo {g}" for g in groups]
tabs = st.tabs(tab_labels)

for tab, group in zip(tabs, groups):
    with tab:
        group_df = get_group_table(standings, group)
        st.dataframe(group_df, use_container_width=True)

        st.markdown("##### Escenarios de clasificación")
        scenarios = get_classification_scenarios(standings, group)
        scenario_df = pd.DataFrame(scenarios)
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)

# ─── Sección 4: Ranking global ─────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">🏆 Ranking de selecciones (FIFA)</p>', unsafe_allow_html=True)

ranking = get_global_ranking(teams, n=16)
st.dataframe(ranking, use_container_width=True)
st.caption("Fuente: ranking FIFA de referencia. Datos DEMO — no representan el ranking oficial actual.")

# ─── Sección 5: Qué mirar hoy ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-header">🔭 Qué mirar hoy</p>', unsafe_allow_html=True)

if today_matches.empty:
    st.write("Sin partidos hoy. Revisa la sección de próximos partidos.")
else:
    for _, row in today_matches.iterrows():
        with st.expander(f"🔍 {row['home_team']} vs {row['away_team']} — Análisis breve"):
            st.markdown(f"""
**Grupo {row['group']} · {row['time']} hs · {row['venue']}**

- **Contexto:** Partido de fase de grupos en etapa temprana del torneo.
- **Puntos clave a observar:** Sistema táctico, rotaciones y estado físico de los equipos.
- **Factor a seguir:** Rendimiento en las primeras transiciones y control del mediocampo.

> ⚠️ *Este análisis es orientativo y de elaboración propia. No constituye predicción ni recomendación de apuestas.*
""")

# ─── Sección 6: Donación ───────────────────────────────────────────────────────
st.markdown("---")
col_donate, col_spacer = st.columns([2, 3])
with col_donate:
    st.markdown("""
    <div class="donate-box">
        <div style="font-size:1.3rem; font-weight:700; margin-bottom:6px;">☕ Apoya el proyecto</div>
        <div style="font-size:0.9rem; margin-bottom:14px;">
            Si te resulta útil, puedes invitarme un café.<br>
            Cada aporte ayuda a mantener el análisis actualizado.
        </div>
        <a href="https://ko-fi.com" target="_blank"
           style="background:white; color:#3a0ca3; padding:8px 20px;
                  border-radius:20px; font-weight:700; text-decoration:none;">
            ☕ Donar en Ko-fi
        </a>
    </div>
    """, unsafe_allow_html=True)

# ─── Disclaimer ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Aviso legal:</strong> Data Fútbol Lab es un proyecto independiente, 
    informativo y no afiliado a ninguna organización oficial de fútbol. 
    Los datos mostrados son de carácter informativo y, cuando están marcados como DEMO, 
    son ficticios y solo se usan para pruebas. No se realizan predicciones de apuestas 
    ni recomendaciones de ningún tipo. Todos los logos, marcas y nombres de equipos 
    son propiedad de sus respectivos dueños y se mencionan con fines informativos únicamente.
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center; color:#aaa; font-size:0.78rem; margin-top:8px;'>"
    "Data Fútbol Lab · Hecho con ❤️ y Python · v0.1 DEMO"
    "</div>",
    unsafe_allow_html=True
)
