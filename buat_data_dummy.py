"""
buat_data_dummy.py - membuat DATA DUMMY (fiktif) 60 pengemudi untuk uji sistem.
Jalankan: python buat_data_dummy.py -> data/data_dummy_driver.csv
PENTING: data ini BUKAN data nyata. Label 'kategori_lapangan' dibuat dari rumus lain
(bukan dari mesin fuzzy) + noise acak, hanya untuk mendemonstrasikan alur validasi.
Ganti dengan data kuesioner/wawancara asli driver (kolom sama) sebelum menarik kesimpulan.
"""
import numpy as np, pandas as pd

rng = np.random.default_rng(42)
N = 60
tidur = np.clip(rng.normal(6.0, 1.5, N), 2, 9).round(1)
kerja = rng.uniform(1, 15, N).round(1)
istirahat = np.clip(rng.uniform(0, 5.5, N) * (0.6 + kerja / 25), 0, 6).round(1)
jam = rng.choice([2, 4, 9, 11, 13, 15, 17, 19, 21, 22, 23], size=N, p=[.05,.05,.12,.1,.12,.1,.1,.12,.1,.08,.06])
dini = ((jam >= 23) | (jam <= 5)).astype(float)
sore = ((jam >= 14) & (jam < 17)).astype(float)
z = 0.9*np.maximum(0, 7-tidur) + 0.35*np.maximum(0, kerja-6) + 0.45*istirahat + 2.0*dini + 0.8*sore + rng.normal(0, 0.6, N)
kategori = np.select([z < 1.5, z < 3.5, z < 5.5], ["Prima", "Mulai Lelah", "Rawan"], "Berhenti Dulu")
df = pd.DataFrame({"id": [f"D{i:02d}" for i in range(1, N+1)], "tidur": tidur, "kerja": kerja,
                   "istirahat": istirahat, "jam": jam, "kategori_lapangan": kategori})
df.to_csv("data/data_dummy_driver.csv", index=False)
print(df.head(8)); print(df["kategori_lapangan"].value_counts())
