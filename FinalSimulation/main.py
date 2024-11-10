# main.py
import tkinter as tk
from classes import InteractionGroup, Person
import random

# Constants
population = 10000

# Group distribution (percentages)
groupOne_percentage = 0.25
groupTwo_percentage = 0.5
groupThree_percentage = 0.25

# Calculate number of people in each group
groupOne_count = int(population * groupOne_percentage)
groupTwo_count = int(population * groupTwo_percentage)
groupThree_count = int(population * groupThree_percentage)

# List to hold all person objects
people = []

# Create people in each group with their specific interaction group
for _ in range(groupOne_count):
    interaction_group = InteractionGroup(1)
    age = random.randint(1, 100)  # Random age between 1 and 100
    people.append(Person(interaction_group, age))

for _ in range(groupTwo_count):
    interaction_group = InteractionGroup(2)
    age = random.randint(1, 100)
    people.append(Person(interaction_group, age))

for _ in range(groupThree_count):
    interaction_group = InteractionGroup(3)
    age = random.randint(1, 100)
    people.append(Person(interaction_group, age))

# Debugging - print population count
print(f"Total population: {len(people)}")
print(f"Group 1 count: {groupOne_count}")
print(f"Group 2 count: {groupTwo_count}")
print(f"Group 3 count: {groupThree_count}")

# Tkinter setup
root = tk.Tk()
root.title("Population Visualization")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Function to display people as dots
colors = {1: "red", 2: "green", 3: "blue"}  # Group colors

x_spacing = 5
y_spacing = 5
x, y = 10, 10

for person in people:
    group = person.interactionGroup.group
    color = colors.get(group, "black")  # Default to black if group color is not found

    # Debugging - print color and coordinates
    print(f"Drawing dot for group {group} at ({x}, {y}) with color {color}")

    canvas.create_oval(x, y, x + 3, y + 3, fill=color, outline=color)
    x += x_spacing
    if x > 780:  # Wrap to next line when reaching canvas width
        x = 10
        y += y_spacing

root.mainloop()
