"""
Utilidades de carga y procesamiento de datos para Data Fútbol Lab.
"""

import pandas as pd
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_matches() -> pd.DataFrame:
    """Carga y tipifica el CSV de partidos."""
    df = pd.read_csv(DATA_DIR / "matches.csv", parse_dates=["date"])
    df["time"] = df["time"].astype(str)
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")
    return df


def load_teams() -> pd.DataFrame:
    """Carga el CSV de selecciones."""
    return pd.read_csv(DATA_DIR / "teams.csv")


def load_standings() -> pd.DataFrame:
    """Carga el CSV de posiciones."""
    return pd.read_csv(DATA_DIR / "standings.csv")


def get_today_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve los partidos cuya fecha coincide con hoy."""
    today = pd.Timestamp(date.today())
    return df[df["date"] == today].reset_index(drop=True)


def get_upcoming_matches(df: pd.DataFrame, days_ahead: int = 5) -> pd.DataFrame:
    """Devuelve los partidos programados en los próximos N días (excluye hoy)."""
    today = pd.Timestamp(date.today())
    limit = today + pd.Timedelta(days=days_ahead)
    mask = (df["date"] > today) & (df["date"] <= limit) & (df["status"] == "Programado")
    return df[mask].sort_values("date").reset_index(drop=True)


def format_result(row: pd.Series) -> str:
    """Devuelve el marcador como cadena o el estado del partido."""
    if pd.notna(row["home_score"]) and pd.notna(row["away_score"]):
        return f"{int(row['home_score'])} - {int(row['away_score'])}"
    return row["status"]


def is_demo_data(df: pd.DataFrame) -> bool:
    """Verifica si los datos provienen de fuentes marcadas como DEMO."""
    if "source" in df.columns:
        return (df["source"] == "DEMO").all()
    return False
