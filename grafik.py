"""grafik.py - fungsi pembuat grafik himpunan fuzzy (dipakai app.py dan buat_grafik.py)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fuzzy_engine import INPUT, OUTPUT, mf

WARNA = {"Prima": "#2e8b57", "Mulai Lelah": "#d4a017", "Rawan": "#e67e22", "Berhenti Dulu": "#c0392b"}

def fig_input(var, nilai=None):
    cfg = INPUT[var]
    lo, hi = cfg["rentang"]
    x = np.linspace(lo, hi, 601)
    fig, ax = plt.subplots(figsize=(6, 2.6))
    for nama, spec in cfg["himpunan"].items():
        ax.plot(x, mf(x, spec), label=nama, linewidth=2)
    if nilai is not None:
        ax.axvline(nilai, color="black", linestyle="--", linewidth=1)
    ax.set_title(f"{cfg['label']} ({cfg['satuan']})", fontsize=10)
    ax.set_ylim(-0.02, 1.08); ax.set_ylabel("Derajat keanggotaan", fontsize=8)
    ax.legend(fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    fig.tight_layout()
    return fig

def fig_output(hasil=None):
    lo, hi = OUTPUT["rentang"]
    x = np.linspace(lo, hi, 1001)
    fig, ax = plt.subplots(figsize=(6, 2.8))
    for nama, spec in OUTPUT["himpunan"].items():
        ax.plot(x, mf(x, spec), color=WARNA[nama], linewidth=2, label=nama)
    if hasil is not None:
        ax.fill_between(hasil["x"], hasil["agregat"], color="gray", alpha=0.35, label="Hasil agregasi")
        ax.axvline(hasil["skor"], color="black", linestyle="--", linewidth=1.2)
        ax.text(hasil["skor"], 1.03, f" skor {hasil['skor']:.1f}", fontsize=9, va="bottom")
    ax.set_title("Output: skor risiko kelelahan (0-100)", fontsize=10)
    ax.set_ylim(-0.02, 1.15); ax.set_ylabel("Derajat keanggotaan", fontsize=8)
    ax.legend(fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    fig.tight_layout()
    return fig
