from analysis import estimate_tc_by_peak
from benchmark_scaling import benchmark_one_L
from sweep_temperature import frange, run_temperature_sweep


def test_frange_count_and_endpoints():
    vals = frange(1.0, 2.0, 5)
    assert len(vals) == 5
    assert abs(vals[0] - 1.0) < 1e-12
    assert abs(vals[-1] - 2.0) < 1e-12


def test_temperature_sweep_row_count():
    rows = run_temperature_sweep([4, 8], [2.0, 2.5, 3.0], n_therm=5, n_meas=8, seed_base=0)
    assert len(rows) == 2 * 3
    required = {"L", "T", "energy_per_spin", "magnetization_per_spin", "specific_heat", "susceptibility"}
    for row in rows:
        assert required.issubset(row.keys())


def test_tc_peak_estimation_synthetic():
    rows = [
        {"L": 4, "T": 2.0, "n_therm": 1, "n_meas": 1, "seed": 0, "energy_per_spin": -1.0, "magnetization_per_spin": 0.8, "specific_heat": 0.5, "susceptibility": 0.7},
        {"L": 4, "T": 2.5, "n_therm": 1, "n_meas": 1, "seed": 0, "energy_per_spin": -0.8, "magnetization_per_spin": 0.6, "specific_heat": 1.1, "susceptibility": 1.4},
        {"L": 8, "T": 2.0, "n_therm": 1, "n_meas": 1, "seed": 0, "energy_per_spin": -1.2, "magnetization_per_spin": 0.9, "specific_heat": 0.6, "susceptibility": 0.8},
        {"L": 8, "T": 2.5, "n_therm": 1, "n_meas": 1, "seed": 0, "energy_per_spin": -0.9, "magnetization_per_spin": 0.5, "specific_heat": 1.2, "susceptibility": 1.5},
    ]
    tc_rows = estimate_tc_by_peak(rows)
    by_L = {int(r["L"]): r for r in tc_rows}
    assert by_L[4]["specific_heat"] == 2.5
    assert by_L[4]["susceptibility"] == 2.5
    assert by_L[8]["specific_heat"] == 2.5
    assert by_L[8]["susceptibility"] == 2.5


def test_benchmark_one_L_positive_time():
    row = benchmark_one_L(L=4, T=2.3, n_therm=2, n_meas=5, repeats=2, seed_base=1)
    assert row["L"] == 4
    assert row["L2"] == 16
    assert float(row["time_per_mcs"]) > 0.0
