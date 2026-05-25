from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

from ising2d import simulate
from analysis import estimate_tc_by_peak, plot_observables_vs_temperature


def frange(start: float, stop: float, num: int) -> list[float]:
    if num < 2:
        return [start]
    step = (stop - start) / (num - 1)
    return [start + i * step for i in range(num)]


def run_temperature_sweep(
    L_list: Iterable[int],
    T_list: Iterable[float],
    n_therm: int,
    n_meas: int,
    seed_base: int,
) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for L in L_list:
        for i_t, T in enumerate(T_list):
            seed = seed_base + 1000 * L + i_t
            obs = simulate(L=L, T=T, n_therm=n_therm, n_meas=n_meas, seed=seed)
            rows.append(
                {
                    "L": L,
                    "T": T,
                    "n_therm": n_therm,
                    "n_meas": n_meas,
                    "seed": seed,
                    "energy_per_spin": obs.energy_per_spin,
                    "magnetization_per_spin": obs.magnetization_per_spin,
                    "specific_heat": obs.specific_heat,
                    "susceptibility": obs.susceptibility,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "L",
        "T",
        "n_therm",
        "n_meas",
        "seed",
        "energy_per_spin",
        "magnetization_per_spin",
        "specific_heat",
        "susceptibility",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="2D Ising temperature sweep (demo)")
    p.add_argument("--L", nargs="+", type=int, default=[4, 8, 12])
    p.add_argument("--T-min", type=float, default=1.6)
    p.add_argument("--T-max", type=float, default=3.4)
    p.add_argument("--nT", type=int, default=13)
    p.add_argument("--n-therm", type=int, default=80)
    p.add_argument("--n-meas", type=int, default=120)
    p.add_argument("--seed-base", type=int, default=1234)
    p.add_argument("--out-csv", type=Path, default=Path("results/sweep_demo.csv"))
    p.add_argument("--out-fig", type=Path, default=Path("results/observables_demo.png"))
    p.add_argument("--out-tc-csv", type=Path, default=Path("results/tc_estimates_demo.csv"))
    p.add_argument("--skip-plot", action="store_true")
    return p


def main() -> None:
    args = build_parser().parse_args()
    T_list = frange(args.T_min, args.T_max, args.nT)
    rows = run_temperature_sweep(args.L, T_list, args.n_therm, args.n_meas, args.seed_base)
    write_csv(args.out_csv, rows)
    tc_rows = estimate_tc_by_peak(rows)
    write_csv(args.out_tc_csv, tc_rows)
    print(f"saved sweep csv: {args.out_csv}")
    print(f"saved Tc estimates: {args.out_tc_csv}")
    if args.skip_plot:
        print("skip plot (--skip-plot)")
    else:
        plot_observables_vs_temperature(rows, args.out_fig)
        print(f"saved plot: {args.out_fig}")


if __name__ == "__main__":
    main()
