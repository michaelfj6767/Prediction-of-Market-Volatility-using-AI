"""
app.py — Radar Volatilitas Saham (TENANG / BERGEJOLAK).

>>> LENGKAPI TODO dengan kodemu sendiri. <<< (Pertemuan 4-5)
Jalankan lokal:  streamlit run app.py
⚠️ EDUKASI, BUKAN SARAN INVESTASI.
"""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

from utils import buat_fitur, FITUR, HORIZON

MODEL_PATH = Path("model_volatilitas.joblib")
DATA_PATH = Path("saham_contoh.csv")
st.set_page_config(page_title="Radar Volatilitas", page_icon="📡", layout="centered")


# --- Pemuatan data sudah disediakan (yfinance online, fallback data contoh) ---
@st.cache_data(show_spinner=False)
def ambil_data(ticker: str):
    try:
        import yfinance as yf
        df = yf.download(ticker, start="2020-01-01", auto_adjust=True, progress=False)
        if len(df) > 60:
            df = df.reset_index()[["Date", "Close", "Volume"]]
            df.columns = ["Date", "Close", "Volume"]
            return df, "yfinance"
    except Exception:
        pass
    return pd.read_csv(DATA_PATH, parse_dates=["Date"]), "contoh"


st.title("📡 Radar Volatilitas Saham")
st.caption(f"Apakah ~{HORIZON} hari ke depan TENANG atau BERGEJOLAK? (bukan prediksi naik/turun)")
st.warning("⚠️ **Materi edukasi, bukan saran investasi.**")

# TODO 1 — Muat model dari MODEL_PATH. Kalau belum ada, tampilkan pesan & hentikan. (Bank A)
if not MODEL_PATH.exists():
    st.error("Jalankan dulu model"); st.stop
model = joblib.load("MODEL_PATH")

ticker = st.text_input("Kode saham (contoh: BBCA.JK, TLKM.JK, AAPL)", value="TLKM.JK")
df, sumber = ambil_data(ticker)
if sumber == "contoh":
    st.info("Memakai data contoh (offline). Di Streamlit Cloud, data nyata otomatis via yfinance.")

tab1, tab2, tab3 = st.tabs(["📡 Radar", "📈 Riwayat Volatilitas", "ℹ️ Tentang"])

# ---------------- Tab 1: Radar ----------------
with tab1:
    # TODO 2 — Prediksi untuk baris data PALING AKHIR:
    #   (a) buat fitur dari df, buang baris kosong, ambil baris terakhir;
    #   (b) ambil PROBABILITAS dari model;
    #   (c) 'bergejolak' bila peluang kelas 1 >= 0.5; simpan keyakinan. (Bank B)
    df_features = df.copy()
    df_clean = df_features.dropna()
    X_last = df_clean.drop.iloc[[-1]]

    probabilities = model.predict_proba[X_last]
    peluang_1 = probabilities[1]
    bergejolak = peluang_1 >= 0.5

    if(bergejolak):
        yakin = peluang_1
    else:
        yakin = 1-peluang_1
    
    if bergejolak is True:
        st.markdown("## 🟠 BERGEJOLAK")
        st.write(f"Diperkirakan ~{HORIZON} hari ke depan bergerak lebih liar.")
    elif bergejolak is False:
        st.markdown("## 🟢 TENANG")
        st.write(f"Diperkirakan ~{HORIZON} hari ke depan relatif stabil.")
    else:
        st.info("Lengkapi TODO 1 & 2.")
    st.progress(float(yakin), text=f"Keyakinan model: {yakin*100:.1f}%")

# ---------------- Tab 2: Riwayat ----------------
with tab2:
    st.subheader("Volatilitas 10-hari (60 hari terakhir)")
    # TODO 3 — Tampilkan grafik volatilitas: std return 10-hari (dikali 100),
    #          60 titik terakhir, pakai st.line_chart. (Bank C)
    chart_data = data["volatilitas_10_hari"].tail(60) * 100
    st.line_chart(chart_data)

# ---------------- Tab 3: Tentang ----------------
with tab3:
    st.markdown(
        f"""
        **Cara kerja:** harga & volume → fitur *besar gerakan* → Random Forest memprediksi
        apakah volatilitas ~{HORIZON} hari ke depan tinggi. Dilatih dgn split kronologis,
        ambang dari data latih (tanpa kebocoran).

        Volatilitas BISA diprediksi (beda dengan arah) karena ia menggerombol — tapi cek
        selalu baseline. ⚠️ Edukasi, bukan saran investasi.
        """
    )


# =====================================================================
# BANK PETUNJUK (konsep, bukan jawaban jadi)
# A. joblib.load(MODEL_PATH). Cek MODEL_PATH.exists(); kalau tidak: st.error(...)+st.stop().
# B. buat_fitur(df).dropna() -> .iloc[[-1]] (kurung dobel). model.predict_proba(x)[0]
#    memberi [peluang_tenang, peluang_gejolak]. 'yakin' = nilai terbesar (max).
# C. Hitung df["Close"].pct_change().rolling(10).std()*100, buang NaN, set index tanggal,
#    ambil .tail(60), lalu st.line_chart(...).
# =====================================================================
