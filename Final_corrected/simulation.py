import os

import numpy as np
from scipy.integrate import odeint

from plotting import plot, plot_continues

# ---------------------------------------- Predefined Parameters ---------------------------------------------

contact_matrix = np.array([
    [1, 4, 4],
    [2, 8, 8],
    [4, 16, 16]
])

group_size_fractions = np.array([0.25, 0.5, 0.25])  # low contact group, medium contact group, high contact group

susceptibility = np.array([1, 1, 1])  # paper also uses 1

infectivity = np.array([1, 1, 1])  # paper also uses 1

initially_infected = np.array([1, 2, 1])  # Initial infected individuals in each group

# ---------------------------------------- User Input Parameters ---------------------------------------------

population = int(input("Enter population size: "))

beta = float(input("Enter infection/transmission rate (beta): "))

gamma = float(input("Enter recovery rate (gamma), 1/(duration of infection): "))

vaccine_coverage_fraction = float(input("Enter the fraction of the population that can be vaccinated (e.g., 0.4): "))

vaccine_efficacy = float(input("Enter the vaccine efficacy (e.g., 0.8 for 80%): "))

# ---------------------------------------- Calculated Parameters ---------------------------------------------

M = (beta / gamma) * contact_matrix

R0 = np.linalg.eigvals(M).max()

print(f"Reproduction number (R0) is: {R0:.2f}")

group_sizes = group_size_fractions * population

exposure_index = np.array(
    [susceptibility[j] * sum(contact_matrix[j, :] * infectivity) for j in range(len(contact_matrix))])

total_vaccines = vaccine_coverage_fraction * population

# ---------------------------------------- Allocation Functions --------------------------------------------

def uniform_allocation(total_vaccines, group_sizes):
    return total_vaccines * (group_sizes / group_sizes.sum())


def optimal_allocation(total_vaccines, group_sizes, exposure_index):
    """
    Optimal allocation of vaccines based on exposure index.
    Vaccines are distributed to groups with the lowest exposure index first.
    """
    sorted_indices = np.argsort(exposure_index)  # Sort groups by exposure index (ascending)
    allocation = np.zeros_like(group_sizes)

    remaining_vaccines = total_vaccines
    for i in sorted_indices:
        max_vaccines = group_sizes[i]  # At most, we can vaccinate the entire group
        allocation_to_group = min(remaining_vaccines, max_vaccines)
        allocation[i] = allocation_to_group
        remaining_vaccines -= allocation_to_group
        if remaining_vaccines <= 0:
            break

    return allocation


# ------------------------------------------- SIRV Model ----------------------------------------------------

def run_sirv_model(group_sizes, initially_infected, vaccine_allocation, beta,
                   gamma, vaccine_efficacy, contact_matrix, days):

    num_groups = len(group_sizes)
    S = np.zeros((days, num_groups))
    V = np.zeros((days, num_groups))
    I = np.zeros((days, num_groups))
    R = np.zeros((days, num_groups))

    # Initial conditions
    S[0, :] = group_sizes - initially_infected - vaccine_allocation
    V[0, :] = vaccine_allocation
    I[0, :] = initially_infected
    R[0, :] = 0

    # D_jk matrix using absolute group sizes needed here
    D_matrix = np.zeros_like(contact_matrix, dtype=float)
    for j in range(num_groups):
        for k in range(num_groups):
            D_matrix[j, k] = (susceptibility[j] * infectivity[k] * contact_matrix[j, k]) / group_sizes[k]

    for t in range(1, days):
        for j in range(num_groups):
            # Force of infection for group j
            force_of_infection = beta * sum(
                D_matrix[j, k] * I[t - 1, k] for k in range(num_groups)
            )

            # Changes for group j
            dS = -force_of_infection * S[t - 1, j]
            dV = -force_of_infection * (1 - vaccine_efficacy) * V[t - 1, j]  # Partial susceptibility
            dI = force_of_infection * (S[t - 1, j] + (1 - vaccine_efficacy) * V[t - 1, j]) - gamma * I[t - 1, j]
            dR = gamma * I[t - 1, j]

            # Update states
            S[t, j] = max(S[t - 1, j] + dS, 0)
            V[t, j] = max(V[t - 1, j] + dV, 0)
            I[t, j] = max(I[t - 1, j] + dI, 0)
            R[t, j] = max(R[t - 1, j] + dR, 0)

    return S, I, R


def run_sirv_model_continuous(group_sizes, initially_infected, vaccine_allocation, beta,
                              gamma, vaccine_efficacy, contact_matrix, t_max):

    # Initial conditions
    num_groups = len(group_sizes)

    S = group_sizes - initially_infected - vaccine_allocation
    V = vaccine_allocation
    I = initially_infected
    R = np.zeros(num_groups)

    D_matrix = np.zeros_like(contact_matrix, dtype=float)
    for j in range(num_groups):
        for k in range(num_groups):
            D_matrix[j, k] = (susceptibility[j] * infectivity[k] * contact_matrix[j, k]) / group_sizes[k]

    t = np.linspace(0, t_max, t_max * 1000)

    def sirv_derivatives(y, t):
        S, V, I, R = np.split(y, 4)
        dS = np.zeros(num_groups)
        dV = np.zeros(num_groups)
        dI = np.zeros(num_groups)
        dR = np.zeros(num_groups)

        for j in range(num_groups):
            # Force of infection for group j
            force_of_infection = beta * sum(
                D_matrix[j, k] * I[k] for k in range(num_groups)
            )

            # Differential equations
            dS[j] = -force_of_infection * S[j]
            dV[j] = -force_of_infection * (1 - vaccine_efficacy) * V[j]
            dI[j] = force_of_infection * (S[j] + (1 - vaccine_efficacy) * V[j]) - gamma * I[j]
            dR[j] = gamma * I[j]

        return np.concatenate([dS, dV, dI, dR])

    result = odeint(sirv_derivatives, np.concatenate([S, V, I, R]), t)
    S, V, I, R = np.split(result, 4, axis=1)

    return t, S, I, R


# ------------------------------------------- Main ----------------------------------------------------

if __name__ == "__main__":
    # Simulation parameters
    days_to_simulate = 150

    # Uniform vaccine allocation
    vaccine_allocation_uniform = uniform_allocation(total_vaccines, group_sizes)

    S_uniform_numerical, I_uniform_numerical, R_uniform_numerical = run_sirv_model(
        group_sizes, initially_infected, vaccine_allocation_uniform,
        beta, gamma, vaccine_efficacy, contact_matrix, days_to_simulate
    )
    plot("sirv", "uniform", S_uniform_numerical, I_uniform_numerical, R_uniform_numerical)

    # Optimal vaccine allocation
    vaccine_allocation_optimal = optimal_allocation(total_vaccines, group_sizes, exposure_index)

    S_optimal_numerical, I_optimal_numerical, R_optimal_numerical = run_sirv_model(
        group_sizes, initially_infected, vaccine_allocation_optimal,
        beta, gamma, vaccine_efficacy, contact_matrix, days_to_simulate
    )
    plot("sirv", "optimal", S_optimal_numerical, I_optimal_numerical, R_optimal_numerical)

    t, S, I, R = run_sirv_model_continuous(group_sizes, initially_infected, vaccine_allocation_uniform,
                                           beta, gamma, vaccine_efficacy, contact_matrix, days_to_simulate)
    plot_continues("uniform", S, I, R, t)

    t, S, I, R = run_sirv_model_continuous(group_sizes, initially_infected, vaccine_allocation_optimal,
                                           beta, gamma, vaccine_efficacy, contact_matrix, days_to_simulate)
    plot_continues("optimal", S, I, R, t)
