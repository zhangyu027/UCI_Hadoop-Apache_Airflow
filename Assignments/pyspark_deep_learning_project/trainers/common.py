from pathlib import Path
import pandas as pd


def read_parquet(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Parquet path not found: {p}")
    return pd.read_parquet(p)
