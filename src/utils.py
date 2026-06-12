"""
Utilidades de carga, validación y procesamiento de datos para Data Fútbol Lab.
"""

import pandas as pd
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

# ─── Esquemas de columnas requeridas por CSV ───────────────────────────────────

REQUIRED_COLS = {
    "matches": [
        "match_id", "date", "time", "home_team", "away_team",
        "group", "stage", "venue", "status", "data_status",
    ],
    "teams": [
        "team_id", "team_name", "confederation", "fifa_ranking",
        "group", "flag_emoji", "data_status",
    ],
    "standings": [
        "group", "position", "team_name", "flag_emoji",
        "played", "won", "drawn", "lost",
        "goals_for", "goals_against", "goal_diff", "points", "data_status",
    ],
}

VALID_STATUSES = {"Programado", "En juego", "Finalizado", "Suspendido", "Aplazado"}
VALID_DATA_STATUSES = {"demo", "verified", "pending"}

# ─── Carga de datos ────────────────────────────────────────────────────────────

def load_matches() -> pd.DataFrame:
    """Carga y tipifica el CSV de partidos."""
    df = pd.read_csv(DATA_DIR / "matches.csv", parse_dates=["date"])
    df["time"] = df["time"].astype(str)
    df["home_score"] = pd.to_numeric(df.get("home_score", pd.Series(dtype=float)), errors="coerce")
    df["away_score"] = pd.to_numeric(df.get("away_score", pd.Series(dtype=float)), errors="coerce")
    df["group"] = df["group"].astype(str).str.strip()
    return df


def load_teams() -> pd.DataFrame:
    """Carga el CSV de selecciones."""
    df = pd.read_csv(DATA_DIR / "teams.csv")
    df["group"] = df["group"].astype(str).str.strip()
    return df


def load_standings() -> pd.DataFrame:
    """Carga el CSV de posiciones."""
    df = pd.read_csv(DATA_DIR / "standings.csv")
    df["group"] = df["group"].astype(str).str.strip()
    return df


def load_sources() -> pd.DataFrame:
    """Carga el registro de fuentes de datos."""
    path = DATA_DIR / "sources.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=["source_id", "source_name", "source_url", "data_type", "notes"])

# ─── Filtros de partidos ───────────────────────────────────────────────────────

def get_today_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve los partidos cuya fecha coincide con hoy."""
    today = pd.Timestamp(date.today())
    return df[df["date"] == today].reset_index(drop=True)


def get_upcoming_matches(df: pd.DataFrame, days_ahead: int = 7) -> pd.DataFrame:
    """Devuelve los partidos programados en los próximos N días (excluye hoy)."""
    today = pd.Timestamp(date.today())
    limit = today + pd.Timedelta(days=days_ahead)
    mask = (df["date"] > today) & (df["date"] <= limit) & (df["status"] == "Programado")
    return df[mask].sort_values("date").reset_index(drop=True)


def format_result(row: pd.Series) -> str:
    """Devuelve el marcador como cadena o el estado del partido."""
    if pd.notna(row.get("home_score")) and pd.notna(row.get("away_score")):
        return f"{int(row['home_score'])} - {int(row['away_score'])}"
    return row["status"]

# ─── Estado de calidad de datos ───────────────────────────────────────────────

def _get_statuses(df: pd.DataFrame) -> set:
    """Extrae el conjunto de data_status presentes en el DataFrame."""
    if "data_status" in df.columns:
        return set(df["data_status"].dropna().unique())
    if "source" in df.columns:
        return {"demo"} if (df["source"] == "DEMO").all() else {"unknown"}
    return {"unknown"}


def is_demo_data(df: pd.DataFrame) -> bool:
    """True si TODOS los registros están marcados como demo."""
    statuses = _get_statuses(df)
    return statuses == {"demo"}


def has_mixed_data(df: pd.DataFrame) -> bool:
    """True si hay mezcla de demo con datos verificados o pendientes."""
    statuses = _get_statuses(df)
    return "demo" in statuses and len(statuses) > 1


def is_verified_data(df: pd.DataFrame) -> bool:
    """True si todos los registros están marcados como verified."""
    statuses = _get_statuses(df)
    return statuses.issubset({"verified"})


def get_data_status_summary(df: pd.DataFrame) -> dict:
    """Devuelve conteos de registros por data_status."""
    if "data_status" not in df.columns:
        return {}
    return df["data_status"].value_counts().to_dict()

# ─── Validación de esquema ────────────────────────────────────────────────────

def validate_csv(df: pd.DataFrame, csv_name: str) -> list[str]:
    """
    Valida el esquema de un DataFrame contra las reglas del proyecto.
    Devuelve una lista de mensajes de advertencia (vacía si todo está bien).
    """
    warnings: list[str] = []
    required = REQUIRED_COLS.get(csv_name, [])

    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        warnings.append(f"[{csv_name}] Columnas faltantes: {missing_cols}")
        return warnings

    if "group" in df.columns:
        spaces = df[df["group"].astype(str) != df["group"].astype(str).str.strip()]
        if not spaces.empty:
            warnings.append(
                f"[{csv_name}] {len(spaces)} fila(s) con espacios en columna 'group'"
            )

    if "data_status" in df.columns:
        invalid_ds = df[~df["data_status"].isin(VALID_DATA_STATUSES)]
        if not invalid_ds.empty:
            bad = invalid_ds["data_status"].unique().tolist()
            warnings.append(
                f"[{csv_name}] Valores inválidos en 'data_status': {bad}. "
                f"Válidos: {sorted(VALID_DATA_STATUSES)}"
            )

    if csv_name == "matches" and "status" in df.columns:
        invalid_st = df[~df["status"].isin(VALID_STATUSES)]
        if not invalid_st.empty:
            bad = invalid_st["status"].unique().tolist()
            warnings.append(
                f"[matches] Valores inválidos en 'status': {bad}. "
                f"Válidos: {sorted(VALID_STATUSES)}"
            )

    for col in ["home_team", "away_team", "team_name", "venue"]:
        if col in df.columns:
            empty = df[df[col].isna() | (df[col].astype(str).str.strip() == "")]
            if not empty.empty:
                warnings.append(
                    f"[{csv_name}] {len(empty)} fila(s) con valor vacío en '{col}'"
                )

    return warnings


def validate_all_csvs(
    matches: pd.DataFrame,
    teams: pd.DataFrame,
    standings: pd.DataFrame,
) -> list[str]:
    """Valida los tres CSVs principales y devuelve todas las advertencias."""
    issues: list[str] = []
    issues.extend(validate_csv(matches, "matches"))
    issues.extend(validate_csv(teams, "teams"))
    issues.extend(validate_csv(standings, "standings"))
    return issues
