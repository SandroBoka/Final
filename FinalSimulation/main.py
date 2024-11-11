import tkinter as tk
from classes import InteractionGroup, Person
import random

population = 10000

groupOne_percentage = 0.25
groupTwo_percentage = 0.5
groupThree_percentage = 0.25

groupOne_count = int(population * groupOne_percentage)
groupTwo_count = int(population * groupTwo_percentage)
groupThree_count = int(population * groupThree_percentage)

people = []

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

print(f"Total population: {len(people)}")
print(f"Group 1 count: {groupOne_count}")
print(f"Group 2 count: {groupTwo_count}")
print(f"Group 3 count: {groupThree_count}")

colors = {1: "orange", 2: "green", 3: "blue"}
dot_radius = 3
occupied_positions = []

root = tk.Tk()
root.title("Population Visualization")
root.state('zoomed')
canvas_width = root.winfo_screenwidth()
canvas_height = root.winfo_screenheight()
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()


def is_overlapping(x, y):
    for pos in occupied_positions:
        if ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) < (2 * dot_radius) ** 2:
            return True
    return False


# Helper function to find a non-overlapping random position
def get_non_overlapping_coordinates():
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        x = random.randint(dot_radius, canvas_width - dot_radius)
        y = random.randint(dot_radius, canvas_height - dot_radius)
        if not is_overlapping(x, y):
            occupied_positions.append((x, y))
            return x, y
        attempts += 1
    raise ValueError("Could not find non-overlapping position after many attempts")


# Draw people on the canvas
for person in people:
    group = person.interactionGroup.group
    color = colors.get(group, "black")
    x, y = get_non_overlapping_coordinates()

    canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill=color, outline=color)

root.mainloop()
