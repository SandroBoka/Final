import tkinter as tk
from model import SIRModel
from view import SIRView


class SIRController:
    def __init__(self, root):
        self.view = SIRView(root)
        self.view.run_button.config(command=self.run_simulation)

        # Bind example selection to apply predefined parameters
        self.view.example_dropdown.bind("<<ComboboxSelected>>", self.apply_example)

    def apply_example(self, event):
        """Applies predefined example parameters based on selection."""
        example_name = self.view.example_var.get()

        # Predefined example values from papers
        examples = {
            "Example 1: High Contact (Paper 1)": {
                "population": 10000,
                "R0": 5.5,
                "gamma": 0.1,
                "vaccine_coverage": 0.7,
                "vaccine_efficacy": 0.9,
                "group_percentages": [0.3, 0.5, 0.2]
            },
            "Example 2: Age-Based (Paper 2)": {
                "population": 10000,
                "R0": 3.0,
                "gamma": 0.07,
                "vaccine_coverage": 0.6,
                "vaccine_efficacy": 0.85,
                "group_percentages": [0.25, 0.4, 0.35]
            }
        }

        # Apply example parameters if one is selected
        if example_name in examples:
            self.view.set_example(examples[example_name])

    def run_simulation(self):
        try:
            # Get parameters from the view
            params = self.view.get_parameters()

            # Remove the 'example' key before passing to SIRModel
            params.pop("example", None)

            # Create the model with the remaining parameters
            model = SIRModel(**params)

            # Calculate herd immunity threshold if selected
            herd_immunity = model.herd_immunity_threshold() if self.view.herd_immunity_var.get() else None

            # Run the simulation and get group results
            t, group_results, allocations = model.simulate()

            # Display results in the view with allocation details
            self.view.display_group_results(t, group_results, allocations, herd_immunity)

        except ValueError:
            self.view.display_error("Please enter valid numeric values for all fields.")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    controller = SIRController(root)
    root.mainloop()
