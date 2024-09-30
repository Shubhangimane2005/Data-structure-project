import tkinter as tk
from tkinter import messagebox, ttk
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np

class TSPPlot:
    def __init__(self, place_names, coords, distance_matrix):
        self.place_names = place_names
        self.coords = coords
        self.distance_matrix = distance_matrix
        self.selected_edges = []
        self.fig, self.ax = plt.subplots()
        self.plot_places()
        plt.show(block=False)  # Show the plot non-blocking

    def plot_places(self):
        self.ax.clear()
        x = self.coords[:, 0]
        y = self.coords[:, 1]
        self.ax.plot(x, y, 'bo')  # plot places

        for i, name in enumerate(self.place_names):
            self.ax.annotate(name, (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        for (start, end) in self.selected_edges:
            arrow_offset = 0.5
            arrow_start = (self.coords[start][0] + arrow_offset, self.coords[start][1] + arrow_offset)
            arrow_end = (self.coords[end][0] - arrow_offset, self.coords[end][1] - arrow_offset)

            self.ax.annotate('', xy=arrow_end,
                             xytext=arrow_start,
                             arrowprops=dict(arrowstyle='->', color='r', lw=1))
            distance = self.distance_matrix[start][end]

            mid_x = (arrow_start[0] + arrow_end[0]) / 2
            mid_y = (arrow_start[1] + arrow_end[1]) / 2
            offset_y = 2 if y[end] > y[start] else -2
            self.ax.text(mid_x, mid_y + offset_y, str(distance), fontsize=10, color='red', ha='center')

        self.ax.set_title('Select places to connect')
        plt.draw()

    def connect_places(self, start, end):
        if (start, end) not in self.selected_edges:
            self.selected_edges.append((start, end))
        self.plot_places()

def calculate_route_distance(route, distance_matrix):
    distance = 0
    for i in range(len(route)):
        distance += distance_matrix[route[i]][route[(i + 1) % len(route)]]
    return distance

def traveling_salesman_problem(distance_matrix):
    num_places = len(distance_matrix)
    places = list(range(num_places))
    min_distance = float('inf')
    best_route = []

    for perm in permutations(places):
        current_distance = calculate_route_distance(perm, distance_matrix)
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = perm
            
    return best_route, min_distance

def on_submit():
    try:
        num_places = int(entry_num_places.get())
        place_names = []

        for i in range(num_places):
            place_name = entry_places[i].get().strip()
            if place_name == "":
                messagebox.showerror("Error", f"Place name for place {i + 1} cannot be empty.")
                return
            place_names.append(place_name)

        distance_input_window(place_names)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers.")

def distance_input_window(place_names):
    global input_window
    input_window = tk.Toplevel(root)
    input_window.title("Enter Distances")

    tk.Label(input_window, text="Enter distances between places:").pack()

    distance_entries = {}
    
    for i in range(len(place_names)):
        for j in range(len(place_names)):
            tk.Label(input_window, text=f"Distance from {place_names[i]} to {place_names[j]}:").pack()
            entry = tk.Entry(input_window, width=10, font=("Arial", 14))  # Increased font size
            entry.pack()
            distance_entries[(i, j)] = entry

    submit_button = tk.Button(input_window, text="Submit Distances", command=lambda: disable_button_and_submit(submit_button, place_names, distance_entries), height=2, width=15, font=("Arial", 14))  # Increased button size
    submit_button.pack()

def disable_button_and_submit(submit_button, place_names, distance_entries):
    submit_button.config(state=tk.DISABLED)  # Disable the button
    submit_distances(place_names, distance_entries)

def submit_distances(place_names, distance_entries):
    try:
        distance_matrix = np.zeros((len(place_names), len(place_names)))
        for (i, j), entry in distance_entries.items():
            distance = entry.get().strip()
            if distance == "":
                messagebox.showerror("Error", "Please enter all distances.")
                return
            distance_matrix[i][j] = int(distance)
        
        best_route, min_distance = traveling_salesman_problem(distance_matrix)
        messagebox.showinfo("Result", f"Best route: {' -> '.join(map(lambda x: place_names[x], best_route))}\nMinimum distance: {min_distance}")

        coords = np.random.rand(len(place_names), 2) * 100
        tsp_plot = TSPPlot(place_names, coords, distance_matrix)

        # Open the connection option immediately after creating TSPPlot
        create_connect_option(place_names, tsp_plot)

        input_window.destroy()  # Destroy the input window after submission

    except ValueError:
        messagebox.showerror("Error", "Please enter valid distances.")

def create_connect_option(place_names, tsp_plot):
    connect_window = tk.Toplevel(root)
    connect_window.title("Connect Places")

    tk.Label(connect_window, text="Select places to connect:").pack()

    place1 = tk.StringVar()
    place2 = tk.StringVar()

    place1_combobox = ttk.Combobox(connect_window, textvariable=place1, values=place_names, font=("Arial", 14))  # Increased font size
    place1_combobox.pack(padx=10, pady=5)

    place2_combobox = ttk.Combobox(connect_window, textvariable=place2, values=place_names, font=("Arial", 14))  # Increased font size
    place2_combobox.pack(padx=10, pady=5)

    connect_button = tk.Button(connect_window, text="Connect", command=lambda: connect_places_if_valid(tsp_plot, place1, place2), height=2, width=15, font=("Arial", 14))  # Increased button size
    connect_button.pack(padx=10, pady=10)

    show_matrix_button = tk.Button(connect_window, text="Show Square Matrix", command=lambda: display_distance_matrix(tsp_plot.distance_matrix, place_names, tsp_plot), height=2, width=15, font=("Arial", 14))  # Increased button size
    show_matrix_button.pack(padx=10, pady=10)

def connect_places_if_valid(tsp_plot, place1_var, place2_var):
    place1_index = place1_var.get()
    place2_index = place2_var.get()

    if place1_index and place2_index and place1_index != place2_index:
        place1_idx = tsp_plot.place_names.index(place1_index)
        place2_idx = tsp_plot.place_names.index(place2_index)
        tsp_plot.connect_places(place1_idx, place2_idx)
    else:
        messagebox.showerror("Error", "Please select two different places to connect.")

def display_distance_matrix(distance_matrix, place_names, tsp_plot):
    matrix_window = tk.Toplevel(root)
    matrix_window.title("Distance Matrix")

    tk.Label(matrix_window, text="Distance Matrix:").grid(row=0, column=0, columnspan=len(place_names))

    for i, place in enumerate(place_names):
        tk.Label(matrix_window, text=place, font=("Arial", 14)).grid(row=1, column=i + 1)  # Increased font size
        tk.Label(matrix_window, text=place, font=("Arial", 14)).grid(row=i + 2, column=0)  # Increased font size

    for i in range(len(place_names)):
        for j in range(len(place_names)):
            tk.Label(matrix_window, text=f"{distance_matrix[i][j]}", font=("Arial", 14)).grid(row=i + 2, column=j + 1)  # Increased font size

    tk.Button(matrix_window, text="Show All Possible Routes", command=lambda: show_all_possible_routes(place_names, distance_matrix), height=2, width=20, font=("Arial", 14)).grid(row=len(place_names) + 2, column=0, columnspan=len(place_names))  # Increased button size

def show_all_possible_routes(place_names, distance_matrix):
    route_input_window = tk.Toplevel(root)
    route_input_window.title("Enter Starting Place")

    tk.Label(route_input_window, text="Enter starting place:", font=("Arial", 14)).pack()  # Increased font size

    starting_place_var = tk.StringVar()
    starting_place_combobox = ttk.Combobox(route_input_window, textvariable=starting_place_var, values=place_names, font=("Arial", 14))  # Increased font size
    starting_place_combobox.pack(padx=10, pady=5)

    def display_routes():
        starting_place = starting_place_var.get()
        if starting_place in place_names:
            start_index = place_names.index(starting_place)
            all_routes = [route for route in permutations(range(len(place_names))) if route[0] == start_index]
            routes_window = tk.Toplevel(root)
            routes_window.title("All Possible Routes")

            tk.Label(routes_window, text="All Possible Routes and Distances:", font=("Arial", 14)).pack()  # Increased font size

            best_route = None
            min_distance = float('inf')

            for route in all_routes:
                distance = calculate_route_distance(route, distance_matrix)
                route_str = " -> ".join(place_names[i] for i in route) + f" -> {place_names[start_index]}: {distance}"
                tk.Label(routes_window, text=route_str, font=("Arial", 12)).pack()  # Increased font size
                
                if distance < min_distance:
                    min_distance = distance
                    best_route = route

            best_route_str = "Best Route: " + " -> ".join(place_names[i] for i in best_route) + f" -> {place_names[start_index]}: {min_distance}"
            tk.Label(routes_window, text=best_route_str, font=('bold', 14)).pack()  # Increased font size
        else:
            messagebox.showerror("Error", "Invalid starting place.")

    tk.Button(route_input_window, text="Show Routes", command=display_routes, height=2, width=15, font=("Arial", 14)).pack()  # Increased button size

# GUI Setup
root = tk.Tk()
root.title("Traveling Salesman Problem")

root.geometry("600x500")  # Increase window size
# Add your name and roll number label
tk.Label(root, text="Shubhangi Mane (Roll No: S092)", font=("Arial", 14)).pack(pady=10)  # Increased font size and added some padding

tk.Label(root, text="Enter number of places:", font=("Arial", 14)).pack()  # Increased font size
entry_num_places = tk.Entry(root, width=10, font=("Arial", 14))  # Increased font size
entry_num_places.pack()

entry_places = []
def create_place_entries():
    try:
        num_places = int(entry_num_places.get())
        for entry in entry_places:
            entry.destroy()
        entry_places.clear()
        
        for i in range(num_places):
            entry = tk.Entry(root, width=14, font=("Arial", 14))  # Increased font size
            entry.pack()
            entry_places.append(entry)
            tk.Label(root, text=f"Place {i + 1}:", font=("Arial", 14)).pack()  # Increased font size
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

tk.Button(root, text="Set Place Names", command=create_place_entries, height=2, width=15, font=("Arial", 14)).pack()  # Increased button size
tk.Button(root, text="Submit", command=on_submit, height=2, width=15, font=("Arial", 14)).pack()  # Increased button size

root.mainloop()
