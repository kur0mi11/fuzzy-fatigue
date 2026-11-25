"""cek_parameter.py - pemeriksaan otomatis untuk Indri setelah mengubah parameter.py.
Jalankan: python cek_parameter.py
1) Celah himpunan: tiap nilai input harus punya minimal satu himpunan dengan derajat > 0.
2) Cakupan rule: tiap kombinasi input harus mengaktifkan minimal satu rule.
3) Konflik rule: dua rule dengan anteseden sama tetapi akibat berbeda."""
import numpy as np
from fuzzy_engine import INPUT, RULES, hitung, mf, teks_rule

print("1) CEK CELAH HIMPUNAN")
for var, cfg in INPUT.items():
    lo, hi = cfg["rentang"]
    x = np.linspace(lo, hi, 2401)
    total = np.maximum.reduce([mf(x, s) for s in cfg["himpunan"].values()])
    celah = x[total <= 0]
    print(f"   {var:10s}", "OK" if celah.size == 0 else f"CELAH di {celah.min():.2f} s/d {celah.max():.2f}")

print("2) CEK CAKUPAN RULE (beberapa detik)")
kosong = []
for t in np.arange(0, 10.01, 0.5):
    for k in np.arange(0, 16.01, 1):
        for i in np.arange(0, 6.01, 1):
            for w in np.arange(0, 24, 1):
                if hitung(t, k, i, w)["agregat"].sum() <= 0:
                    kosong.append((t, k, i, w))
print("   OK, semua kombinasi tercakup" if not kosong else f"   ADA {len(kosong)} kombinasi tanpa rule, contoh: {kosong[:3]}")

print("3) CEK KONFLIK RULE")
lihat, konflik = {}, 0
for n, (ant, akibat) in enumerate(RULES, 1):
    kunci = tuple(sorted(ant.items()))
    if kunci in lihat and lihat[kunci][1] != akibat:
        print(f"   KONFLIK: rule {lihat[kunci][0]} dan {n}"); konflik += 1
    lihat[kunci] = (n, akibat)
print("   OK, tidak ada konflik langsung" if konflik == 0 else f"   {konflik} konflik")
