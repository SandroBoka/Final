import os

import numpy as np
from matplotlib import pyplot as plt

days_to_simulate = 150
output_folder_sirv = "graphs_sirv"
output_folder_continues = "graphs_continues"
output_folder_group_specific_uniform = os.path.join(output_folder_sirv, "group_specific_uniform")
output_folder_group_specific_optimal = os.path.join(output_folder_sirv, "group_specific_optimal")
os.makedirs(output_folder_sirv, exist_ok=True)
os.makedirs(output_folder_continues, exist_ok=True)
os.makedirs(output_folder_group_specific_uniform, exist_ok=True)
os.makedirs(output_folder_group_specific_optimal, exist_ok=True)

group = "Uniform Vaccine Allocation (Group-Specific)"
groupPath = "uniform_allocation_group_specific.pdf"

total = "Uniform Vaccine Allocation (Total)"
totalPath = "uniform_allocation_total.pdf"
totalPathContinues = "uniform_allocation_total.pdf"

groupOptimal = "Optimal Vaccine Allocation (Group-Specific)"
groupPathOptimal = "optimal_allocation_group_specific.pdf"

totalOptimal = "Optimal Vaccine Allocation (Total)"
totalPathOptimal = "optimal_allocation_total.pdf"
totalPathOptimalContinues = "optimal_allocation_total.pdf"


def plot(type, allocation, S, I, R):
    if type == "sirv" and allocation == "uniform":
        plot_sir(S, I, R, days_to_simulate, group, groupPath, "uniform")
        plot_total_sir(S, I, R, days_to_simulate, total, os.path.join(output_folder_sirv, totalPath))
    elif type == "sirv" and allocation == "optimal":
        plot_sir(S, I, R, days_to_simulate, groupOptimal, groupPathOptimal, "optimal")
        plot_total_sir(S, I, R, days_to_simulate, totalOptimal, os.path.join(output_folder_sirv, totalPathOptimal))
    else:
        print(f"Wrong type passed: {type}, or wrong allocation passed: {allocation}")


def plot_continues(allocation, S, I, R, t):
    if allocation == "uniform":
        plot_sir_continues(S, I, R, t, "SIRV Model Dynamics Uniform",
                           os.path.join(output_folder_continues, totalPathContinues))
    elif allocation == "optimal":
        plot_sir_continues(S, I, R, t, "SIRV Model Dynamics Optimal",
                           os.path.join(output_folder_continues, totalPathOptimalContinues))
    else:
        print(f"Wrong allocation passed: {allocation}")


def plot_sir(S, I, R, days, title, filename_prefix, allocation_type):
    """
    Plots the SIR model results for each group separately and saves the plots as PDFs in dedicated folders.

    Parameters:
        S, I, R: arrays of susceptible, infected, and recovered counts over time
        days: int, number of days simulated
        title: str, title for the plot
        filename_prefix: str, path prefix to save the plots as PDFs
        allocation_type: str, either 'uniform' or 'optimal' to determine folder structure
    """
    time = np.arange(days)

    output_folder = output_folder_group_specific_uniform if allocation_type == "uniform" else output_folder_group_specific_optimal

    for group in range(S.shape[1]):
        plt.figure(figsize=(20, 12))
        plt.plot(time, S[:, group], label=f"Susceptible (Group {group + 1})", color='blue')
        plt.plot(time, I[:, group], label=f"Infected (Group {group + 1})", color='red')
        plt.plot(time, R[:, group], label=f"Recovered (Group {group + 1})", color='green')

        plt.xlabel("Days")
        plt.ylabel("Population")
        plt.xticks(np.arange(0, days + 1, 5))
        plt.title(f"{title} - Group {group + 1}")
        plt.legend()
        plt.grid(True)

        filename = os.path.join(output_folder, f"{filename_prefix}_group_{group + 1}.pdf")
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

    plt.figure(figsize=(20, 12))
    plt.plot(time, total_S, label="Total Susceptible", color='blue')
    plt.plot(time, total_I, label="Total Infected", color='red')
    plt.plot(time, total_R, label="Total Recovered", color='green')

    plt.xlabel("Days")
    plt.ylabel("Total Population")
    plt.xticks(np.arange(0, days + 1, 5))
    plt.title(title)
    plt.legend()
    plt.grid(True)

    if filename:
        plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()


def plot_sir_continues(S, I, R, t, title, filename):
    plt.figure(figsize=(20, 12))
    plt.plot(t, I.sum(axis=1), label="Infected")
    plt.plot(t, S.sum(axis=1), label="Susceptible")
    plt.plot(t, R.sum(axis=1), label="Recovered")
    plt.xlabel("Days")
    plt.xticks(np.arange(0, days_to_simulate + 1, 5))
    plt.ylabel("Population")
    plt.title(title)
    plt.grid(True)
    plt.legend()

    plt.savefig(filename, format='pdf', bbox_inches='tight')
    plt.show()
