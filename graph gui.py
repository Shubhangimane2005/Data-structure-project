import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph GUI")
        self.root.geometry("1200x600")  # Set a larger window size
        
        self.graph = nx.Graph()
        self.removed_vertices = []
        self.removed_edges = []

        # Set up GUI components with a left-side layout
        self.control_frame = tk.Frame(self.root, bg='lightgray')
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.canvas_frame = tk.Frame(self.root, bg='white')
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add name and roll number labels
        self.name_label = tk.Label(self.control_frame, text="Shubhangi Mane", font=("Arial", 18, "bold"), bg='lightgray')
        self.name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.rollno_label = tk.Label(self.control_frame, text="Roll No: S092", font=("Arial", 14,"bold"), bg='lightgray')
        self.rollno_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Add vertex and edge labels and input fields
        self.label1 = tk.Label(self.control_frame, text="Vertex 1:", font=("Arial", 14), bg='lightgray')
        self.label1.grid(row=2, column=0, padx=10, pady=10)
        self.vertex1 = tk.Entry(self.control_frame, font=("Arial", 14), width=20)
        self.vertex1.grid(row=2, column=1, padx=10, pady=10)

        self.label2 = tk.Label(self.control_frame, text="Vertex 2:", font=("Arial", 14), bg='lightgray')
        self.label2.grid(row=3, column=0, padx=10, pady=10)
        self.vertex2 = tk.Entry(self.control_frame, font=("Arial", 14), width=20)
        self.vertex2.grid(row=3, column=1, padx=10, pady=10)

        self.add_vertex_btn = tk.Button(self.control_frame, text="Add Vertex", font=("Arial", 14), command=self.add_vertex, width=20)
        self.add_vertex_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.add_edge_btn = tk.Button(self.control_frame, text="Add Edge", font=("Arial", 14), command=self.add_edge, width=20)
        self.add_edge_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.remove_vertex_btn = tk.Button(self.control_frame, text="Remove Vertex", font=("Arial", 14), command=self.remove_vertex, width=20)
        self.remove_vertex_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.remove_edge_btn = tk.Button(self.control_frame, text="Remove Edge", font=("Arial", 14), command=self.remove_edge, width=20)
        self.remove_edge_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.display_btn = tk.Button(self.control_frame, text="Display Graph", font=("Arial", 14), command=self.display_graph, width=20)
        self.display_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Labels for displaying graph summary
        self.graph_summary_title = tk.Label(self.control_frame, text="Graph Summary", font=("Arial", 16, "bold"), bg='lightgray')
        self.graph_summary_title.grid(row=9, column=0, columnspan=2, padx=10, pady=(20, 10))

        self.graph_summary_text = tk.Label(self.control_frame, text="", font=("Arial", 12), bg='lightgray', justify=tk.LEFT, anchor="w", wraplength=300)
        self.graph_summary_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def add_vertex(self):
        v1 = self.vertex1.get().strip()
        if v1:
            if v1 not in self.graph:
                self.graph.add_node(v1)
                messagebox.showinfo("Success", f"Vertex '{v1}' added.")
            else:
                messagebox.showerror("Error", f"Vertex '{v1}' already exists.")
            self.display_graph()  # Automatically display the graph after action
        else:
            messagebox.showerror("Error", "Vertex name must be entered.")
        self.vertex1.delete(0, tk.END)

    def add_edge(self):
        v1 = self.vertex1.get().strip()
        v2 = self.vertex2.get().strip()
        if v1 and v2:
            if v1 not in self.graph:
                self.graph.add_node(v1)
            if v2 not in self.graph:
                self.graph.add_node(v2)
            self.graph.add_edge(v1, v2)
            messagebox.showinfo("Success", f"Edge between '{v1}' and '{v2}' added.")
            self.display_graph()  # Automatically display the graph after action
        else:
            messagebox.showerror("Error", "Both vertices must be entered.")
        self.vertex1.delete(0, tk.END)
        self.vertex2.delete(0, tk.END)

    def remove_vertex(self):
        v1 = self.vertex1.get().strip()
        if v1:
            if v1 in self.graph:
                self.graph.remove_node(v1)
                self.removed_vertices.append(v1)
                messagebox.showinfo("Success", f"Vertex '{v1}' removed.")
                self.display_graph()  # Automatically display the graph after action
            else:
                messagebox.showerror("Error", f"Vertex '{v1}' does not exist.")
        else:
            messagebox.showerror("Error", "Vertex name must be entered.")
        self.vertex1.delete(0, tk.END)

    def remove_edge(self):
        v1 = self.vertex1.get().strip()
        v2 = self.vertex2.get().strip()
        if v1 and v2:
            if self.graph.has_edge(v1, v2):
                self.graph.remove_edge(v1, v2)
                self.removed_edges.append((v1, v2))
                messagebox.showinfo("Success", f"Edge between '{v1}' and '{v2}' removed.")
                self.display_graph()  # Automatically display the graph after action
            else:
                messagebox.showerror("Error", "Edge does not exist.")
        else:
            messagebox.showerror("Error", "Both vertices must be entered.")
        self.vertex1.delete(0, tk.END)
        self.vertex2.delete(0, tk.END)

    def display_graph(self):
        self.clear_canvas()
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')  # White background for clarity
        # Adjust k and scale parameters to change the distance between vertices
        pos = nx.spring_layout(self.graph, k=0.3, iterations=20, scale=2)
        nx.draw(self.graph, pos, with_labels=True, ax=ax, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12, font_weight='bold')
        ax.set_aspect('equal')  # Keep the aspect ratio equal
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Update the summary label
        num_vertices = len(self.graph.nodes)
        num_edges = len(self.graph.edges)
        vertices = list(self.graph.nodes)
        edges = list(self.graph.edges)
        removed_vertices = ", ".join(self.removed_vertices)
        removed_edges = ", ".join([f"{v1}-{v2}" for v1, v2 in self.removed_edges])

        summary_message = (f"Number of vertices: {num_vertices}\n"
                           f"Vertices: {', '.join(vertices)}\n"
                           f"Number of edges: {num_edges}\n"
                           f"Edges: {', '.join([f'{v1}-{v2}' for v1, v2 in edges])}\n"
                           f"Removed vertices: {removed_vertices if removed_vertices else 'None'}\n"
                           f"Removed edges: {removed_edges if removed_edges else 'None'}")

        self.graph_summary_text.config(text=summary_message)
        
        # Optionally show the summary in a message box
        # messagebox.showinfo("Graph Summary", summary_message)
    
    def clear_canvas(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
