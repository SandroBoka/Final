# view.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SIRView:
    def __init__(self, root):
        self.root = root
        self.root.title("SIR Model with Vaccination")

        # Labels and Entry widgets for parameters
        tk.Label(root, text="Population (N)").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.population_entry = tk.Entry(root)
        self.population_entry.grid(row=0, column=1, padx=10, pady=5)
        self.population_entry.insert(0, "1000")

        tk.Label(root, text="Basic Reproduction Number (R0)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.R0_entry = tk.Entry(root)
        self.R0_entry.grid(row=1, column=1, padx=10, pady=5)
        self.R0_entry.insert(0, "3.0")

        tk.Label(root, text="Recovery Rate (gamma)").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.gamma_entry = tk.Entry(root)
        self.gamma_entry.grid(row=2, column=1, padx=10, pady=5)
        self.gamma_entry.insert(0, "0.1")

        tk.Label(root, text="Vaccine Coverage (%)").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.vaccine_coverage_entry = tk.Entry(root)
        self.vaccine_coverage_entry.grid(row=3, column=1, padx=10, pady=5)
        self.vaccine_coverage_entry.insert(0, "0.6")

        tk.Label(root, text="Vaccine Efficacy (%)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.vaccine_efficacy_entry = tk.Entry(root)
        self.vaccine_efficacy_entry.grid(row=4, column=1, padx=10, pady=5)
        self.vaccine_efficacy_entry.insert(0, "0.8")

        # Error label
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.grid(row=5, columnspan=2)

        # Button to run simulation
        self.run_button = ttk.Button(root, text="Run Simulation")
        self.run_button.grid(row=6, columnspan=2, pady=10)

        # Frame to hold the plot
        self.plot_frame = tk.Frame(root)
        self.plot_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def display_error(self, message):
        self.error_label.config(text=message)

    def get_parameters(self):
        return {
            "population": int(self.population_entry.get()),
            "R0": float(self.R0_entry.get()),
            "gamma": float(self.gamma_entry.get()),
            "vaccine_coverage": float(self.vaccine_coverage_entry.get()),
            "vaccine_efficacy": float(self.vaccine_efficacy_entry.get())
        }

    def display_results(self, t, S, I, R):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create figure and plot results
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(t, S, 'b', label='Susceptible')
        ax.plot(t, I, 'r', label='Infected')
        ax.plot(t, R, 'g', label='Recovered')
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Population')
        ax.set_title('SIR Model with Vaccination')
        ax.legend()
        ax.grid()

        # Display plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
