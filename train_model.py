"""
train_model.py — Melatih model RADAR VOLATILITAS & menyimpannya.

>>> LENGKAPI TODO dengan kodemu sendiri. <<< (Pertemuan 2)
Jalankan:  python train_model.py   ->  model/model_volatilitas.joblib
Mentok? Lihat Bank Petunjuk di bawah.
"""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from utils import buat_fitur, buat_target, volatilitas_depan, FITUR

DATA_PATH = Path("data/saham_contoh.csv")
MODEL_PATH = Path("model/model_volatilitas.joblib")


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df = buat_fitur(df)

    # TODO 1 — Hitung AMBANG dari DATA LATIH saja (80% awal), bukan seluruh data
    #          (kalau pakai seluruh data = kebocoran!). Ambil median volatilitas_depan
    #          pada 80% baris pertama. (Bank A)
    n = int(len(df) * 0.8)
    ambang = volatilitas_depan(df).iloc[:n].median()  # <-- GANTI
    # JELASKAN kenapa ambang HARUS dari data latih saja: ambang harus diambil dari data latih agar mencegah data yg diambil salah ditafsirkan

    df = buat_target(df, ambang).dropna().reset_index(drop=True)
    X, y = df[FITUR], df["target"]

    # TODO 2 — SPLIT KRONOLOGIS (80% awal latih, 20% akhir uji). Jangan diacak. (Bank B)
    n = int(len(df) * 0.8)
    X_tr, X_te = X.iloc[:n], X.iloc[n:] None  # <-- GANTI
    y_tr, y_te = y.iloc[:n], y.iloc[n:] None  # <-- GANTI

    # TODO 3 — Latih Random Forest pada data latih. (Bank C)
    model = RandomForestClassifier(random_state=67)
    model.fit(X_tr, y_tr)

    # TODO 4 — Akurasi uji & baseline majority; bandingkan dengan tebak koin (0.50). (Bank D)
    acc = accuracy_score(y_te, model.predict(X_te))       # <-- GANTI
    majority = max(y_te.mean(), 1 - y_te.mean())   # <-- GANTI
    print(f"Akurasi model    : {acc}")
    print(f"Baseline majority: {majority}")
    # JELASKAN: apakah modelmu jauh di atas 0.50? Apa artinya soal volatilitas? ____

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel disimpan ke: {MODEL_PATH}")


if __name__ == "__main__":
    main()


# =====================================================================
# BANK PETUNJUK (konsep, bukan jawaban jadi)
# A. volatilitas_depan(df).iloc[:n].median()
# B. X.iloc[:n] / X.iloc[n:] (dan sama untuk y). 'n' sudah dihitung.
# C. RandomForestClassifier(...).fit(X_tr, y_tr)  (boleh set random_state).
# D. acc = model.score(X_te, y_te); majority = max(y_te.mean(), 1 - y_te.mean()).
# =====================================================================
