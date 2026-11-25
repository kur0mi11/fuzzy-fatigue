"""
fuzzy_engine.py
Mesin Fuzzy Logic metode MAMDANI untuk Fuzzy Fatigue Index (tanpa library fuzzy, hanya numpy).
(PEMILIK: Feny - tugas E, F, I; parameter ada di parameter.py)
Alur: Fuzzifikasi -> Evaluasi Rule (AND = min) -> Agregasi (max) -> Defuzzifikasi (centroid)
Parameter (himpunan dan rule) ada di parameter.py dan merupakan USULAN AWAL.
"""
import numpy as np

# ---------------------------------------------------------------
# 1. FUNGSI KEANGGOTAAN (trapesium: a,b,c,d ; segitiga: b == c)
# ---------------------------------------------------------------
def trapmf(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    rising = (x - a) / (b - a) if b > a else (x >= a).astype(float)
    falling = (d - x) / (d - c) if d > c else (x <= d).astype(float)
    return np.clip(np.minimum(rising, falling), 0.0, 1.0)

def mf(x, spec):
    """spec = satu tuple (a,b,c,d) atau list tuple (gabungan/OR dengan max)."""
    if isinstance(spec, tuple):
        return trapmf(x, *spec)
    return np.maximum.reduce([trapmf(x, *s) for s in spec])

from parameter import INPUT, OUTPUT, RULES, P, M, R, B

# ---------------------------------------------------------------
# 2. MESIN INFERENSI MAMDANI
# ---------------------------------------------------------------
_X = np.linspace(*OUTPUT["rentang"], 1001)
_MF_OUT = {k: mf(_X, v) for k, v in OUTPUT["himpunan"].items()}

def fuzzifikasi(nilai):
    """nilai: dict {tidur, kerja, istirahat, waktu} -> derajat keanggotaan tiap himpunan."""
    der = {}
    for var, cfg in INPUT.items():
        lo, hi = cfg["rentang"]
        x = min(max(float(nilai[var]), lo), hi)
        der[var] = {h: float(mf(x, s)) for h, s in cfg["himpunan"].items()}
    return der

def hitung(tidur, kerja, istirahat, waktu):
    nilai = {"tidur": tidur, "kerja": kerja, "istirahat": istirahat, "waktu": waktu}
    der = fuzzifikasi(nilai)
    agregat = np.zeros_like(_X)
    kekuatan = []                                   # alpha tiap rule
    for anteseden, akibat in RULES:
        alpha = min(der[v][h] for v, h in anteseden.items())            # AND = min
        kekuatan.append(alpha)
        agregat = np.maximum(agregat, np.minimum(_MF_OUT[akibat], alpha))  # implikasi min, agregasi max
    skor = float((_X * agregat).sum() / agregat.sum()) if agregat.sum() > 0 else 0.0  # centroid
    mu_out = {k: float(np.interp(skor, _X, v)) for k, v in _MF_OUT.items()}
    kategori = max(mu_out, key=mu_out.get)
    return {"skor": skor, "kategori": kategori, "derajat": der, "kekuatan": kekuatan,
            "x": _X, "agregat": agregat, "mu_out": mu_out}

def teks_rule(i):
    ant, akibat = RULES[i]
    kiri = " DAN ".join(f"{INPUT[v]['label']} {h.upper()}" for v, h in ant.items())
    return f"JIKA {kiri} MAKA risiko {akibat.upper()}"

# ---------------------------------------------------------------
# 3. MODUL SARAN
# ---------------------------------------------------------------
SARAN_UTAMA = {
    "Prima": ["Kondisi masih baik. Tetap minum air dan istirahat singkat tiap 2-3 jam."],
    "Mulai Lelah": ["Rencanakan istirahat 10-15 menit dalam 30 menit ke depan.",
                    "Minum air dan makan ringan.", "Hindari mengambil order jarak jauh."],
    "Rawan": ["Berhenti di tempat aman dan istirahat minimal 20-30 menit sekarang.",
              "Jangan ambil order jarak jauh atau memaksakan target bonus.",
              "Jika mengantuk, tidur singkat 15-20 menit di tempat aman."],
    "Berhenti Dulu": ["Hentikan perjalanan sekarang dan cari tempat aman.",
                      "Istirahat atau tidur dulu; pertimbangkan pulang.",
                      "Bonus tidak sebanding dengan keselamatan."],
}

def saran(hasil, nilai):
    out = list(SARAN_UTAMA[hasil["kategori"]])
    if nilai["tidur"] < 5:
        out.append("Tidur semalam sangat kurang: usahakan tidur lebih awal malam ini.")
    if nilai["istirahat"] > 4:
        out.append("Sudah lama tidak berhenti: ambil jeda sekarang, jangan menunggu order berikutnya.")
    if nilai["waktu"] >= 23 or nilai["waktu"] <= 5:
        out.append("Dini hari adalah jam paling rawan mengantuk: ekstra waspada atau pertimbangkan berhenti.")
    return out

DISCLAIMER = ("Alat edukasi dan peringatan dini, bukan alat ukur medis. "
              "Jika Anda mengantuk, berhenti dan istirahat meskipun skor rendah.")
