"""Jalankan: python uji_skenario.py  -> tabel hasil uji (disimpan juga ke hasil_uji_skenario.csv) untuk Bab 4 laporan."""
import csv
from fuzzy_engine import hitung

# (nama, tidur, kerja, istirahat, jam, ekspektasi)  -> ekspektasi = penilaian manual awal; sesuaikan dengan hasil wawancara driver
SKENARIO = [
    ("Segar di pagi hari",             8.0,  3.0, 0.5,  9.0, "Prima"),
    ("Siang hari normal",              7.5,  5.0, 1.0, 13.0, "Prima"),
    ("Sore, kerja sedang",             6.0,  8.0, 2.5, 17.0, "Mulai Lelah"),
    ("Kerja lama tapi baru istirahat", 8.0, 12.0, 0.5, 14.0, "Mulai Lelah"),
    ("Kurang tidur, baru mulai kerja", 4.0,  2.0, 0.5,  9.0, "Mulai Lelah"),
    ("Malam hari, sudah capek",        5.0, 11.0, 3.5, 20.0, "Rawan"),
    ("Lembur malam",                   6.0, 13.0, 4.0, 22.0, "Rawan"),
    ("Dini hari, kurang tidur",        3.0, 12.0, 4.0,  3.0, "Berhenti Dulu"),
    ("Kondisi terburuk",               2.0, 15.0, 5.5,  2.0, "Berhenti Dulu"),
    ("Dini hari tapi segar",           8.5,  2.0, 0.5,  4.0, "Mulai Lelah"),
]
baris = []
for no, (nama, t, k, i, w, eks) in enumerate(SKENARIO, 1):
    h = hitung(t, k, i, w)
    baris.append([no, nama, t, k, i, w, round(h["skor"], 1), h["kategori"], eks, "Ya" if h["kategori"] == eks else "Tidak"])
kepala = ["No", "Skenario", "Tidur (jam)", "Kerja (jam)", "Sejak istirahat (jam)", "Pukul", "Skor", "Kategori sistem", "Ekspektasi", "Sesuai?"]
print(" | ".join(kepala))
for b in baris:
    print(" | ".join(str(x) for x in b))
cocok = sum(1 for b in baris if b[-1] == "Ya")
print(f"\nKesesuaian: {cocok}/{len(baris)} = {cocok/len(baris)*100:.0f}%")
with open("hasil_uji_skenario.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(kepala); w.writerows(baris)
