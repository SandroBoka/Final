import tkinter as tk
from model import SIRModel
from view import SIRView


class SIRController:
    def __init__(self, root):
        self.view = SIRView(root)
        self.view.run_button.config(command=self.run_simulation)

    def run_simulation(self):
        try:
            # Get parameters from the view
            params = self.view.get_parameters()

            # Create the model with the parameters
            model = SIRModel(**params)

            # Calculate herd immunity threshold if selected
            herd_immunity = model.herd_immunity_threshold() if self.view.herd_immunity_var.get() else None

            # Run the simulation
            t, S, I, R = model.simulate()

            # Display results in the view
            self.view.display_results(t, S, I, R, herd_immunity)

        except ValueError:
            self.view.display_error("Please enter valid numeric values for all fields.")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    controller = SIRController(root)
    root.mainloop()
