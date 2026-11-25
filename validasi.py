"""validasi.py - membandingkan keluaran sistem fuzzy dengan label lapangan (data dummy atau data asli)."""
import pandas as pd
from fuzzy_engine import hitung

URUTAN = ["Prima", "Mulai Lelah", "Rawan", "Berhenti Dulu"]

def evaluasi(df):
    """df wajib punya kolom: tidur, kerja, istirahat, jam, kategori_lapangan"""
    hasil = [hitung(r.tidur, r.kerja, r.istirahat, r.jam) for r in df.itertuples()]
    out = df.copy()
    out["skor_sistem"] = [round(h["skor"], 1) for h in hasil]
    out["kategori_sistem"] = [h["kategori"] for h in hasil]
    sel = out["kategori_sistem"].map(URUTAN.index) - out["kategori_lapangan"].map(URUTAN.index)
    akurasi = float((sel == 0).mean())
    toleransi1 = float((sel.abs() <= 1).mean())   # benar atau meleset satu tingkat
    konfusi = pd.crosstab(out["kategori_lapangan"], out["kategori_sistem"]).reindex(index=URUTAN, columns=URUTAN, fill_value=0)
    return out, akurasi, toleransi1, konfusi
