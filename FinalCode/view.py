import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SIRView:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced SIR Model with Vaccination")

        # Frame for scrolling if needed
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Create a frame for user inputs
        input_frame = tk.Frame(self.scrollable_frame)
        input_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Population
        tk.Label(input_frame, text="Population (N):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.population_entry = tk.Entry(input_frame)
        self.population_entry.grid(row=0, column=1, padx=10, pady=5)
        self.population_entry.insert(0, "1000")

        # Basic Reproduction Number (R0)
        tk.Label(input_frame, text="Basic Reproduction Number (R0):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.R0_entry = tk.Entry(input_frame)
        self.R0_entry.grid(row=1, column=1, padx=10, pady=5)
        self.R0_entry.insert(0, "3.0")

        # Recovery Rate (gamma)
        tk.Label(input_frame, text="Recovery Rate (gamma):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.gamma_entry = tk.Entry(input_frame)
        self.gamma_entry.grid(row=2, column=1, padx=10, pady=5)
        self.gamma_entry.insert(0, "0.1")

        # Vaccine Coverage
        tk.Label(input_frame, text="Vaccine Coverage (%):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.vaccine_coverage_entry = tk.Entry(input_frame)
        self.vaccine_coverage_entry.grid(row=3, column=1, padx=10, pady=5)
        self.vaccine_coverage_entry.insert(0, "60")  # As percentage

        # Vaccine Efficacy
        tk.Label(input_frame, text="Vaccine Efficacy (%):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.vaccine_efficacy_entry = tk.Entry(input_frame)
        self.vaccine_efficacy_entry.grid(row=4, column=1, padx=10, pady=5)
        self.vaccine_efficacy_entry.insert(0, "80")  # As percentage

        # Waning Immunity Rate
        tk.Label(input_frame, text="Waning Immunity Rate:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.waning_rate_entry = tk.Entry(input_frame)
        self.waning_rate_entry.grid(row=5, column=1, padx=10, pady=5)
        self.waning_rate_entry.insert(0, "0.05")

        # Group percentages for different contact rates
        tk.Label(input_frame, text="Group 1 (Low Contact) %:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.group1_entry = tk.Entry(input_frame)
        self.group1_entry.grid(row=6, column=1, padx=10, pady=5)
        self.group1_entry.insert(0, "25")  # Default value

        tk.Label(input_frame, text="Group 2 (Medium Contact) %:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.group2_entry = tk.Entry(input_frame)
        self.group2_entry.grid(row=7, column=1, padx=10, pady=5)
        self.group2_entry.insert(0, "50")  # Default value

        tk.Label(input_frame, text="Group 3 (High Contact) %:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.group3_entry = tk.Entry(input_frame)
        self.group3_entry.grid(row=8, column=1, padx=10, pady=5)
        self.group3_entry.insert(0, "25")  # Default value

        # Predefined Examples Dropdown
        tk.Label(input_frame, text="Select Predefined Example").grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.example_var = tk.StringVar()
        self.example_dropdown = ttk.Combobox(input_frame, textvariable=self.example_var, state="readonly")
        self.example_dropdown['values'] = ["Custom", "Example 1: High Contact", "Example 2: Age-Based"]
        self.example_dropdown.grid(row=9, column=1, padx=10, pady=5)
        self.example_dropdown.current(0)  # Default to "Custom"

        # Bind directly to the on_example_select method to avoid conflicts
        self.example_dropdown.bind("<<ComboboxSelected>>", self.on_example_select)

        # Checkbox for Optimal Vaccine Allocation
        self.optimal_allocation_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Use Optimal Vaccine Allocation", variable=self.optimal_allocation_var).grid(
            row=10, columnspan=2, sticky="w")

        # Checkbox to Display Herd Immunity Threshold
        self.herd_immunity_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Display Herd Immunity Threshold", variable=self.herd_immunity_var).grid(
            row=11, columnspan=2, sticky="w")

        # Error label
        self.error_label = tk.Label(input_frame, text="", fg="red")
        self.error_label.grid(row=12, columnspan=2)

        # Run Simulation Button
        self.run_button = ttk.Button(input_frame, text="Run Simulation")
        self.run_button.grid(row=13, columnspan=2, pady=10)

        # Plot frames for side-by-side display
        self.plot_frame_1 = tk.Frame(self.scrollable_frame)
        self.plot_frame_1.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        self.plot_frame_2 = tk.Frame(self.scrollable_frame)
        self.plot_frame_2.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    def on_example_select(self, event):
        """Handles example selection and sets the example parameters."""
        example = self.example_var.get()
        examples = {
            "Example 1: High Contact": {
                "population": 1000, "R0": 5.5, "gamma": 0.1,
                "vaccine_coverage": 0.7, "vaccine_efficacy": 0.9,
                "group_percentages": [0.3, 0.5, 0.2]
            },
            "Example 2: Age-Based": {
                "population": 1000, "R0": 3.0, "gamma": 0.07,
                "vaccine_coverage": 0.6, "vaccine_efficacy": 0.85,
                "group_percentages": [0.25, 0.4, 0.35]
            }
        }
        if example in examples:
            self.set_example(examples[example])

    def get_parameters(self):
        """Retrieve parameters from GUI fields."""
        try:
            return {
                "population": int(self.population_entry.get()),
                "R0": float(self.R0_entry.get()),
                "gamma": float(self.gamma_entry.get()),
                "vaccine_coverage": float(self.vaccine_coverage_entry.get()) / 100,
                "vaccine_efficacy": float(self.vaccine_efficacy_entry.get()) / 100,
                "waning_rate": float(self.waning_rate_entry.get()),
                "optimal_allocation": self.optimal_allocation_var.get(),
                "group_percentages": [
                    float(self.group1_entry.get()) / 100,
                    float(self.group2_entry.get()) / 100,
                    float(self.group3_entry.get()) / 100,
                ]
            }
        except ValueError:
            self.display_error("Please enter valid numeric values for all fields.")
            return None

    def set_example(self, params=None):
        """Set predefined example values based on selection in dropdown."""
        if params is None:
            example = self.example_var.get()

            # Predefined examples if selected via dropdown (can be expanded as needed)
            examples = {
                "Example 1: High Contact": {
                    "population": 1000, "R0": 5.5, "gamma": 0.1,
                    "vaccine_coverage": 0.7, "vaccine_efficacy": 0.9,
                    "group_percentages": [0.3, 0.5, 0.2]
                },
                "Example 2: Age-Based": {
                    "population": 1000, "R0": 3.0, "gamma": 0.07,
                    "vaccine_coverage": 0.6, "vaccine_efficacy": 0.85,
                    "group_percentages": [0.25, 0.4, 0.35]
                }
            }
            params = examples.get(example)

        if params:
            self.population_entry.delete(0, tk.END)
            self.population_entry.insert(0, str(params["population"]))

            self.R0_entry.delete(0, tk.END)
            self.R0_entry.insert(0, str(params["R0"]))

            self.gamma_entry.delete(0, tk.END)
            self.gamma_entry.insert(0, str(params["gamma"]))

            self.vaccine_coverage_entry.delete(0, tk.END)
            self.vaccine_coverage_entry.insert(0, str(params["vaccine_coverage"] * 100))

            self.vaccine_efficacy_entry.delete(0, tk.END)
            self.vaccine_efficacy_entry.insert(0, str(params["vaccine_efficacy"] * 100))

            self.group1_entry.delete(0, tk.END)
            self.group1_entry.insert(0, str(params["group_percentages"][0] * 100))

            self.group2_entry.delete(0, tk.END)
            self.group2_entry.insert(0, str(params["group_percentages"][1] * 100))

            self.group3_entry.delete(0, tk.END)
            self.group3_entry.insert(0, str(params["group_percentages"][2] * 100))

    def display_error(self, message):
        """Display error messages in the GUI."""
        self.error_label.config(text=message)

    def display_group_results(self, t, group_results, allocations, herd_immunity=None):
        """Plot infection dynamics and vaccine allocation across groups and display cumulative infections."""

        # Clear previous plots
        for widget in self.plot_frame_1.winfo_children():
            widget.destroy()
        for widget in self.plot_frame_2.winfo_children():
            widget.destroy()

        # Calculate the cumulative number of infections
        total_cumulative_infected = 0
        for S, I, R, V in group_results:
            # Compute new infections as the drop in susceptibles at each time step, clipped to avoid negatives
            new_infections = np.clip(-np.diff(S), 0, None)
            # Sum new infections across all time steps, limiting by population size
            total_cumulative_infected += np.sum(new_infections)
        total_cumulative_infected = min(total_cumulative_infected,
                                        self.get_parameters()['population'])  # Cap at total population

        # Display cumulative infection count above the plots
        if hasattr(self, 'cumulative_label'):
            self.cumulative_label.destroy()  # Clear previous label if it exists
        self.cumulative_label = tk.Label(self.scrollable_frame,
                                         text=f"Total Infected Over 160 Days: {total_cumulative_infected:.0f}",
                                         font=("Helvetica", 14, "bold"))
        self.cumulative_label.pack(pady=10)

        # Infection Dynamics Plot
        fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=100)
        S_total = sum([S for S, I, R, V in group_results])
        I_total = sum([I for S, I, R, V in group_results])
        R_total = sum([R for S, I, R, V in group_results])

        ax1.plot(t, S_total, 'b', label='Total Susceptible')
        ax1.plot(t, I_total, 'r', label='Total Infected')
        ax1.plot(t, R_total, 'g', label='Total Recovered')
        ax1.set_xlabel("Time (days)")
        ax1.set_ylabel("Population")
        ax1.set_title("Infection Dynamics Over Time")
        ax1.legend(loc="upper right")
        ax1.grid()

        # Display herd immunity if selected
        if herd_immunity:
            ax1.axhline(herd_immunity * self.get_parameters()['population'], color='purple', linestyle='--',
                        label='Herd Immunity Threshold')
            ax1.legend(loc="upper right")

        # Embed plot into Tkinter
        canvas1 = FigureCanvasTkAgg(fig1, master=self.plot_frame_1)
        canvas1.draw()
        canvas1.get_tk_widget().pack()

        # Vaccine Allocation Plot
        fig2, ax2 = plt.subplots(figsize=(6, 4), dpi=100)
        groups = [f"Group {i + 1}" for i in range(len(allocations))]
        ax2.bar(groups, allocations, color=['b', 'r', 'g'])
        ax2.set_xlabel("Groups")
        ax2.set_ylabel("Vaccine Allocation")
        ax2.set_title("Optimal Vaccine Allocation Across Groups")

        # Embed second plot into Tkinter
        canvas2 = FigureCanvasTkAgg(fig2, master=self.plot_frame_2)
        canvas2.draw()
        canvas2.get_tk_widget().pack()
