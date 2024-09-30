import tkinter as tk
from tkinter import messagebox, font
import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value, reference=None, side=None):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            if reference is not None:
                ref_node = self.find(self.root, reference)
                if ref_node:
                    if side == 'left':
                        if ref_node.left is None:
                            ref_node.left = TreeNode(value)
                        else:
                            messagebox.showinfo("Info", f"Node {reference} already has a left child.")
                    elif side == 'right':
                        if ref_node.right is None:
                            ref_node.right = TreeNode(value)
                        else:
                            messagebox.showinfo("Info", f"Node {reference} already has a right child.")
                else:
                    messagebox.showinfo("Info", f"Reference node {reference} not found.")
            else:
                messagebox.showinfo("Info", "Reference node must be provided for insertion.")

    def insert_root(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            messagebox.showinfo("Info", f"Inserted root node {value}.")
        else:
            messagebox.showinfo("Info", "Root node already exists.")

    def find(self, node, value):
        if node is None:
            return None
        if node.value == value:
            return node
        left_result = self.find(node.left, value)
        if left_result:
            return left_result
        return self.find(node.right, value)

    def _get_depth(self, node):
        if node is None:
            return 0
        return max(self._get_depth(node.left), self._get_depth(node.right)) + 1

    def _layout_tree(self, graph):
        levels = {}
        for node in graph.nodes():
            depth = self._get_depth(self.find(self.root, node))
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
        pos = nx.multipartite_layout(graph, subset_key=levels)
        return pos

    def display_tree(self):
        g = nx.DiGraph()
        self._populate_graph(g, self.root)

        if g.number_of_nodes() == 0:
            messagebox.showinfo("Info", "The tree is empty.")
            return

        pos = self._layout_tree(g)
        plt.figure(figsize=(10, 8))  # Set figure size for better visibility
        nx.draw(g, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=12)
        plt.title("Binary Tree")
        plt.show()

    def _populate_graph(self, graph, node):
        if node is not None:
            graph.add_node(node.value)
            if node.left:
                graph.add_edge(node.value, node.left.value)
                self._populate_graph(graph, node.left)
            if node.right:
                graph.add_edge(node.value, node.right.value)
                self._populate_graph(graph, node.right)

    def inorder_traversal(self, node):
        return self.inorder_traversal(node.left) + [node.value] + self.inorder_traversal(node.right) if node else []

    def preorder_traversal(self, node):
        return [node.value] + self.preorder_traversal(node.left) + self.preorder_traversal(node.right) if node else []

    def postorder_traversal(self, node):
        return self.postorder_traversal(node.left) + self.postorder_traversal(node.right) + [node.value] if node else []

    def delete(self, value):
        self.root = self._delete_node(self.root, value)

    def _delete_node(self, node, value):
        if node is None:
            messagebox.showinfo("Info", f"Node {value} not found.")
            return None

        if value < node.value:
            node.left = self._delete_node(node.left, value)
        elif value > node.value:
            node.right = self._delete_node(node.right, value)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the inorder successor (smallest in the right subtree)
            min_larger_node = self._min_value_node(node.right)
            node.value = min_larger_node.value
            node.right = self._delete_node(node.right, min_larger_node.value)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

class TreeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Binary Tree Application")
        self.tree = BinaryTree()

        # Custom font for larger text
        self.large_font = font.Font(size=14)

        # Binary Tree Operations label
        tk.Label(master, text="Binary Tree Operations", font=self.large_font).grid(row=0, column=0, columnspan=2)

        # Reference node entry
        tk.Label(master, text="Reference Node (for insertion):", font=self.large_font).grid(row=1, column=0)
        self.ref_node_entry = tk.Entry(master, font=self.large_font)
        self.ref_node_entry.grid(row=1, column=1)

        # Value entry
        tk.Label(master, text="Value to Insert/Delete:", font=self.large_font).grid(row=2, column=0)
        self.value_entry = tk.Entry(master, font=self.large_font)
        self.value_entry.grid(row=2, column=1)

        # Insert Root button
        self.insert_root_button = tk.Button(master, text="Insert Root Node", command=self.insert_root_node, width=20, height=2, font=self.large_font)
        self.insert_root_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Insert buttons
        self.insert_left_button = tk.Button(master, text="Insert Left", command=self.insert_node_left, width=20, height=2, font=self.large_font)
        self.insert_left_button.grid(row=4, column=0, pady=5)

        self.insert_right_button = tk.Button(master, text="Insert Right", command=self.insert_node_right, width=20, height=2, font=self.large_font)
        self.insert_right_button.grid(row=4, column=1, pady=5)

        # Delete Node button
        self.delete_node_button = tk.Button(master, text="Delete Node", command=self.delete_node, width=20, height=2, font=self.large_font)
        self.delete_node_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Show Tree button
        self.show_tree_button = tk.Button(master, text="Show Tree", command=self.show_tree, width=20, height=2, font=self.large_font)
        self.show_tree_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Show Traversal buttons
        self.inorder_button = tk.Button(master, text="Show In-Order Traversal", command=self.show_inorder, width=20, height=2, font=self.large_font)
        self.inorder_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.preorder_button = tk.Button(master, text="Show Pre-Order Traversal", command=self.show_preorder, width=20, height=2, font=self.large_font)
        self.preorder_button.grid(row=8, column=0, columnspan=2, pady=5)

        self.postorder_button = tk.Button(master, text="Show Post-Order Traversal", command=self.show_postorder, width=20, height=2, font=self.large_font)
        self.postorder_button.grid(row=9, column=0, columnspan=2, pady=5)

        # Label for displaying results
        self.result_label = tk.Label(master, text="", font=self.large_font, wraplength=400, justify='center')
        self.result_label.grid(row=10, column=0, columnspan=2, pady=10)

    def insert_root_node(self):
        new_value = self.value_entry.get()
        if not new_value:
            messagebox.showinfo("Info", "Please enter a value to insert as root.")
            return
        self.tree.insert_root(new_value)

    def insert_node_left(self):
        ref_value = self.ref_node_entry.get()
        new_value = self.value_entry.get()
        if not new_value:
            messagebox.showinfo("Info", "Please enter a value to insert.")
            return
        if ref_value:
            self.tree.insert(new_value, ref_value, side='left')
            messagebox.showinfo("Info", f"Inserted node {new_value} to the left of {ref_value}.")
        else:
            messagebox.showinfo("Info", "Reference node must be provided for insertion.")

    def insert_node_right(self):
        ref_value = self.ref_node_entry.get()
        new_value = self.value_entry.get()
        if not new_value:
            messagebox.showinfo("Info", "Please enter a value to insert.")
            return
        if ref_value:
            self.tree.insert(new_value, ref_value, side='right')
            messagebox.showinfo("Info", f"Inserted node {new_value} to the right of {ref_value}.")
        else:
            messagebox.showinfo("Info", "Reference node must be provided for insertion.")

    def delete_node(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showinfo("Info", "Please enter a value to delete.")
            return
        self.tree.delete(value)
        messagebox.showinfo("Info", f"Deleted node {value}.")

    def show_tree(self):
        self.tree.display_tree()

    def show_inorder(self):
        traversal = self.tree.inorder_traversal(self.tree.root)
        self.result_label.config(text="In-Order Traversal: " + ", ".join(map(str, traversal)))

    def show_preorder(self):
        traversal = self.tree.preorder_traversal(self.tree.root)
        self.result_label.config(text="Pre-Order Traversal: " + ", ".join(map(str, traversal)))

    def show_postorder(self):
        traversal = self.tree.postorder_traversal(self.tree.root)
        self.result_label.config(text="Post-Order Traversal: " + ", ".join(map(str, traversal)))


if __name__ == "__main__":
    root = tk.Tk()
    app = TreeApp(root)
    root.mainloop()
