from ising2d import simulate


def main() -> None:
    for L in (4, 8):
        obs = simulate(L=L, T=2.3, n_therm=100, n_meas=200, seed=123)
        print(f"L={L}")
        print(f"  energy/spin      = {obs.energy_per_spin:.6f}")
        print(f"  magnetization    = {obs.magnetization_per_spin:.6f}")
        print(f"  specific heat    = {obs.specific_heat:.6f}")
        print(f"  susceptibility   = {obs.susceptibility:.6f}")


if __name__ == "__main__":
    main()
