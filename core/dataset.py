from __future__ import annotations
import os
import pandas as pd

class DataRegistry:
    """Load and hold the Framingham dataset in memory."""
    def __init__(self, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found at {path}")
        df = pd.read_csv(path)
        # Standardize column names (strip spaces)
        df.columns = [c.strip() for c in df.columns]
        self.df = df
