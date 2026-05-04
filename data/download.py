"""
Downloads, extracts, and cleans both datasets from UCI.
Idempotent — skips download if CSVs already exist.
Run with: python data/download.py
"""
import io
import os
import zipfile
import requests
import pandas as pd

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

WDBC_URL = "https://archive.ics.uci.edu/static/public/17/breast+cancer+wisconsin+diagnostic.zip"
BANK_URL = "https://archive.ics.uci.edu/static/public/267/banknote+authentication.zip"

WDBC_COLS = ["id", "diagnosis"] + [
    f"{stat}_{measure}"
    for measure in ["radius", "texture", "perimeter", "area", "smoothness",
                    "compactness", "concavity", "concave_points",
                    "symmetry", "fractal_dimension"]
    for stat in ["mean", "se", "worst"]
]

BANK_COLS = ["variance", "skewness", "curtosis", "entropy", "class"]


def download_and_extract(url: str, filename: str) -> bytes:
    """Download a ZIP and return the content of the target file."""
    print(f"Downloading {url} ...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        return z.read(filename)


def build_wdbc():
    out_path = os.path.join(DATA_DIR, "wdbc.csv")
    if os.path.exists(out_path):
        df = pd.read_csv(out_path)
        print(f"wdbc.csv already exists — {len(df)} rows, skipping download.")
        return
    raw = download_and_extract(WDBC_URL, "wdbc.data")
    df = pd.read_csv(io.BytesIO(raw), header=None, names=WDBC_COLS)
    df = df.drop(columns=["id"])
    df["diagnosis"] = df["diagnosis"].map({"M": 1, "B": 0})
    df.to_csv(out_path, index=False)
    print(f"wdbc.csv saved — {len(df)} rows loaded.")


def build_banknote():
    out_path = os.path.join(DATA_DIR, "banknote.csv")
    if os.path.exists(out_path):
        df = pd.read_csv(out_path)
        print(f"banknote.csv already exists — {len(df)} rows, skipping download.")
        return
    raw = download_and_extract(
        BANK_URL, "data_banknote_authentication.txt")
    df = pd.read_csv(io.BytesIO(raw), header=None, names=BANK_COLS)
    df.to_csv(out_path, index=False)
    print(f"banknote.csv saved — {len(df)} rows loaded.")


if __name__ == "__main__":
    build_wdbc()
    build_banknote()