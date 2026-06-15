from __future__ import annotations

from collections import defaultdict
from pathlib import Path



def _group_by_L(rows: list[dict]) -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        grouped[int(r["L"])].append(r)
    for L in grouped:
        grouped[L].sort(key=lambda x: float(x["T"]))
    return grouped


def estimate_tc_by_peak(rows: list[dict]) -> list[dict[str, float | int]]:
    grouped = _group_by_L(rows)
    out: list[dict[str, float | int]] = []
    for L, lrows in grouped.items():
        chi_peak = max(lrows, key=lambda x: float(x["susceptibility"]))
        cv_peak = max(lrows, key=lambda x: float(x["specific_heat"]))
        out.append(
            {
                "L": L,
                "T": float("nan"),
                "n_therm": int(lrows[0]["n_therm"]),
                "n_meas": int(lrows[0]["n_meas"]),
                "seed": -1,
                "energy_per_spin": float("nan"),
                "magnetization_per_spin": float("nan"),
                "specific_heat": float(cv_peak["T"]),
                "susceptibility": float(chi_peak["T"]),
            }
        )
    return out


def plot_observables_vs_temperature(rows: list[dict], out_path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as e:
        raise RuntimeError("matplotlib is required for plotting") from e

    grouped = _group_by_L(rows)
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
    ax_e, ax_m, ax_cv, ax_chi = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

    for L, lrows in grouped.items():
        t = [float(r["T"]) for r in lrows]
        e = [float(r["energy_per_spin"]) for r in lrows]
        m = [float(r["magnetization_per_spin"]) for r in lrows]
        cv = [float(r["specific_heat"]) for r in lrows]
        chi = [float(r["susceptibility"]) for r in lrows]

        label = f"L={L}"
        ax_e.plot(t, e, marker="o", ms=3, label=label)
        ax_m.plot(t, m, marker="o", ms=3, label=label)
        ax_cv.plot(t, cv, marker="o", ms=3, label=label)
        ax_chi.plot(t, chi, marker="o", ms=3, label=label)

    ax_e.set_title("Energy per spin")
    ax_m.set_title("Magnetization per spin")
    ax_cv.set_title("Specific heat")
    ax_chi.set_title("Susceptibility")
    for ax in (ax_e, ax_m, ax_cv, ax_chi):
        ax.set_xlabel("T")
        ax.grid(True, alpha=0.3)
        ax.legend()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
