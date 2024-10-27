# model.py

import numpy as np
from scipy.integrate import odeint


class SIRModel:
    def __init__(self, population, R0, gamma, vaccine_coverage, vaccine_efficacy):
        self.N = population
        self.R0 = R0
        self.gamma = gamma
        self.vaccine_coverage = vaccine_coverage
        self.vaccine_efficacy = vaccine_efficacy
        self.beta = self.R0 * self.gamma  # Calculate infection rate

    def simulate(self):
        # Initial conditions
        I0 = 1  # Initial number of infected individuals
        R_init = 0  # Initial number of recovered individuals
        S0 = self.N - I0 - R_init  # Initial susceptible population
        V = S0 * self.vaccine_coverage * self.vaccine_efficacy  # Effective vaccinated population
        S0 -= V  # Adjust susceptible population

        # Differential equations for SIR model
        def sir_model(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I
            return dSdt, dIdt, dRdt

        # Initial conditions vector
        y0 = S0, I0, R_init

        # Time points (days)
        t = np.linspace(0, 160, 160)

        # Integrate the SIR equations over the time grid, t.
        result = odeint(sir_model, y0, t, args=(self.N, self.beta, self.gamma))
        S, I, R = result.T

        return t, S, I, R
