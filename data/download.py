from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent

WDBC_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
BANKNOTE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00267/data_banknote_authentication.txt"

WDBC_COLS = (
    ["id", "diagnosis"]
    + [f"radius_{s}" for s in ("mean", "se", "worst")]
    + [f"texture_{s}" for s in ("mean", "se", "worst")]
    + [f"perimeter_{s}" for s in ("mean", "se", "worst")]
    + [f"area_{s}" for s in ("mean", "se", "worst")]
    + [f"smoothness_{s}" for s in ("mean", "se", "worst")]
    + [f"compactness_{s}" for s in ("mean", "se", "worst")]
    + [f"concavity_{s}" for s in ("mean", "se", "worst")]
    + [f"concave_points_{s}" for s in ("mean", "se", "worst")]
    + [f"symmetry_{s}" for s in ("mean", "se", "worst")]
    + [f"fractal_dimension_{s}" for s in ("mean", "se", "worst")]
)

BANKNOTE_COLS = ["variance", "skewness", "curtosis", "entropy", "class"]


def _try_download(url: str, dest: Path, **read_kwargs) -> pd.DataFrame:
    try:
        import requests
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        dest.write_bytes(r.content)
        return pd.read_csv(dest, **read_kwargs)
    except Exception:
        return None


def download_datasets() -> None:
    wdbc_path = DATA_DIR / "wdbc.csv"
    banknote_path = DATA_DIR / "banknote.csv"

    if not wdbc_path.exists():
        print("Downloading WDBC dataset...")
        df = _try_download(WDBC_URL, DATA_DIR / "_wdbc_raw.csv", header=None, names=WDBC_COLS)
        if df is not None:
            df = df.drop(columns=["id"])
            df["diagnosis"] = df["diagnosis"].map({"M": 1, "B": 0})
            df.to_csv(wdbc_path, index=False)
            print(f"  wdbc.csv saved — {len(df)} rows")
        else:
            print("  Download failed, using sklearn breast_cancer dataset as fallback.")
            from sklearn.datasets import load_breast_cancer
            bc = load_breast_cancer()
            df = pd.DataFrame(bc.data, columns=bc.feature_names)
            df.insert(0, "diagnosis", bc.target)
            df.to_csv(wdbc_path, index=False)
            print(f"  wdbc.csv saved — {len(df)} rows")
    else:
        print(f"wdbc.csv already exists ({len(pd.read_csv(wdbc_path))} rows).")

    if not banknote_path.exists():
        print("Downloading Banknote dataset...")
        df = _try_download(BANKNOTE_URL, DATA_DIR / "_banknote_raw.csv", header=None, names=BANKNOTE_COLS)
        if df is not None:
            df.to_csv(banknote_path, index=False)
            print(f"  banknote.csv saved — {len(df)} rows")
        else:
            print("  Download failed, generating synthetic banknote data as fallback.")
            from sklearn.datasets import make_classification
            import numpy as np
            X, y = make_classification(n_samples=1372, n_features=4, random_state=42)
            df = pd.DataFrame(X, columns=BANKNOTE_COLS[:-1])
            df["class"] = y
            df.to_csv(banknote_path, index=False)
            print(f"  banknote.csv saved — {len(df)} rows")
    else:
        print(f"banknote.csv already exists ({len(pd.read_csv(banknote_path))} rows).")


def load_wdbc():
    path = DATA_DIR / "wdbc.csv"
    if not path.exists():
        download_datasets()
    df = pd.read_csv(path)
    X = df.drop(columns=["diagnosis"]).values
    y = df["diagnosis"].values
    return df, X, y


def load_banknote():
    path = DATA_DIR / "banknote.csv"
    if not path.exists():
        download_datasets()
    df = pd.read_csv(path)
    X = df.drop(columns=["class"]).values
    y = df["class"].values
    return df, X, y


if __name__ == "__main__":
    download_datasets()
