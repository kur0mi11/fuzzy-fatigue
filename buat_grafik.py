"""Jalankan: python buat_grafik.py  -> menyimpan grafik himpunan fuzzy ke folder grafik_laporan/ (untuk laporan)."""
import os
import matplotlib.pyplot as plt
from fuzzy_engine import INPUT, hitung
from grafik import fig_input, fig_output

os.makedirs("grafik_laporan", exist_ok=True)
for var in INPUT:
    f = fig_input(var); f.savefig(f"grafik_laporan/mf_{var}.png", dpi=200); plt.close(f)
f = fig_output(); f.savefig("grafik_laporan/mf_output.png", dpi=200); plt.close(f)
# contoh hasil agregasi + centroid untuk satu kasus (dini hari, kurang tidur)
h = hitung(3, 12, 4, 3)
f = fig_output(h); f.savefig("grafik_laporan/contoh_agregasi_centroid.png", dpi=200); plt.close(f)
print("Selesai: lihat folder grafik_laporan/")
