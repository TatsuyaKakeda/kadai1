from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class Observables:
    energy_per_spin: float
    magnetization_per_spin: float
    specific_heat: float
    susceptibility: float


class Ising2D:
    def __init__(self, L: int, J: float = 1.0, seed: int | None = None) -> None:
        if L <= 0:
            raise ValueError("L must be positive")
        self.L = L
        self.N = L * L
        self.J = J
        self.rng = random.Random(seed)
        self.spins = [[self.rng.choice([-1, 1]) for _ in range(L)] for _ in range(L)]

    def delta_energy(self, x: int, y: int) -> float:
        s = self.spins[x][y]
        nn = (
            self.spins[(x + 1) % self.L][y]
            + self.spins[(x - 1) % self.L][y]
            + self.spins[x][(y + 1) % self.L]
            + self.spins[x][(y - 1) % self.L]
        )
        return 2.0 * self.J * s * nn

    def metropolis_attempt(self, x: int, y: int, beta: float) -> bool:
        dE = self.delta_energy(x, y)
        if dE <= 0 or self.rng.random() < math.exp(-beta * dE):
            self.spins[x][y] *= -1
            return True
        return False

    def mcs_step(self, beta: float) -> int:
        accepted = 0
        for _ in range(self.N):
            x = self.rng.randrange(self.L)
            y = self.rng.randrange(self.L)
            accepted += int(self.metropolis_attempt(x, y, beta))
        return accepted

    def total_energy(self) -> float:
        e = 0.0
        for x in range(self.L):
            for y in range(self.L):
                s = self.spins[x][y]
                right = self.spins[x][(y + 1) % self.L]
                down = self.spins[(x + 1) % self.L][y]
                e += -self.J * s * (right + down)
        return e

    def total_magnetization(self) -> int:
        return sum(sum(row) for row in self.spins)


def simulate(L: int, T: float, n_therm: int, n_meas: int, J: float = 1.0, seed: int | None = None) -> Observables:
    if T <= 0:
        raise ValueError("T must be positive")
    if n_therm < 0 or n_meas <= 0:
        raise ValueError("n_therm must be >= 0 and n_meas > 0")

    model = Ising2D(L=L, J=J, seed=seed)
    beta = 1.0 / T

    for _ in range(n_therm):
        model.mcs_step(beta)

    energies = []
    mags = []
    abs_mags = []
    for _ in range(n_meas):
        model.mcs_step(beta)
        E = model.total_energy()
        M = model.total_magnetization()
        energies.append(E)
        mags.append(M)
        abs_mags.append(abs(M))

    N = model.N
    e_mean = sum(energies) / len(energies)
    e2_mean = sum(e * e for e in energies) / len(energies)
    m2_mean = sum(m * m for m in mags) / len(mags)
    m_abs_mean = sum(abs_mags) / len(abs_mags)

    return Observables(
        energy_per_spin=e_mean / N,
        magnetization_per_spin=m_abs_mean / N,
        specific_heat=(beta * beta / N) * (e2_mean - e_mean * e_mean),
        susceptibility=(beta / N) * (m2_mean - m_abs_mean * m_abs_mean),
    )
