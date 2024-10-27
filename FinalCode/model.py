import numpy as np
from scipy.integrate import odeint


class SIRModel:
    def __init__(self, population, R0, gamma, vaccine_coverage, vaccine_efficacy, optimal_allocation=False):
        self.N = population
        self.R0 = R0
        self.gamma = gamma
        self.vaccine_coverage = vaccine_coverage
        self.vaccine_efficacy = vaccine_efficacy
        self.optimal_allocation = optimal_allocation
        self.beta = self.R0 * self.gamma  # Infection rate

    def herd_immunity_threshold(self):
        """Calculate the critical vaccination proportion for herd immunity."""
        return (1 - (1 / self.R0)) * self.N

    def simulate(self):
        # Initial conditions
        I0 = 1  # Initial number of infected individuals
        R_init = 0  # Initial number of recovered individuals
        S0 = self.N - I0 - R_init  # Initial susceptible population

        # Adjust susceptible population for vaccinated proportion
        V = S0 * self.vaccine_coverage * self.vaccine_efficacy if not self.optimal_allocation else self.optimal_vaccine_allocation()
        S0 -= V  # Adjust susceptible population after vaccination

        # Differential equations for the SIR model
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

    def optimal_vaccine_allocation(self):
        """Simulate a counterintuitive vaccine allocation approach for high R0."""
        # Placeholder logic; you would replace with actual optimal allocation strategy calculations
        if self.R0 > 5:
            # Prioritize lower-contact groups (reduce vaccination for higher contact groups)
            return self.vaccine_coverage * 0.8
        return self.vaccine_coverage
