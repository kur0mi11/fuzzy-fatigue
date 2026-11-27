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
        c.execute(
            "INSERT INTO riwayat VALUES (?,?,?,?,?,?,?)",
            (
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                n["tidur"],
                n["kerja"],
                n["istirahat"],
                n["waktu"],
                round(h["skor"], 1),
                h["kategori"],
            ),
        )


def db_baca():
    with sqlite3.connect(DB) as c:
        return pd.read_sql_query("SELECT * FROM riwayat ORDER BY waktu_cek DESC", c)


# ---------------- PAGE CONFIG & CUSTOM CSS ----------------
st.set_page_config(page_title="Fuzzy Fatigue Index", page_icon="🏍️", layout="wide")
db_init()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg-main: #F7F8FA;
    --bg-card: #FFFFFF;
    --text-dark: #111827;
    --text-muted: #6B7280;
    --emerald: #10B981;
    --emerald-dark: #059669;
    --emerald-soft: #ECFDF5;
    --amber-soft: #FFFBEB;
    --amber-text: #D97706;
    --red-soft: #FEF2F2;
    --red-text: #DC2626;
    --border-light: #E5E7EB;
}

/* Global Background & Font */
.stApp {
    background-color: var(--bg-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-dark);
}

/* Container Spacing */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1180px !important;
}

/* Top Navbar Pill */
.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-card);
    padding: 12px 24px;
    border-radius: 999px;
    border: 1px solid var(--border-light);
    margin-bottom: 28px;
}
.brand-logo {
    font-weight: 700;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-dark);
}
.brand-badge {
    background: var(--text-dark);
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 999px;
}

/* Editorial Hero Section */
.hero-section {
    text-align: center;
    padding: 12px 16px 28px 16px;
}
.hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: 3.4rem;
    line-height: 1.08;
    font-weight: 400;
    color: var(--text-dark);
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--text-muted);
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Bento Card Style */
.bento-card {
    background: var(--bg-card);
    border-radius: 22px;
    padding: 24px;
    border: 1px solid var(--border-light);
    margin-bottom: 18px;
}
.card-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 4px;
}
.card-desc {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 16px;
}

/* Status Pill Badges */
.pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.pill-green { background: var(--emerald-soft); color: var(--emerald-dark); }
.pill-amber { background: var(--amber-soft); color: var(--amber-text); }
.pill-red   { background: var(--red-soft); color: var(--red-text); }

/* Hero Metric Card */
.emerald-card {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    color: #FFFFFF;
    border-radius: 22px;
    padding: 26px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
}
.emerald-card-label {
    font-size: 0.85rem;
    font-weight: 500;
    opacity: 0.9;
}
.emerald-card-score {
    font-size: 3.6rem;
    font-weight: 700;
    line-height: 1.05;
    margin: 8px 0 12px 0;
    letter-spacing: -0.03em;
}
.emerald-card-sub {
    font-size: 0.82rem;
    opacity: 0.92;
    line-height: 1.45;
}

/* Segmented Bar */
.seg-bar-wrap {
    display: flex;
    height: 12px;
    border-radius: 999px;
    overflow: hidden;
    background: #F3F4F6;
    gap: 3px;
    margin: 12px 0;
}

/* Center Tab Wrapper */
div[data-testid="stTabs"] > div:first-child {
    display: flex;
    justify-content: center;
}

/* Tab Container (Pill Bar) */
.stTabs [data-baseweb="tab-list"] {
    display: inline-flex !important;
    flex-wrap: wrap !important;
    gap: 6px !important;
    background: #FFFFFF !important;
    padding: 6px !important;
    border-radius: 999px !important;
    border: 1px solid #E5E7EB !important;
    margin: 0 auto 24px auto !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
}

/* Masing-masing Tab */
.stTabs [data-baseweb="tab"] {
    height: auto !important;
    padding: 8px 18px !important;
    border-radius: 999px !important;
    border: none !important;
    background: transparent !important;
    color: #6B7280 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    transition: all 0.18s ease !important;
}

/* Hover Tab */
.stTabs [data-baseweb="tab"]:hover {
    color: #111827 !important;
    background: #F3F4F6 !important;
}

/* Tab Aktif */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #111827 !important;
    color: #FFFFFF !important;
}

/* Hilangkan garis bawah merah & border bawaan BaseWeb */
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab"]::before,
.stTabs [data-baseweb="tab"]::after {
    display: none !important;
    content: none !important;
    border: none !important;
    background: transparent !important;
}

/* Buttons */
.stButton > button {
    background-color: var(--text-dark) !important;
    color: #FFFFFF !important;
    border-radius: 999px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    border: none !important;
    width: 100%;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: var(--emerald-dark) !important;
    transform: translateY(-1px);
}

/* Slider Accent */
div[data-baseweb="slider"] > div > div > div:nth-child(2) {
    background-color: var(--emerald) !important;
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.3rem; }
    .hide-mobile { display: none; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- TOP HEADER & HERO ----------------
st.markdown("""
<div class="top-nav">
    <div class="brand-logo"><span>❖</span> FuzzyFatigue AI</div>
    <div style="font-size:0.82rem;color:#6B7280;" class="hide-mobile">Mamdani Inference · Safety Telemetry</div>
    <div class="brand-badge">Driver Guard v1.0</div>
</div>

<div class="hero-section">
    <div class="hero-title">Monitor Driver Fatigue<br>with Fuzzy Precision</div>
    <div class="hero-sub">
        Sistem peringatan dini tingkat kelelahan pengemudi ojol &amp; kurir berbasis logika Fuzzy Mamdani untuk menjaga keselamatan berkendara secara real-time.
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Cek Kelelahan", "Riwayat", "Validasi Data", "Metode & Sumber"])

# ---------------- TAB 1: CEK ----------------
with tab1:
    col_input, col_output = st.columns([1.15, 1], gap="large")

    with col_input:
        st.markdown("""
        <div class="bento-card" style="padding-bottom:12px;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <div class="card-label">Parameter Kondisi Pengemudi</div>
                    <div class="card-desc">Masukkan 4 indikator di bawah sesuai kondisi aktual di lapangan</div>
                </div>
                <span class="pill pill-green">Live Input</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            tidur = st.number_input("🛏️ Jam tidur semalam (0–10 jam)", min_value=0.0, max_value=10.0, value=7.0, step=0.01, format="%.2f")
            kerja = st.number_input("🛵 Sudah kerja berapa jam hari ini? (0–16 jam)", min_value=0.0, max_value=16.0, value=4.0, step=0.01, format="%.2f")
            istirahat = st.number_input("☕ Jeda sejak istirahat terakhir (0–6 jam)", min_value=0.0, max_value=6.0, value=1.0, step=0.01, format="%.2f")
            jam_pilih = st.time_input("🕒 Jam operasional saat ini (00:00–23:59)", value=datetime.now().time().replace(second=0, microsecond=0), step=60)

        # Konversi objek time (HH:MM) ke desimal jam (contoh: 14:30 -> 14.5)
        waktu = round(jam_pilih.hour + (jam_pilih.minute / 60.0), 2)

        nilai = {"tidur": tidur, "kerja": kerja, "istirahat": istirahat, "waktu": waktu}
        hasil = hitung(tidur, kerja, istirahat, waktu)
        skor = hasil["skor"]
        kat = hasil["kategori"]
        kat_lower = kat.strip().lower()
        is_prima = ("prima" in kat_lower or "aman" in kat_lower or "rendah" in kat_lower)

        p_tidur = min(int((tidur / 8.0) * 100), 100)
        p_segar = max(100 - int(skor), 0)
        st.markdown(f"""
        <div class="bento-card" style="margin-top:16px;">
            <div class="card-label">Indeks Kesiapan &amp; Pemulihan</div>
            <div class="card-desc">Ringkasan rasio kebugaran tidur dan kesiapan fokus</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:8px;">
                <div style="background:#F9FAFB;padding:14px;border-radius:16px;">
                    <span class="pill pill-green">Sleep Ratio</span>
                    <div style="font-size:2rem;font-weight:700;margin-top:8px;color:#111827;">{p_tidur}%</div>
                    <div style="font-size:0.75rem;color:#6B7280;">Dari target 8 jam tidur</div>
                </div>
                <div style="background:#F9FAFB;padding:14px;border-radius:16px;">
                    <span class="pill {'pill-green' if p_segar >= 60 else 'pill-red'}">Alertness</span>
                    <div style="font-size:2rem;font-weight:700;margin-top:8px;color:#111827;">{p_segar}%</div>
                    <div style="font-size:0.75rem;color:#6B7280;">Tingkat kewaspadaan sisa</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_output:
        if is_prima:
            card_bg = "linear-gradient(135deg, #10B981 0%, #059669 100%)"
            pill_cls = "pill-green"
            status_desc = "Kondisi prima — kewaspadaan dan pemulihan berada pada level aman untuk berkendara."
        elif "mulai lelah" in kat_lower or "waspada" in kat_lower or "sedang" in kat_lower:
            card_bg = "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"
            pill_cls = "pill-red"
            status_desc = "Mulai lelah — terdeteksi tanda awal kelelahan, perhatikan jeda istirahat dan hidrasi."
        else:
            card_bg = "linear-gradient(135deg, #B91C1C 0%, #7F1D1D 100%)"
            pill_cls = "pill-red"
            status_desc = "Risiko kelelahan tinggi — disarankan segera berhenti dan beristirahat sebelum lanjut jalan."

        st.markdown(f"""
        <div class="emerald-card" style="background:{card_bg};">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span class="emerald-card-label">Fatigue Risk Score</span>
                <span style="background:rgba(255,255,255,0.22);padding:4px 12px;border-radius:999px;font-size:0.75rem;font-weight:700;">
                    {kat.upper()}
                </span>
            </div>
            <div class="emerald-card-score">{skor:.0f}<span style="font-size:1.3rem;font-weight:500;opacity:0.85;"> / 100</span></div>
            <div class="emerald-card-sub">
                {status_desc}
            </div>
        </div>
        """, unsafe_allow_html=True)

        aman_w = max(0.0, min(100.0, 100.0 - skor))
        risiko_w = max(0.0, min(100.0, float(skor)))
        bar_risiko_color = "#10B981" if is_prima else "#EF4444"
        st.markdown(f"""
        <div class="bento-card">
            <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <span class="card-label">Distribusi Ambang Risiko</span>
                <span class="pill {pill_cls}">{kat.upper()}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:10px;font-weight:700;font-size:1.15rem;">
                <span style="color:#10B981;">{aman_w:.0f}% <small style="font-weight:500;font-size:0.75rem;color:#6B7280;">Prima</small></span>
                <span style="color:#EF4444;">{risiko_w:.0f}% <small style="font-weight:500;font-size:0.75rem;color:#6B7280;">Mulai Lelah</small></span>
            </div>
            <div class="seg-bar-wrap">
                <div style="width:{aman_w}%;background:#10B981;border-radius:999px;"></div>
                <div style="width:{risiko_w}%;background:{bar_risiko_color};border-radius:999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        saran_list = "".join([f"<li style='margin-bottom:8px;color:#374151;font-size:0.88rem;'>{s}</li>" for s in saran(hasil, nilai)])
        st.markdown(f"""
        <div class="bento-card">
            <div class="card-label">Rekomendasi Tindakan</div>
            <div class="card-desc">Saran keselamatan berdasarkan rule fuzzy yang aktif</div>
            <ul style="padding-left:18px;margin:0;">{saran_list}</ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Simpan Hasil ke Riwayat"):
            db_simpan(nilai, hasil)
            st.success("Data pengecekan berhasil disimpan ke riwayat.")

    st.caption(DISCLAIMER)

    with st.expander("🔍 Lihat Detail Perhitungan Fuzzy Mamdani (Fuzzifikasi → Rule → Defuzzifikasi)"):
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            st.markdown("**1. Fuzzifikasi (Derajat Keanggotaan μ)**")
            baris = [(INPUT[v]["label"], h, round(m, 3)) for v, d in hasil["derajat"].items() for h, m in d.items()]
            st.dataframe(pd.DataFrame(baris, columns=["Variabel", "Himpunan", "Derajat (μ)"]), hide_index=True, use_container_width=True)
        with c_f2:
            st.markdown("**2. Rule Aktif (α = min anteseden)**")
            aktif = [(i + 1, teks_rule(i), round(a, 3)) for i, a in enumerate(hasil["kekuatan"]) if a > 0]
            st.dataframe(pd.DataFrame(aktif, columns=["No", "Rule", "α"]), hide_index=True, use_container_width=True)

        st.markdown("**3. Agregasi (Max) & 4. Defuzzifikasi (Centroid)**")
        f = fig_output(hasil)
        st.pyplot(f)
        plt.close(f)

# ---------------- TAB 2: RIWAYAT ----------------
with tab2:
    rw = db_baca()
    if rw.empty:
        st.markdown("""
        <div class="bento-card" style="text-align:center;padding:48px 24px;">
            <div style="font-size:2rem;margin-bottom:8px;">📊</div>
            <div class="card-label" style="font-size:1.1rem;">Belum Ada Riwayat Pengecekan</div>
            <div class="card-desc">Lakukan simulasi pada tab <b>Cek Kelelahan</b> lalu klik tombol simpan untuk melihat analitik di sini.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        modes = rw["kategori"].mode()
        dom = modes.iloc[0] if not modes.empty else "-"
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="bento-card">
                <span class="pill pill-green">Total Log</span>
                <div style="font-size:2.4rem;font-weight:700;margin-top:8px;">{len(rw)}</div>
                <div class="card-desc" style="margin:0;">Jumlah pengecekan tersimpan</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="bento-card">
                <span class="pill pill-red">Mean Score</span>
                <div style="font-size:2.4rem;font-weight:700;margin-top:8px;">{rw['skor'].mean():.1f}</div>
                <div class="card-desc" style="margin:0;">Rata-rata indeks kelelahan</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="bento-card">
                <span class="pill pill-green">Dominan</span>
                <div style="font-size:2.4rem;font-weight:700;margin-top:8px;">{str(dom).capitalize()}</div>
                <div class="card-desc" style="margin:0;">Kategori paling sering muncul</div>
            </div>""", unsafe_allow_html=True)

        c_chart, c_tbl = st.columns([1, 1.4], gap="large")
        with c_chart:
            st.markdown('<div class="bento-card"><div class="card-label">Distribusi Kategori</div><div class="card-desc">Proporsi hasil evaluasi pengemudi</div>', unsafe_allow_html=True)
            st.bar_chart(rw["kategori"].value_counts(), color="#10B981")
            st.markdown("</div>", unsafe_allow_html=True)
        with c_tbl:
            st.markdown('<div class="bento-card"><div class="card-label">Log Pengecekan Terakhir</div><div class="card-desc">Riwayat parameter dan skor terhitung</div>', unsafe_allow_html=True)
            st.dataframe(rw, hide_index=True, use_container_width=True)
            st.download_button("Unduh Riwayat (CSV)", rw.to_csv(index=False), "riwayat.csv", "text/csv")
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Catatan: pada lingkungan cloud ephemeral, berkas riwayat.db dapat ter-reset saat aplikasi restart.")

# ---------------- TAB 3: VALIDASI ----------------
with tab3:
    st.markdown("""
    <div class="bento-card">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <div class="card-label">Validasi Akurasi Model Fuzzy</div>
                <div class="card-desc">Bandingkan keluaran sistem dengan label kuesioner lapangan. Default menggunakan dataset simulasi.</div>
            </div>
            <span class="pill pill-amber">Benchmark Mode</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    up = st.file_uploader("Unggah file CSV (kolom wajib: tidur, kerja, istirahat, jam, kategori_lapangan)", type="csv")
    try:
        df = pd.read_csv(up) if up else pd.read_csv("data/data_dummy_driver.csv")
        out, akurasi, tol1, konfusi = evaluasi(df)

        v1, v2 = st.columns(2)
        with v1:
            st.markdown(f"""
            <div class="bento-card">
                <span class="pill pill-green">Exact Match</span>
                <div style="font-size:2.6rem;font-weight:700;margin-top:8px;">{akurasi*100:.0f}%</div>
                <div class="card-desc" style="margin:0;">Akurasi kecocokan persis dengan label lapangan</div>
            </div>""", unsafe_allow_html=True)
        with v2:
            st.markdown(f"""
            <div class="bento-card">
                <span class="pill pill-amber">±1 Level Tolerance</span>
                <div style="font-size:2.6rem;font-weight:700;margin-top:8px;">{tol1*100:.0f}%</div>
                <div class="card-desc" style="margin:0;">Akurasi tepat atau selisih maksimal 1 tingkat</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="bento-card"><div class="card-label">Matriks Konfusi &amp; Hasil Evaluasi</div><div class="card-desc">Baris = label lapangan, Kolom = prediksi sistem</div>', unsafe_allow_html=True)
        st.dataframe(konfusi, use_container_width=True)
        st.dataframe(out, hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal membaca data: {e}")

# ---------------- TAB 4: METODE ----------------
with tab4:
    st.markdown("""
    <div class="bento-card">
        <span class="pill pill-green">Arsitektur Inferensi</span>
        <div class="card-label" style="font-size:1.15rem;margin-top:8px;">Metode Fuzzy Mamdani</div>
        <div class="card-desc" style="margin-bottom:0;">
            Sistem memproses 4 variabel input melalui 4 tahap utama: <b>Fuzzifikasi</b> (fungsi keanggotaan trapesium/segitiga), <b>Evaluasi Rule</b> (operator AND = min), <b>Agregasi</b> (operator max), dan <b>Defuzzifikasi</b> (metode Centroid).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Kurva Fungsi Keanggotaan Input")
    cols_fig = st.columns(2)
    for idx, v in enumerate(INPUT):
        with cols_fig[idx % 2]:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            f = fig_input(v, nilai[v])
            st.pyplot(f)
            plt.close(f)
            st.markdown("</div>", unsafe_allow_html=True)

    c_rule, c_ref = st.columns([1.3, 1], gap="large")
    with c_rule:
        rules_html = "".join([f"<div style='padding:8px 0;border-bottom:1px solid #F3F4F6;font-size:0.84rem;'><b>#{i+1}</b> {teks_rule(i)}</div>" for i in range(len(RULES))])
        st.markdown(f"""
        <div class="bento-card">
            <div class="card-label">Basis Pengetahuan ({len(RULES)} Aturan Fuzzy)</div>
            <div class="card-desc">Daftar aturan IF-THEN yang digunakan dalam mesin inferensi</div>
            <div style="max-height:360px;overflow-y:auto;padding-right:6px;">{rules_html}</div>
        </div>
        """, unsafe_allow_html=True)

    with c_ref:
        st.markdown(f"""
        <div class="bento-card">
            <div class="card-label">Sumber Acuan Parameter</div>
            <div class="card-desc">Landasan regulasi dan literatur ilmiah</div>
            <ul style="padding-left:18px;font-size:0.85rem;color:#374151;line-height:1.6;">
                <li style="margin-bottom:10px;"><b>AAA Foundation for Traffic Safety (2016)</b>, <i>Acute Sleep Deprivation and Risk of Motor Vehicle Crash Involvement</i>.</li>
                <li style="margin-bottom:10px;"><b>UU No. 22 Tahun 2009 (LLAJ) Pasal 90</b>: batas waktu kerja dan istirahat pengemudi kendaraan bermotor.</li>
                <li><b>Journal of Vocational Health Studies 7 (2024)</b>: penelitian kelelahan pengemudi ojek online di Jabodetabek.</li>
            </ul>
            <div style="margin-top:16px;padding:12px;background:#F9FAFB;border-radius:12px;font-size:0.78rem;color:#6B7280;">
                {DISCLAIMER}
            </div>
        </div>
        """, unsafe_allow_html=True)