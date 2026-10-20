from pathlib import Path
import joblib  
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 

from utils import buat_fitur, buat_target, volatilitas_depan, FITUR

DATA_PATH = Path("saham_contoh.csv")
MODEL_PATH = Path("model_volatilitas.joblib")


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    df = buat_fitur(df)

    # TODO 1 — Hitung AMBANG dari DATA LATIH saja (80% awal)
    n = int(len(df) * 0.8)
    ambang = volatilitas_depan(df).iloc[:n].median()  
    
    # JELASKAN kenapa ambang HARUS dari data latih saja: 
    # Agar tidak terjadi "Data Leakage" (kebocoran data). Jika kita menggunakan informasi dari data uji (20% akhir) 
    # untuk menghitung ambang, model kita secara tidak langsung sudah 'mengintip' masa depan, 
    # sehingga hasil evaluasi model menjadi tidak realistis/terlalu optimis.

    df = buat_target(df, ambang).dropna().reset_index(drop=True)
    X, y = df[FITUR], df["target"]

    # TODO 2 — SPLIT KRONOLOGIS (80% awal latih, 20% akhir uji). Jangan diacak.
    n = int(len(df) * 0.8)
    X_tr, X_te = X.iloc[:n], X.iloc[n:]   
    y_tr, y_te = y.iloc[:n], y.iloc[n:]   

    # TODO 3 — Latih Random Forest pada data latih.
    model = RandomForestClassifier(random_state=67)
    model.fit(X_tr, y_tr)

    # TODO 4 — Akurasi uji & baseline majority; bandingkan dengan tebak koin (0.50).
    acc = accuracy_score(y_te, model.predict(X_te))       
    majority = max(y_te.mean(), 1 - y_te.mean())   
    print(f"Akurasi model    : {acc:.4f}")
    print(f"Baseline majority: {majority:.4f}")
    
    # JELASKAN: apakah modelmu jauh di atas 0.50? Apa artinya soal volatilitas? 
    # Jika akurasi model berada di atas 0.50 (tebak koin) dan di atas baseline majority, artinya 
    # pola volatilitas saham di masa lalu memiliki struktur prediktif (tidak acak murni) dan 
    # fitur-fitur yang dibuat berhasil menangkap sinyal pergerakan volatilitas tersebut.

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel disimpan ke: {MODEL_PATH}")


if __name__ == "__main__":
    main()
