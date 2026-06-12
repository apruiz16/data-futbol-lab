"""
Lógica de tablas de posiciones y ranking para Data Fútbol Lab.
"""

import pandas as pd


def get_group_table(standings: pd.DataFrame, group: str) -> pd.DataFrame:
    """Filtra y formatea la tabla de posiciones de un grupo específico."""
    df = standings[standings["group"] == group].copy()
    df = df.sort_values(["points", "goal_diff", "goals_for"], ascending=False)
    df = df.reset_index(drop=True)
    df.index += 1

    display_cols = [
        "flag_emoji", "team_name", "played", "won", "drawn",
        "lost", "goals_for", "goals_against", "goal_diff", "points"
    ]
    rename_map = {
        "flag_emoji": "",
        "team_name": "Selección",
        "played": "PJ",
        "won": "PG",
        "drawn": "PE",
        "lost": "PP",
        "goals_for": "GF",
        "goals_against": "GC",
        "goal_diff": "DG",
        "points": "Pts"
    }
    return df[display_cols].rename(columns=rename_map)


def get_global_ranking(teams: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Devuelve el ranking FIFA de las selecciones participantes."""
    df = teams[["flag_emoji", "team_name", "confederation", "fifa_ranking", "group"]].copy()
    df = df.drop_duplicates(subset="team_name")
    df = df.sort_values("fifa_ranking").head(n).reset_index(drop=True)
    df.index += 1
    rename_map = {
        "flag_emoji": "",
        "team_name": "Selección",
        "confederation": "Confederación",
        "fifa_ranking": "Ranking FIFA",
        "group": "Grupo"
    }
    return df.rename(columns=rename_map)


def get_classification_scenarios(standings: pd.DataFrame, group: str) -> list[dict]:
    """
    Genera escenarios simples de clasificación para un grupo.
    Solo funciona cuando hay partidos ya jugados.
    """
    df = standings[standings["group"] == group].copy()
    df = df.sort_values(["points", "goal_diff", "goals_for"], ascending=False).reset_index(drop=True)

    scenarios = []
    for i, row in df.iterrows():
        position = i + 1
        remaining = 3 - row["played"]  # máximo 3 partidos en fase de grupos

        if position <= 2:
            status = "✅ Clasificado o en posición de clasificar"
        elif position == 3:
            status = "⚠️ Posible tercer mejor puesto — depende de otros grupos"
        else:
            status = "❌ Necesita resultados favorables para clasificar"

        scenarios.append({
            "Pos": position,
            "": row["flag_emoji"],
            "Selección": row["team_name"],
            "Pts": row["points"],
            "PJ": row["played"],
            "Rest.": remaining,
            "Escenario": status
        })

    return scenarios
