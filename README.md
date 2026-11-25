# Fuzzy Fatigue Index (versi lengkap, sesuai Panduan Fase 1-2)

Sistem peringatan dini kelelahan pengemudi ojol & kurir. Metode: Fuzzy Mamdani.
Semua angka di `parameter.py` adalah USULAN AWAL; validasi dengan riset & wawancara sebelum dijadikan klaim di laporan.

## Struktur
| File | Fungsi | Pemilik |
|---|---|---|
| parameter.py | Himpunan fuzzy + 24 rule (satu-satunya tempat mengubah angka) | Indri |
| fuzzy_engine.py | Fuzzifikasi, inferensi Mamdani, centroid, saran | Feny |
| grafik.py, buat_grafik.py | Grafik himpunan untuk laporan | Feny |
| app.py | Website Streamlit 4 tab | Keisha |
| validasi.py | Akurasi + matriks konfusi | Keisha |
| uji_skenario.py | 10 skenario uji -> hasil_uji_skenario.csv | Keisha |
| buat_data_dummy.py | Membuat data/data_dummy_driver.csv (FIKTIF) | Iqlima |
| data/ | data_dummy_driver.csv dan data_lapangan.csv (hasil wawancara) | Iqlima |

## Menjalankan
    pip install -r requirements.txt
    python buat_data_dummy.py     # sekali saja, membuat data dummy
    python uji_skenario.py        # harus: Kesesuaian 9/10 = 90%
    streamlit run app.py          # buka http://localhost:8501
    python buat_grafik.py         # PNG di folder grafik_laporan/

## Angka acuan (untuk mengecek instalasi benar)
Input tidur 5, kerja 11, istirahat 3.5, pukul 20 -> skor 71.13, kategori Rawan.
Derajat: kerja Lama 0.75, istirahat Lama 0.667 (bukan 0.333 seperti README lama).
Dummy: akurasi 55%, toleransi 1 tingkat 98%.
