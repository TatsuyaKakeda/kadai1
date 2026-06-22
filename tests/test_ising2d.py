import math

from ising2d import Ising2D, simulate


def test_delta_energy_all_up_l4():
    model = Ising2D(L=4, seed=0)
    model.spins = [[1 for _ in range(4)] for _ in range(4)]
    assert model.delta_energy(0, 0) == 8.0


def test_total_energy_all_up_l4():
    model = Ising2D(L=4, seed=0)
    model.spins = [[1 for _ in range(4)] for _ in range(4)]
    assert model.total_energy() == -2.0 * model.N


def test_mcs_preserves_spin_values():
    model = Ising2D(L=8, seed=1)
    model.mcs_step(beta=0.5)
    assert all(s in (-1, 1) for row in model.spins for s in row)


def test_simulation_outputs_finite_values():
    obs = simulate(L=4, T=2.3, n_therm=20, n_meas=50, seed=42)
    assert math.isfinite(obs.energy_per_spin)
    assert math.isfinite(obs.magnetization_per_spin)
    assert math.isfinite(obs.specific_heat)
    assert math.isfinite(obs.susceptibility)
    assert obs.specific_heat >= 0.0
    assert obs.susceptibility >= 0.0


def test_low_temp_more_magnetized_than_high_temp():
    low = simulate(L=8, T=1.5, n_therm=50, n_meas=80, seed=7)
    high = simulate(L=8, T=4.0, n_therm=50, n_meas=80, seed=7)
    assert low.magnetization_per_spin > high.magnetization_per_spin
