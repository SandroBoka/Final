import os

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------- Predefined Parameters ---------------------------------------------

contact_matrix = np.array([
    [1, 4, 4],
    [2, 8, 8],
    [4, 16, 16]
])

group_size_fractions = np.array([0.25, 0.5, 0.25])  # low contact group, medium contact group, high contact group

susceptibility = np.array([1, 1, 1])  # paper also uses 1

infectivity = np.array([1, 1, 1])  # paper also uses 1

initially_infected = np.array([1, 2, 4])  # Initial infected individuals in each group

# ---------------------------------------- User Input Parameters ---------------------------------------------

population = int(input("Enter population size: "))

reproduction_number = float(input("Enter R0: "))

recovery_rate = float(input("Enter recovery rate, 1/(duration of infection): "))

vaccine_coverage_fraction = float(input("Enter the fraction of the population that can be vaccinated (e.g., 0.4): "))

vaccine_efficacy = float(input("Enter the vaccine efficacy (e.g., 0.8 for 80%): "))

# ---------------------------------------- Calculated Parameters ---------------------------------------------

group_sizes = group_size_fractions * population

next_generation_matrix = np.zeros_like(contact_matrix, dtype=float)
for j in range(len(contact_matrix)):
    for k in range(len(contact_matrix)):
        next_generation_matrix[j, k] = (susceptibility[j] * infectivity[k] * contact_matrix[j, k]) / \
                                       group_size_fractions[k]

spectral_radius = max(np.linalg.eigvals(next_generation_matrix).real)

transmission_rate = (reproduction_number * recovery_rate) / spectral_radius

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


# ------------------------------------------- SIR Model ----------------------------------------------------

def run_sir_model(group_sizes, initially_infected, vaccine_allocation, susceptibility, transmission_rate,
                  recovery_rate, days):
    """
    Runs the SIR model for the given parameters.

    Parameters:
        group_sizes: array, sizes of each group
        initially_infected: array, initial infected individuals in each group
        vaccine_allocation: array, number of vaccines allocated to each group
        susceptibility: array, representing each group susceptibility to infection
        transmission_rate: float, transmission rate (beta)
        recovery_rate: float, recovery rate (gamma)
        days: int, number of days to simulate

    Returns:
        S, I, R: arrays with susceptible, infected, and recovered counts over time
    """
    num_groups = len(group_sizes)
    S = np.zeros((days, num_groups))
    I = np.zeros((days, num_groups))
    R = np.zeros((days, num_groups))

    adjusted_susceptibility = susceptibility - (vaccine_allocation / group_sizes) * susceptibility * vaccine_efficacy

    # Initial conditions
    S[0, :] = group_sizes - initially_infected - vaccine_allocation * vaccine_efficacy
    I[0, :] = initially_infected
    R[0, :] = 0

    for t in range(1, days):
        for j in range(num_groups):
            # Force of infection for group j
            force_of_infection = transmission_rate * adjusted_susceptibility[j] * sum(
                contact_matrix[j, k] * I[t - 1, k] / group_sizes[k] for k in range(num_groups)
            )

            # Changes
            dS = -force_of_infection * S[t - 1, j]
            dI = force_of_infection * S[t - 1, j] - recovery_rate * I[t - 1, j]
            dR = recovery_rate * I[t - 1, j]

            # Update states
            S[t, j] = max(S[t - 1, j] + dS, 0)  # Ensure no negative susceptible
            I[t, j] = max(I[t - 1, j] + dI, 0)  # Ensure no negative infected
            R[t, j] = max(R[t - 1, j] + dR, 0)  # Ensure no negative recovered

    # total_infected = np.sum(I[-1, :])
    # print(f"Total number of infected individuals at the end of simulation: {total_infected}")
    # for group in range(num_groups):
    #     print(f"Group {group + 1} infected: {I[-1, group]}")

    return S, I, R


# ------------------------------------------- SIRV Model ----------------------------------------------------

def run_sirv_model(group_sizes, initially_infected, vaccine_allocation, transmission_rate,
                   recovery_rate, vaccine_efficacy, contact_matrix, days):
    """
    Runs the SIRV model for the given parameters, accounting for partial protection from vaccination.

    Parameters:
        group_sizes: array, sizes of each group
        initially_infected: array, initial infected individuals in each group
        vaccine_allocation: array, number of vaccines allocated to each group
        transmission_rate: float, transmission rate (beta)
        recovery_rate: float, recovery rate (gamma)
        vaccine_efficacy: float, vaccine efficacy (1 - epsilon)
        contact_matrix: matrix, contact rates between groups
        days: int, number of days to simulate

    Returns:
        S, I, R: arrays with susceptible, infected, and recovered counts over time
    """
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

    for t in range(1, days):
        for j in range(num_groups):
            # Force of infection for group j
            force_of_infection = transmission_rate * sum(
                contact_matrix[j, k] * I[t - 1, k] / group_sizes[k] for k in range(num_groups)
            )

            # Changes for group j
            dS = -force_of_infection * S[t - 1, j]
            dV = -force_of_infection * (1 - vaccine_efficacy) * V[t - 1, j]  # Partial susceptibility
            dI = force_of_infection * (S[t - 1, j] + (1 - vaccine_efficacy) * V[t - 1, j]) - recovery_rate * I[t - 1, j]
            dR = recovery_rate * I[t - 1, j]

            # Update states
            S[t, j] = max(S[t - 1, j] + dS, 0)
            V[t, j] = max(V[t - 1, j] + dV, 0)
            I[t, j] = max(I[t - 1, j] + dI, 0)
            R[t, j] = max(R[t - 1, j] + dR, 0)

    return S, I, R


# ------------------------------------------- Plotting ----------------------------------------------------

def plot_sir(S, I, R, days, title, filename=None):
    """
    Plots the SIR model results for each group and optionally saves the plot as a PDF.

    Parameters:
        S, I, R: arrays of susceptible, infected, and recovered counts over time
        days: int, number of days simulated
        title: str, title for the plot
        filename: str, optional, path to save the plot as a PDF
    """
    time = np.arange(days)
    plt.figure(figsize=(10, 6))
    for group in range(S.shape[1]):
        plt.plot(time, S[:, group], label=f"Susceptible (Group {group + 1})")
        plt.plot(time, I[:, group], label=f"Infected (Group {group + 1})")
        plt.plot(time, R[:, group], label=f"Recovered (Group {group + 1})")

    plt.xlabel("Days")
    plt.ylabel("Population")
    plt.xticks(np.arange(0, days_to_simulate + 1, 25))
    plt.title(title)
    plt.legend()
    plt.grid(True)

    if filename:
        plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()


def plot_total_sir(S, I, R, days, title, filename=None):
    """
    Plots the total number of susceptible, infected, and recovered across all groups
    and optionally saves the plot as a PDF.

    Parameters:
        S, I, R: arrays of susceptible, infected, and recovered counts over time
        days: int, number of days simulated
        title: str, title for the plot
        filename: str, optional, path to save the plot as a PDF
    """
    time = np.arange(days)
    total_S = np.sum(S, axis=1)  # Sum across all groups
    total_I = np.sum(I, axis=1)
    total_R = np.sum(R, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(time, total_S, label="Total Susceptible", color='blue')
    plt.plot(time, total_I, label="Total Infected", color='red')
    plt.plot(time, total_R, label="Total Recovered", color='green')

    plt.xlabel("Days")
    plt.ylabel("Total Population")
    plt.xticks(np.arange(0, days_to_simulate + 1, 25))
    plt.title(title)
    plt.legend()
    plt.grid(True)

    if filename:
        plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()


# ------------------------------------------- Main ----------------------------------------------------

if __name__ == "__main__":
    # Simulation parameters
    days_to_simulate = 300
    output_folder = "graphs"
    output_folder_sirv = "graphs_sirv"
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(output_folder_sirv, exist_ok=True)

    # Uniform vaccine allocation
    vaccine_allocation_uniform = uniform_allocation(total_vaccines, group_sizes)

    S_uniform, I_uniform, R_uniform = run_sir_model(
        group_sizes, initially_infected, vaccine_allocation_uniform, susceptibility,
        transmission_rate, recovery_rate, days_to_simulate
    )

    S_uniform_numerical, I_uniform_numerical, R_uniform_numerical = run_sirv_model(
        group_sizes, initially_infected, vaccine_allocation_uniform,
        transmission_rate, recovery_rate, vaccine_efficacy, contact_matrix, days_to_simulate
    )

    # Optimal vaccine allocation
    vaccine_allocation_optimal = optimal_allocation(total_vaccines, group_sizes, exposure_index)

    S_optimal, I_optimal, R_optimal = run_sir_model(
        group_sizes, initially_infected, vaccine_allocation_optimal, susceptibility,
        transmission_rate, recovery_rate, days_to_simulate
    )

    S_optimal_numerical, I_optimal_numerical, R_optimal_numerical = run_sirv_model(
        group_sizes, initially_infected, vaccine_allocation_optimal,
        transmission_rate, recovery_rate, vaccine_efficacy, contact_matrix, days_to_simulate
    )

    # Plot and save results for each group (Uniform Allocation)
    plot_sir(S_uniform, I_uniform, R_uniform, days_to_simulate,
             "Uniform Vaccine Allocation (Group-Specific)",
             filename=os.path.join(output_folder, "uniform_allocation_group_specific.pdf"))
    plot_sir(S_uniform_numerical, I_uniform_numerical, R_uniform_numerical, days_to_simulate,
             "Uniform Vaccine Allocation (Group-Specific)",
             filename=os.path.join(output_folder_sirv, "uniform_allocation_group_specific.pdf"))

    # Plot and save results for each group (Optimal Allocation)
    plot_sir(S_optimal, I_optimal, R_optimal, days_to_simulate,
             "Optimal Vaccine Allocation (Group-Specific)",
             filename=os.path.join(output_folder, "optimal_allocation_group_specific.pdf"))
    plot_sir(S_optimal_numerical, I_optimal_numerical, R_optimal_numerical, days_to_simulate,
             "Optimal Vaccine Allocation (Group-Specific)",
             filename=os.path.join(output_folder_sirv, "optimal_allocation_group_specific.pdf"))

    # Plot and save total results (Uniform Allocation)
    plot_total_sir(S_uniform, I_uniform, R_uniform, days_to_simulate,
                   "Uniform Vaccine Allocation (Total)",
                   filename=os.path.join(output_folder, "uniform_allocation_total.pdf"))
    plot_total_sir(S_uniform_numerical, I_uniform_numerical, R_uniform_numerical, days_to_simulate,
                   "Uniform Vaccine Allocation (Total)",
                   filename=os.path.join(output_folder_sirv, "uniform_allocation_total.pdf"))

    # Plot and save total results (Optimal Allocation)
    plot_total_sir(S_optimal, I_optimal, R_optimal, days_to_simulate,
                   "Optimal Vaccine Allocation (Total)",
                   filename=os.path.join(output_folder, "optimal_allocation_total.pdf"))
    plot_total_sir(S_optimal_numerical, I_optimal_numerical, R_optimal_numerical, days_to_simulate,
                   "Optimal Vaccine Allocation (Total)",
                   filename=os.path.join(output_folder_sirv, "optimal_allocation_total.pdf"))
