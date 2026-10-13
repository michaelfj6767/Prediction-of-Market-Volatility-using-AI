"""
utils.py — Rekayasa fitur & target untuk RADAR VOLATILITAS.

>>> LENGKAPI bagian TODO dengan kodemu SENDIRI. <<< (Pertemuan 1)

ATURAN:
  1. Tulis sendiri — jangan menyalin jawaban jadi.
  2. Isi tiap "# JELASKAN:" dengan kata-katamu. Ini yang dinilai.
  3. Mentok? Buka "Bank Petunjuk" di bawah (menyebut konsep, bukan kode jadi).

Ingat: kita menebak BESARNYA gerakan (volatilitas), BUKAN arah naik/turun.
"""
import numpy as np
import pandas as pd

FITUR = ["absret0", "absret_lag1", "absret_lag2",
         "vol5", "vol10", "vol20", "ewma_abs", "rng5", "vol_chg"]
HORIZON = 5  # kita menilai volatilitas 5 hari ke depan


def buat_fitur(df: pd.DataFrame) -> pd.DataFrame:
    """Butuh kolom 'Close' dan 'Volume'."""
    df = df.copy()
    df["return"] = df["Close"].pct_change()

    # TODO 1 — "absret" = BESARNYA return (nilai mutlak, abaikan tanda +/-). (Bank A)
    df["absret"] = None  # <-- GANTI
    # JELASKAN kenapa untuk volatilitas kita pakai NILAI MUTLAK, bukan return biasa: ____

    # TODO 2 — kondisi HARI INI & 2 hari lalu: absret0 (hari ini), absret_lag1, absret_lag2. (Bank B)
    df["absret0"] = None       # <-- GANTI
    df["absret_lag1"] = None   # <-- GANTI
    df["absret_lag2"] = None   # <-- GANTI

    # TODO 3 — volatilitas bergulir: vol5, vol10, vol20 = sebaran (std) return
    #          selama 5/10/20 hari terakhir. (Bank C)
    df["vol5"] = None    # <-- GANTI
    df["vol10"] = None   # <-- GANTI
    df["vol20"] = None   # <-- GANTI

    # TODO 4 — "ewma_abs" = rata-rata BERGERAK-EKSPONENSIAL dari absret
    #          (volatilitas terbaru, lebih menimbang hari baru). (Bank D)
    df["ewma_abs"] = None  # <-- GANTI

    # TODO 5 — "rng5" = rentang harga 5 hari (tertinggi - terendah) dibagi harga. (Bank E)
    df["rng5"] = None  # <-- GANTI

    # TODO 6 — "vol_chg" = VOLUME hari ini dibanding rata-rata 20 hari (bentuk rasio-1). (Bank F)
    df["vol_chg"] = None  # <-- GANTI
    # JELASKAN kenapa LONJAKAN VOLUME bisa menandakan gejolak: ____

    return df


def volatilitas_depan(df: pd.DataFrame) -> pd.Series:
    """Volatilitas HORIZON hari KE DEPAN — dipakai untuk membuat label."""
    # TODO 7 — std return selama HORIZON hari, lalu GESER ke depan sejauh HORIZON
    #          supaya baris hari-t berisi volatilitas HARI SETELAHnya. (Bank G)
    return None  # <-- GANTI


def buat_target(df: pd.DataFrame, ambang: float) -> pd.DataFrame:
    df = df.copy()
    # TODO 8 — target = 1 bila volatilitas ke depan LEBIH BESAR dari 'ambang'
    #          (BERGEJOLAK), selain itu 0. (Bank H)
    df["target"] = None  # <-- GANTI
    return df


# =====================================================================
# BANK PETUNJUK (konsep / nama metode — BUKAN jawaban jadi)
# A. 'nilai mutlak' sebuah kolom: metode .abs().
# B. Nilai hari ini = kolom itu sendiri. Nilai hari lalu = geser mundur (.shift(lag)).
# C. 'sebaran' = standar deviasi. 'selama 5 hari' = rolling(5) lalu .std().
# D. Rata-rata bergerak eksponensial: .ewm(span=...).mean().
# E. Tertinggi 5 hari = rolling(5).max(); terendah = rolling(5).min(); bagi dgn Close.
# F. df["Volume"] / df["Volume"].rolling(20).mean() - 1.
# G. df["return"].rolling(HORIZON).std().shift(-HORIZON)  (angka NEGATIF = lihat ke depan).
# H. Bandingkan hasil volatilitas_depan(df) dengan 'ambang' pakai '>', lalu .astype(int).
# =====================================================================
