"""
app.py - Website Fuzzy Fatigue Index (Streamlit).
Jalankan: streamlit run app.py
Tab: 1) Cek Kelelahan 2) Riwayat 3) Validasi Data 4) Metode & Sumber
"""
import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fuzzy_engine import INPUT, RULES, DISCLAIMER, hitung, saran, teks_rule
from grafik import fig_input, fig_output, WARNA
from validasi import evaluasi

DB = "riwayat.db"

def db_init():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS riwayat (
            waktu_cek TEXT, tidur REAL, kerja REAL, istirahat REAL, jam REAL, skor REAL, kategori TEXT)""")

def db_simpan(n, h):
    with sqlite3.connect(DB) as c:
        c.execute("INSERT INTO riwayat VALUES (?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M"), n["tidur"], n["kerja"], n["istirahat"],
                   n["waktu"], round(h["skor"], 1), h["kategori"]))

def db_baca():
    with sqlite3.connect(DB) as c:
        return pd.read_sql_query("SELECT * FROM riwayat ORDER BY waktu_cek DESC", c)

st.set_page_config(page_title="Fuzzy Fatigue Index", page_icon="🏍️", layout="centered")
db_init()
st.title("🏍️ Fuzzy Fatigue Index")
st.caption("Sistem peringatan dini kelelahan pengemudi ojol & kurir · Fuzzy Logic metode Mamdani")
tab1, tab2, tab3, tab4 = st.tabs(["Cek Kelelahan", "Riwayat", "Validasi Data", "Metode & Sumber"])

# ---------------- TAB 1: CEK ----------------
with tab1:
    st.info("Cara pakai: geser 4 slider sesuai kondisimu sekarang. Skor dan saran langsung berubah.")
    tidur = st.slider("Jam tidur semalam (jam)", 0.0, 10.0, 7.0, 0.5)
    kerja = st.slider("Sudah kerja berapa jam hari ini?", 0.0, 16.0, 4.0, 0.5)
    istirahat = st.slider("Berapa jam sejak istirahat terakhir?", 0.0, 6.0, 1.0, 0.25)
    waktu = st.slider("Pukul berapa sekarang? (14.5 = pukul 14.30)", 0.0, 23.5, 12.0, 0.5)
    nilai = {"tidur": tidur, "kerja": kerja, "istirahat": istirahat, "waktu": waktu}
    hasil = hitung(tidur, kerja, istirahat, waktu)
    warna = WARNA[hasil["kategori"]]
    st.markdown(
        f"""<div style="background:{warna};color:white;border-radius:14px;padding:18px;text-align:center;margin:12px 0">
        <div style="font-size:0.95rem;opacity:.9">Skor risiko kelelahan</div>
        <div style="font-size:3rem;font-weight:700;line-height:1.1">{hasil['skor']:.0f}<span style="font-size:1.2rem"> / 100</span></div>
        <div style="font-size:1.4rem;font-weight:600">{hasil['kategori'].upper()}</div></div>""",
        unsafe_allow_html=True)
    st.progress(min(max(hasil["skor"] / 100, 0.0), 1.0))
    st.subheader("Saran untuk kamu")
    for s in saran(hasil, nilai):
        st.markdown(f"- {s}")
    st.caption(DISCLAIMER)
    if st.button("Simpan ke riwayat"):
        db_simpan(nilai, hasil); st.success("Tersimpan di riwayat.")
    with st.expander("Lihat proses perhitungan fuzzy (untuk laporan/presentasi)"):
        st.markdown("**1. Fuzzifikasi**")
        baris = [(INPUT[v]["label"], h, round(m, 3)) for v, d in hasil["derajat"].items() for h, m in d.items()]
        st.dataframe(pd.DataFrame(baris, columns=["Variabel", "Himpunan", "Derajat (μ)"]), hide_index=True)
        st.markdown("**2. Rule aktif** (α = minimum dari anteseden)")
        aktif = [(i + 1, teks_rule(i), round(a, 3)) for i, a in enumerate(hasil["kekuatan"]) if a > 0]
        st.dataframe(pd.DataFrame(aktif, columns=["No", "Rule", "α"]), hide_index=True)
        st.markdown("**3. Agregasi (max) dan 4. Defuzzifikasi (centroid)**")
        f = fig_output(hasil); st.pyplot(f); plt.close(f)

# ---------------- TAB 2: RIWAYAT ----------------
with tab2:
    st.subheader("Riwayat pengecekan")
    rw = db_baca()
    if rw.empty:
        st.info("Belum ada riwayat. Simpan hasil dari tab Cek Kelelahan.")
    else:
        c1, c2 = st.columns(2)
        c1.metric("Jumlah pengecekan", len(rw))
        c2.metric("Rata-rata skor", f"{rw['skor'].mean():.1f}")
        st.bar_chart(rw["kategori"].value_counts())
        st.dataframe(rw, hide_index=True)
        st.download_button("Unduh riwayat (CSV)", rw.to_csv(index=False), "riwayat.csv", "text/csv")
    st.caption("Catatan: di Streamlit Cloud, berkas riwayat.db bisa hilang saat aplikasi restart. Untuk produksi gunakan database online.")

# ---------------- TAB 3: VALIDASI ----------------
with tab3:
    st.subheader("Validasi sistem dengan data")
    st.warning("Data bawaan adalah DATA DUMMY (fiktif) untuk demonstrasi. Unggah data asli hasil kuesioner untuk validasi sebenarnya.")
    up = st.file_uploader("Unggah CSV (kolom: tidur, kerja, istirahat, jam, kategori_lapangan)", type="csv")
    try:
        df = pd.read_csv(up) if up else pd.read_csv("data/data_dummy_driver.csv")
        out, akurasi, tol1, konfusi = evaluasi(df)
        c1, c2 = st.columns(2)
        c1.metric("Akurasi tepat", f"{akurasi*100:.0f}%")
        c2.metric("Benar atau meleset 1 tingkat", f"{tol1*100:.0f}%")
        st.markdown("**Matriks konfusi** (baris = label lapangan, kolom = keluaran sistem)")
        st.dataframe(konfusi)
        st.dataframe(out, hide_index=True)
    except Exception as e:
        st.error(f"Gagal membaca data: {e}")

# ---------------- TAB 4: METODE ----------------
with tab4:
    st.subheader("Metode")
    st.markdown("Fuzzy Mamdani: fuzzifikasi, evaluasi rule (AND = min), agregasi (max), defuzzifikasi centroid.")
    for v in INPUT:
        f = fig_input(v, nilai[v]); st.pyplot(f); plt.close(f)
    st.markdown(f"**Daftar {len(RULES)} rule**")
    for i in range(len(RULES)):
        st.markdown(f"{i + 1}. {teks_rule(i)}")
    st.subheader("Sumber acuan parameter")
    st.markdown(
        "- AAA Foundation for Traffic Safety (2016), *Acute Sleep Deprivation and Risk of Motor Vehicle Crash Involvement*.\n"
        "- UU No. 22 Tahun 2009 (LLAJ) Pasal 90: batas waktu kerja dan istirahat pengemudi kendaraan bermotor umum.\n"
        "- Penelitian kelelahan pengemudi ojek online di Jabodetabek, *Journal of Vocational Health Studies* 7 (2024).")
    st.caption(DISCLAIMER)
