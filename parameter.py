"""
parameter.py (PEMILIK: Indri - tugas C dan D)
Berisi seluruh parameter sistem: himpunan fuzzy tiap variabel (tugas C) dan rule base (tugas D).
Ubah angka di sini setelah riset/wawancara; tidak perlu menyentuh fuzzy_engine.py.
Format himpunan: (a, b, c, d) = trapesium; segitiga bila b == c; list tuple = gabungan (OR/max).
"""
INPUT = {
    "tidur": {"label": "Jam tidur semalam", "satuan": "jam", "rentang": (0, 10), "langkah": 0.5,
              "himpunan": {"Kurang": (0, 0, 4, 6), "Cukup": (4, 6, 6, 7.5), "Baik": (6, 7.5, 10, 10)}},
    "kerja": {"label": "Lama kerja hari ini", "satuan": "jam", "rentang": (0, 16), "langkah": 0.5,
              "himpunan": {"Singkat": (0, 0, 3, 6), "Sedang": (4, 8, 8, 12), "Lama": (8, 12, 16, 16)}},
    "istirahat": {"label": "Lama sejak istirahat terakhir", "satuan": "jam", "rentang": (0, 6), "langkah": 0.25,
                  "himpunan": {"Baru": (0, 0, 1, 2), "Sedang": (1, 2.5, 2.5, 4), "Lama": (2.5, 4, 6, 6)}},
    "waktu": {"label": "Jam sekarang", "satuan": "pukul", "rentang": (0, 24), "langkah": 0.5,
              "himpunan": {"Pagi-Siang": (5, 7, 15, 18),
                           "Sore-Malam": (15, 18, 21, 23),
                           "Dini Hari": [(0, 0, 4, 6), (21, 23, 24, 24)]}},  # 23.00-05.00 (melingkar)
}
OUTPUT = {"label": "Skor risiko kelelahan", "rentang": (0, 100),
          "himpunan": {"Prima": (0, 0, 20, 35), "Mulai Lelah": (25, 45, 45, 62),
                       "Rawan": (50, 70, 70, 85), "Berhenti Dulu": (75, 90, 100, 100)}}

P, M, R, B = "Prima", "Mulai Lelah", "Rawan", "Berhenti Dulu"
RULES = [
    # --- Dasar: kombinasi tidur x kerja (menjamin semua input tercakup)
    ({"tidur": "Kurang", "kerja": "Lama"}, B),
    ({"tidur": "Kurang", "kerja": "Sedang"}, M),
    ({"tidur": "Kurang", "kerja": "Singkat"}, M),
    ({"tidur": "Cukup", "kerja": "Lama"}, R),
    ({"tidur": "Cukup", "kerja": "Sedang"}, M),
    ({"tidur": "Cukup", "kerja": "Singkat"}, P),
    ({"tidur": "Baik", "kerja": "Lama"}, M),
    ({"tidur": "Baik", "kerja": "Sedang"}, P),
    ({"tidur": "Baik", "kerja": "Singkat"}, P),
    # --- Pengaruh lama tidak istirahat
    ({"istirahat": "Lama", "kerja": "Lama"}, B),
    ({"istirahat": "Lama", "tidur": "Kurang", "kerja": "Sedang"}, R),
    ({"istirahat": "Lama", "kerja": "Sedang"}, M),
    ({"istirahat": "Baru", "tidur": "Baik", "kerja": "Singkat"}, P),
    ({"istirahat": "Baru", "tidur": "Cukup", "kerja": "Singkat"}, P),
    ({"istirahat": "Sedang", "kerja": "Lama"}, R),
    # --- Pengaruh waktu (dini hari paling rawan)
    ({"waktu": "Dini Hari", "tidur": "Kurang"}, B),
    ({"waktu": "Dini Hari", "kerja": "Lama"}, B),
    ({"waktu": "Dini Hari", "kerja": "Sedang"}, R),
    ({"waktu": "Dini Hari", "tidur": "Cukup"}, M),
    ({"waktu": "Dini Hari", "kerja": "Singkat"}, M),
    ({"waktu": "Dini Hari", "istirahat": "Lama"}, B),
    ({"waktu": "Pagi-Siang", "tidur": "Baik", "kerja": "Singkat"}, P),
    # --- Kombinasi berat
    ({"tidur": "Kurang", "kerja": "Lama", "istirahat": "Lama"}, B),
    ({"tidur": "Cukup", "kerja": "Lama", "waktu": "Sore-Malam"}, R),
]
