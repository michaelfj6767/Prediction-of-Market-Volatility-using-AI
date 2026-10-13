# 📡 Radar Volatilitas Saham — PROYEK MURID (Starter)

Bangun aplikasi yang memprediksi apakah saham akan **TENANG atau BERGEJOLAK**
beberapa hari ke depan (ukuran risiko, **bukan** arah naik/turun).

> ⚠️ Proyek EDUKASI — bukan saran investasi.

## 📏 Aturan main
1. **Tulis kodemu sendiri.** Jangan menyalin jawaban jadi.
2. Isi tiap **`# JELASKAN`** / sel JELASKAN dengan kata-katamu — **ini yang paling dinilai.**
3. Mentok? Buka **"Bank Petunjuk"** (bawah tiap file/notebook) — berisi konsep/nama metode, bukan jawaban jadi.
4. Kamu akan ditanya "baris ini ngapain?" saat presentasi.

## Alur (ikuti Panduan_Build_Bertahap.pdf)
| Pertemuan | Kamu mengerjakan | File |
|---|---|---|
| 1 | Fitur & volatilitas ke depan (TODO 1–7) | `utils.py` / notebook |
| 2 | Ambang, target, split, latih, baseline (TODO 1–4 / 8–12) | `train_model.py` / notebook |
| 3 | Evaluasi: baseline persistence + confusion matrix (tafsirkan) | notebook |
| 4 | Aplikasi — tab Radar (TODO 1–2) | `app.py` |
| 5 | Aplikasi — grafik volatilitas (TODO 3) + jalankan lokal | `app.py` |
| 6 | Deploy + presentasi | GitHub + Streamlit |

## Menjalankan (setelah TODO diisi)
```bash
pip install -r requirements.txt
python train_model.py     # -> model/model_volatilitas.joblib
streamlit run app.py
```

## ✅ Checklist
- [ ] Ambang & split dari **data latih** saja (tanpa kebocoran).
- [ ] Split **kronologis** (tidak diacak).
- [ ] Bandingkan dengan **baseline** (majority & persistence).
- [ ] Ini **volatilitas**, bukan arah.
- [ ] Sel **JELASKAN** sudah diisi.
