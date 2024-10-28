import numpy as np
from scipy.integrate import odeint


class SIRModel:
    def __init__(self, population, R0, gamma, vaccine_coverage, vaccine_efficacy, optimal_allocation=False,
                 group_percentages=None, contact_matrix=None, waning_rate=0.0):
        self.N = population
        self.R0 = R0
        self.gamma = gamma
        self.vaccine_coverage = vaccine_coverage
        self.vaccine_efficacy = vaccine_efficacy
        self.optimal_allocation = optimal_allocation
        self.beta = self.R0 * self.gamma  # Calculate infection rate
        self.waning_rate = waning_rate  # Rate at which immunity wanes

        # Group setup with exposure index-based prioritization
        self.group_percentages = group_percentages if group_percentages else [0.33, 0.33, 0.34]
        self.groups = [
            {"fraction": self.group_percentages[0], "contact_rate": 0.5, "susceptibility": 0.9},
            {"fraction": self.group_percentages[1], "contact_rate": 1.0, "susceptibility": 1.0},
            {"fraction": self.group_percentages[2], "contact_rate": 2.0, "susceptibility": 1.1}
        ]

        # Default contact matrix if none provided
        if contact_matrix is None:
            self.contact_matrix = np.array([
                [0.5, 0.2, 0.1],
                [0.2, 1.0, 0.3],
                [0.1, 0.3, 2.0]
            ])
        else:
            self.contact_matrix = np.array(contact_matrix)

    def herd_immunity_threshold(self):
        """Calculate herd immunity threshold based on R0."""
        return 1 - (1 / self.R0)

    def optimal_vaccine_allocation(self):
        """Allocate vaccines optimally based on exposure index and R0 threshold."""
        total_vaccines = self.N * self.vaccine_coverage * self.vaccine_efficacy
        allocation = []

        # Calculate exposure index for each group
        exposure_indices = [
            group["susceptibility"] * np.sum(self.contact_matrix[idx]) for idx, group in enumerate(self.groups)
        ]

        # For high R0, prioritize low exposure index groups
        if self.R0 > 5:
            groups_sorted = sorted(range(len(self.groups)), key=lambda i: exposure_indices[i])
            for i in groups_sorted:
                group_vaccines = total_vaccines * self.groups[i]["fraction"]
                allocation.append(group_vaccines)
                total_vaccines -= group_vaccines
        else:
            # Allocate proportionally for lower R0
            for group in self.groups:
                allocation.append(total_vaccines * group["fraction"])

        return allocation

    def simulate(self, t_max=160):
        # Initial vaccine allocation setup
        allocations = self.optimal_vaccine_allocation() if self.optimal_allocation else [
                                                                                            self.N * self.vaccine_coverage * self.vaccine_efficacy
                                                                                        ] * len(self.groups)

        # Initialize results
        results = []
        t = np.linspace(0, t_max, t_max)

        for idx, group in enumerate(self.groups):
            group_size = self.N * group["fraction"]
            V = allocations[idx] * self.vaccine_efficacy
            S0 = group_size - V  # Susceptible after accounting for vaccinated

            # Initial small infection seed
            I0 = group_size * 0.001
            R0 = 0
            y0 = S0, I0, R0, V

            # SIRV model with waning immunity
            def sir_model(y, t, N, beta, gamma, contact_rate, waning_rate):
                S, I, R, V = y
                dSdt = -beta * S * I * contact_rate / N + waning_rate * V
                dIdt = beta * S * I * contact_rate / N - gamma * I
                dRdt = gamma * I
                dVdt = -waning_rate * V  # Waning immunity effect
                return dSdt, dIdt, dRdt, dVdt

            # Integrate dynamics over time
            result = odeint(sir_model, y0, t,
                            args=(group_size, self.beta, self.gamma, group["contact_rate"], self.waning_rate))
            results.append(result.T)

        return t, results, allocations
