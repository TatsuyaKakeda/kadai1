from __future__ import annotations

import argparse
import csv
import statistics
import time
from pathlib import Path

from ising2d import Ising2D


def benchmark_one_L(L: int, T: float, n_therm: int, n_meas: int, repeats: int, seed_base: int) -> dict[str, float | int]:
    beta = 1.0 / T
    times_per_mcs: list[float] = []
    for rep in range(repeats):
        model = Ising2D(L=L, seed=seed_base + L * 100 + rep)
        for _ in range(n_therm):
            model.mcs_step(beta)

        t0 = time.perf_counter()
        for _ in range(n_meas):
            model.mcs_step(beta)
        dt = time.perf_counter() - t0
        times_per_mcs.append(dt / n_meas)

    median = statistics.median(times_per_mcs)
    return {
        "L": L,
        "L2": L * L,
        "T": T,
        "n_therm": n_therm,
        "n_meas": n_meas,
        "repeats": repeats,
        "time_per_mcs": median,
    }


def write_benchmark_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["L", "L2", "T", "n_therm", "n_meas", "repeats", "time_per_mcs"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def plot_benchmark(rows: list[dict[str, float | int]], out_prefix: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as e:
        raise RuntimeError("matplotlib is required for plotting") from e

    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    L = [int(r["L"]) for r in rows]
    L2 = [int(r["L2"]) for r in rows]
    t = [float(r["time_per_mcs"]) for r in rows]

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(L, t, marker="o")
    ax1.set_xlabel("L")
    ax1.set_ylabel("time_per_mcs [s]")
    ax1.set_title("time_per_mcs vs L")
    ax1.grid(True, alpha=0.3)
    fig1.savefig(out_prefix.with_name(out_prefix.name + "_vs_L.png"), dpi=150)
    plt.close(fig1)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(L2, t, marker="o")
    ax2.set_xlabel("L^2")
    ax2.set_ylabel("time_per_mcs [s]")
    ax2.set_title("time_per_mcs vs L^2")
    ax2.grid(True, alpha=0.3)
    fig2.savefig(out_prefix.with_name(out_prefix.name + "_vs_L2.png"), dpi=150)
    plt.close(fig2)


def main() -> None:
    p = argparse.ArgumentParser(description="benchmark 1MCS scaling demo")
    p.add_argument("--L", nargs="+", type=int, default=[4, 8, 12, 16])
    p.add_argument("--T", type=float, default=2.3)
    p.add_argument("--n-therm", type=int, default=30)
    p.add_argument("--n-meas", type=int, default=80)
    p.add_argument("--repeats", type=int, default=3)
    p.add_argument("--seed-base", type=int, default=2026)
    p.add_argument("--out-csv", type=Path, default=Path("results/benchmark_demo.csv"))
    p.add_argument("--out-prefix", type=Path, default=Path("results/benchmark_demo"))
    p.add_argument("--skip-plot", action="store_true")
    args = p.parse_args()

    rows = [benchmark_one_L(L, args.T, args.n_therm, args.n_meas, args.repeats, args.seed_base) for L in args.L]
    write_benchmark_csv(args.out_csv, rows)
    print(f"saved benchmark csv: {args.out_csv}")
    if args.skip_plot:
        print("skip plot (--skip-plot)")
    else:
        plot_benchmark(rows, args.out_prefix)
        print(f"saved benchmark plots: {args.out_prefix}_vs_L.png, {args.out_prefix}_vs_L2.png")


if __name__ == "__main__":
    main()
