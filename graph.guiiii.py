import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import scrolledtext

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph GUI")
        self.root.geometry("1200x600")  # Set a larger window size

        self.graph = nx.Graph()
        self.positions = {}  # Store vertex positions
        self.vertex_spacing = 2  # Space between vertices
        self.removed_vertices = []
        self.removed_edges = []

        # Main frame setup
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollable canvas setup for controls on the left
        self.canvas_in_main_frame = tk.Canvas(self.main_frame)
        self.canvas_in_main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas_in_main_frame.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_in_main_frame.config(yscrollcommand=self.scrollbar.set)

        # Frame within canvas
        self.scrollable_frame = tk.Frame(self.canvas_in_main_frame)
        self.canvas_in_main_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas_in_main_frame.config(scrollregion=self.canvas_in_main_frame.bbox("all")))

        # Add widgets to scrollable_frame
        self.name_label = tk.Label(self.scrollable_frame, text="Shubhangi Mane", font=("Arial", 18, "bold"))
        self.name_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.rollno_label = tk.Label(self.scrollable_frame, text="Roll No: S092", font=("Arial", 14, "bold"))
        self.rollno_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.label1 = tk.Label(self.scrollable_frame, text="Reference Vertex:", font=("Arial", 14))
        self.label1.grid(row=2, column=0, padx=10, pady=10)
        self.vertex1 = tk.Entry(self.scrollable_frame, font=("Arial", 14), width=20)
        self.vertex1.grid(row=2, column=1, padx=10, pady=10)

        self.label2 = tk.Label(self.scrollable_frame, text="New Vertex:", font=("Arial", 14))
        self.label2.grid(row=3, column=0, padx=10, pady=10)
        self.vertex2 = tk.Entry(self.scrollable_frame, font=("Arial", 14), width=20)
        self.vertex2.grid(row=3, column=1, padx=10, pady=10)

        self.position_label = tk.Label(self.scrollable_frame, text="Position:", font=("Arial", 14))
        self.position_label.grid(row=4, column=0, padx=10, pady=10)

        self.position_options = ["Left", "Right", "Center"]
        self.position_var = tk.StringVar(value="Center")
        self.position_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.position_var, values=self.position_options, state="readonly", font=("Arial", 14))
        self.position_menu.grid(row=4, column=1, padx=10, pady=10)

        self.add_vertex_btn = tk.Button(self.scrollable_frame, text="Add Vertex", font=("Arial", 14), command=self.add_vertex_relative, width=20)
        self.add_vertex_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.add_edge_btn = tk.Button(self.scrollable_frame, text="Add Edge", font=("Arial", 14), command=self.add_edge, width=20)
        self.add_edge_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.remove_vertex_btn = tk.Button(self.scrollable_frame, text="Remove Vertex", font=("Arial", 14), command=self.remove_vertex, width=20)
        self.remove_vertex_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.remove_edge_btn = tk.Button(self.scrollable_frame, text="Remove Edge", font=("Arial", 14), command=self.remove_edge, width=20)
        self.remove_edge_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.display_btn = tk.Button(self.scrollable_frame, text="Display Graph", font=("Arial", 14), command=self.display_summary, width=20)
        self.display_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.dfs_btn = tk.Button(self.scrollable_frame, text="DFS Traversal", font=("Arial", 14), command=self.perform_dfs, width=20)
        self.dfs_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        self.bfs_btn = tk.Button(self.scrollable_frame, text="BFS Traversal", font=("Arial", 14), command=self.perform_bfs, width=20)
        self.bfs_btn.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

        self.graph_summary_title = tk.Label(self.scrollable_frame, text="Graph Summary", font=("Arial", 16, "bold"))
        self.graph_summary_title.grid(row=12, column=0, columnspan=2, padx=10, pady=(20, 10))

        self.graph_summary_text = scrolledtext.ScrolledText(self.scrollable_frame, font=("Arial", 12), wrap=tk.WORD, height=15, width=40)
        self.graph_summary_text.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

        # Frame for graph on the right-hand side
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Initialize the figure for graph plotting
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.plot_graph()

    def add_vertex_relative(self):
        new_vertex = self.vertex2.get().strip()
        ref_vertex = self.vertex1.get().strip()
        position = self.position_var.get()  # Get the selected relative position

        if not new_vertex:
            messagebox.showerror("Error", "New vertex name must be entered.")
            return

        if new_vertex in self.graph:
            messagebox.showerror("Error", f"Vertex '{new_vertex}' already exists.")
            return

        if not self.graph.nodes:
            # First vertex, no reference needed
            self.graph.add_node(new_vertex)
            self.positions[new_vertex] = (0, 0)  # Place the first node at the origin
            messagebox.showinfo("Success", f"Vertex '{new_vertex}' added as the first vertex.")
            self.display_summary()
        else:
            # After first vertex, reference vertex is required
            if not ref_vertex:
                messagebox.showerror("Error", "Reference vertex must be specified after the first vertex.")
                return
            if ref_vertex not in self.graph:
                messagebox.showerror("Error", f"Reference vertex '{ref_vertex}' does not exist.")
                return
            self.graph.add_node(new_vertex)
            self.assign_relative_position(ref_vertex, new_vertex, position)
            messagebox.showinfo("Success", f"Vertex '{new_vertex}' added to the {position} of '{ref_vertex}'.")
            self.display_summary()

        self.vertex1.delete(0, tk.END)
        self.vertex2.delete(0, tk.END)

    def assign_relative_position(self, ref_vertex, new_vertex, position):
        """Assign specific positions for the new vertex relative to the reference vertex."""
        ref_pos = self.positions.get(ref_vertex, (0, 0))
        shift = self.vertex_spacing

        if position == "Left":
            new_pos = (ref_pos[0] - shift, ref_pos[1])
        elif position == "Right":
            new_pos = (ref_pos[0] + shift, ref_pos[1])
        else:  # Center (assuming upward direction)
            new_pos = (ref_pos[0], ref_pos[1] + shift)

        # Ensure the position is unique
        while new_pos in self.positions.values():
            new_pos = (new_pos[0] + 0.1, new_pos[1] + 0.1)

        self.positions[new_vertex] = new_pos

    def plot_graph(self):
        self.ax.clear()

        if self.graph.nodes:
            nx.draw(self.graph, pos=self.positions, with_labels=True, ax=self.ax,
                    node_color="skyblue", edge_color="gray", node_size=2000,
                    font_size=10, font_weight="bold")
        else:
            self.ax.text(0.5, 0.5, "Graph is empty", fontsize=15, ha='center')

        self.fig.tight_layout()
        self.canvas.draw()

    def display_summary(self):
        self.plot_graph()
        self.graph_summary_text.delete(1.0, tk.END)
        self.graph_summary_text.insert(tk.END, f"Vertices: {list(self.graph.nodes)}\n")
        self.graph_summary_text.insert(tk.END, f"Edges: {list(self.graph.edges)}\n")
        self.graph_summary_text.insert(tk.END, f"Removed Vertices: {self.removed_vertices}\n")
        self.graph_summary_text.insert(tk.END, f"Removed Edges: {self.removed_edges}\n")

    def add_edge(self):
        v1 = self.vertex1.get().strip()
        v2 = self.vertex2.get().strip()

        if not v1 or not v2:
            messagebox.showerror("Error", "Both vertices must be specified.")
            return

        if v1 not in self.graph or v2 not in self.graph:
            messagebox.showerror("Error", "Both vertices must exist in the graph.")
            return

        if self.graph.has_edge(v1, v2):
            messagebox.showerror("Error", f"Edge between '{v1}' and '{v2}' already exists.")
            return

        self.graph.add_edge(v1, v2)
        self.display_summary()
        messagebox.showinfo("Success", f"Edge added between '{v1}' and '{v2}'.")

        self.vertex1.delete(0, tk.END)
        self.vertex2.delete(0, tk.END)

    def remove_vertex(self):
        vertex = self.vertex2.get().strip()

        if not vertex:
            messagebox.showerror("Error", "Vertex name must be entered.")
            return

        if vertex not in self.graph:
            messagebox.showerror("Error", f"Vertex '{vertex}' does not exist.")
            return

        # Remove the vertex and its associated edges
        self.graph.remove_node(vertex)
        self.removed_vertices.append(vertex)
        self.display_summary()
        messagebox.showinfo("Success", f"Vertex '{vertex}' removed.")

        self.vertex2.delete(0, tk.END)

    def remove_edge(self):
        v1 = self.vertex1.get().strip()
        v2 = self.vertex2.get().strip()

        if not v1 or not v2:
            messagebox.showerror("Error", "Both vertices must be specified.")
            return

        if v1 not in self.graph or v2 not in self.graph:
            messagebox.showerror("Error", "Both vertices must exist in the graph.")
            return

        if not self.graph.has_edge(v1, v2):
            messagebox.showerror("Error", f"Edge between '{v1}' and '{v2}' does not exist.")
            return

        self.graph.remove_edge(v1, v2)
        self.removed_edges.append((v1, v2))
        self.display_summary()
        messagebox.showinfo("Success", f"Edge between '{v1}' and '{v2}' removed.")

        self.vertex1.delete(0, tk.END)
        self.vertex2.delete(0, tk.END)

    def perform_dfs(self):
        start_vertex = self.vertex1.get().strip()

        if not start_vertex:
            messagebox.showerror("Error", "Start vertex must be specified.")
            return

        if start_vertex not in self.graph:
            messagebox.showerror("Error", f"Vertex '{start_vertex}' does not exist.")
            return

        dfs_traversal = list(nx.dfs_edges(self.graph, source=start_vertex))
        traversal_nodes = set()
        for u, v in dfs_traversal:
            traversal_nodes.add(u)
            traversal_nodes.add(v)
        
        # Plot DFS Traversal
        G_dfs = nx.DiGraph()
        G_dfs.add_edges_from(dfs_traversal)
        pos_dfs = nx.spring_layout(G_dfs)
        plt.figure(figsize=(10, 6))
        nx.draw(G_dfs, pos=pos_dfs, with_labels=True, node_color="lightgreen", edge_color="blue", node_size=2000, font_size=10, font_weight="bold")
        plt.title("DFS Traversal")
        plt.show()

    def perform_bfs(self):
        start_vertex = self.vertex1.get().strip()

        if not start_vertex:
            messagebox.showerror("Error", "Start vertex must be specified.")
            return

        if start_vertex not in self.graph:
            messagebox.showerror("Error", f"Vertex '{start_vertex}' does not exist.")
            return

        bfs_traversal = list(nx.bfs_edges(self.graph, source=start_vertex))
        traversal_nodes = set()
        for u, v in bfs_traversal:
            traversal_nodes.add(u)
            traversal_nodes.add(v)

        # Plot BFS Traversal
        G_bfs = nx.DiGraph()
        G_bfs.add_edges_from(bfs_traversal)
        pos_bfs = nx.spring_layout(G_bfs)
        plt.figure(figsize=(10, 6))
        nx.draw(G_bfs, pos=pos_bfs, with_labels=True, node_color="lightcoral", edge_color="green", node_size=2000, font_size=10, font_weight="bold")
        plt.title("BFS Traversal")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
