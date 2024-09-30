import tkinter as tk
import subprocess

class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Page")

        # Create a canvas for scrolling and a scrollbar
        self.canvas = tk.Canvas(self.root, width=900, height=700)  # Increased size for the canvas
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the main content
        self.main_frame = tk.Frame(self.canvas)

        # Create a window in the canvas to hold the main_frame
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Bind the canvas to configure the scroll region
        self.main_frame.bind("<Configure>", self.on_frame_configure)

        # Create two frames: one for buttons (left) and one for data structure info (right)
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", padx=20, pady=20)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Add buttons in the left frame
        self.create_buttons()

        # Add the Data Structures information section to the right frame
        self.create_data_structure_info()

    def on_frame_configure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_buttons(self):
        button_font = ("Helvetica", 14)  # Increased button font size

        # Stack Operations button
        self.stack_button = tk.Button(self.left_frame, text="Stack Operations", font=button_font, width=25, height=2, command=self.open_stack_operations)
        self.stack_button.pack(pady=10)

        # Queue Operations button
        self.queue_button = tk.Button(self.left_frame, text="Queue Operations", font=button_font, width=25, height=2, command=self.open_queue_operations)
        self.queue_button.pack(pady=10)

        # Singly Linked List Operations button
        self.sll_button = tk.Button(self.left_frame, text="Singly Linked List Operations", font=button_font, width=25, height=2, command=self.open_singly_linked_list_operations)
        self.sll_button.pack(pady=10)

        # Doubly Linked List Operations button
        self.dll_button = tk.Button(self.left_frame, text="Doubly Linked List Operations", font=button_font, width=25, height=2, command=self.open_doubly_linked_list_operations)
        self.dll_button.pack(pady=10)

        # Priority Queue without Heap button
        self.priority_queue_button = tk.Button(self.left_frame, text="Priority Queue without Heap", font=button_font, width=25, height=2, command=self.open_priority_queue_operations)
        self.priority_queue_button.pack(pady=10)

        # Priority Queue with Heap button
        self.priority_queue_heap_button = tk.Button(self.left_frame, text="Priority Queue with Heap", font=button_font, width=25, height=2, command=self.open_priority_queue_heap_operations)
        self.priority_queue_heap_button.pack(pady=10)

        # Binary Tree button
        self.binary_tree_button = tk.Button(self.left_frame, text="Binary Tree Operations", font=button_font, width=25, height=2, command=self.open_binary_tree_operations)
        self.binary_tree_button.pack(pady=10)

        # Huffman Encoding button
        self.huffman_button = tk.Button(self.left_frame, text="Huffman Encoding", font=button_font, width=25, height=2, command=self.open_Huffman_operations)
        self.huffman_button.pack(pady=10)

        # Graph Operations button
        self.graph_button = tk.Button(self.left_frame, text="Graph Operations", font=button_font, width=25, height=2, command=self.open_graph_operations)
        self.graph_button.pack(pady=10)

        # Graph with BFS & DFS button
        self.graph_bfs_dfs_button = tk.Button(self.left_frame, text="Graph with BFS & DFS", font=button_font, width=25, height=2, command=self.open_graph_bfs_dfs_operations)
        self.graph_bfs_dfs_button.pack(pady=10)

        # Salesman Operations button
        self.salesman_button = tk.Button(self.left_frame, text="Salesman Operations", font=button_font, width=25, height=2, command=self.open_salesman_operations)
        self.salesman_button.pack(pady=10)

        # Hash (Non-Collision) button
        self.hash_non_collision_button = tk.Button(self.left_frame, text="Hash (Non-Collision) Operations", font=button_font, width=25, height=2, command=self.open_hash_noncollision_operations)
        self.hash_non_collision_button.pack(pady=10)

        # Hash (Collision) button
        self.hash_collision_button = tk.Button(self.left_frame, text="Hash (Collision) Operations", font=button_font, width=25, height=2, command=self.open_hash_collision_operations)
        self.hash_collision_button.pack(pady=10)

    def create_data_structure_info(self):
        # Add a label for the Data Structures Info Section in the right frame
        self.info_label = tk.Label(self.right_frame, text="SHUBHANGI MANE.(S092)", font=("Helvetica", 18, "bold"))
        self.info_label.pack(pady=10)
        self.info_label = tk.Label(self.right_frame, text="Data Structure: A Visual Tour", font=("Helvetica", 18, "bold"))
        self.info_label.pack(pady=10)

        # Add a description for Data Structures in a Text widget
        data_structure_info = """
        **What is a Data Structure?**
        A Data Structure is a specialized format for organizing, processing, retrieving, and storing data. In computer science, it plays a pivotal role in enhancing the performance of algorithms.

        **Why are Data Structures Important?**
        - They optimize search and sort operations.
        - They are fundamental for efficient storage and retrieval of data.
        - They provide an organized way to manage vast datasets effectively.

        **Types of Data Structures:**

        1. **Linear Data Structures:**
        - **Array**: A fixed-size structure used to store data elements of the same type. Quick access, but resizing can be costly.
        - **Linked List**: Each element points to the next one, forming a chain. Allows dynamic memory allocation and efficient insertions/deletions.
        - **Stack**: Follows Last In, First Out (LIFO). Common in recursion, browser history, and undo features.
        - **Queue**: Follows First In, First Out (FIFO). Useful in task scheduling and real-time processing.

        2. **Non-Linear Data Structures:**
        - **Tree**: A hierarchical structure consisting of nodes, starting from a root node. Binary Trees, AVL Trees, and B-Trees are widely used.
        - **Graph**: Represents relationships between data points (vertices). Examples include social networks, road maps, and communication networks.
        - **Hash Table**: Maps keys to values for efficient lookup. Used in dictionaries, database indexing, and caching.

        **Real-World Applications:**
        - **Stack**: Web browsers use stacks to manage back and forward functionality. Editors like Microsoft Word implement undo features using stacks.
        - **Queue**: Operating systems use queues for job scheduling. Printers maintain a queue of print jobs.
        - **Linked List**: Used in dynamic memory allocation and tracking free memory blocks.
        - **Tree**: File systems, databases, and hierarchical data representation.
        - **Graph**: GPS systems, social networks, and routing algorithms in computer networks.
        - **Hash Table**: Frequently used in databases, for instance, to map large datasets efficiently.

        **Conclusion:**
        Data structures form the backbone of computer science algorithms. Understanding their properties, limitations, and uses is key to building efficient software.
        """

        # Increase text font size for readability
        self.info_text = tk.Text(self.right_frame, wrap="word", font=("Helvetica", 14), height=40, width=100)  # Increased font size and dimensions
        self.info_text.pack(pady=10)

        # Tag for underlining
        self.info_text.tag_configure("underline", font=("Helvetica", 14, "underline"))

        # Insert text with underlining
        self.info_text.insert(tk.END, "What is a Data Structure?\n", "underline")
        self.info_text.insert(tk.END, "A Data Structure is a specialized format for organizing, processing, retrieving, and storing data. In computer science, it plays a pivotal role in enhancing the performance of algorithms.\n\n")

        self.info_text.insert(tk.END, "Why are Data Structures Important?\n", "underline")
        self.info_text.insert(tk.END, "- They optimize search and sort operations.\n")
        self.info_text.insert(tk.END, "- They are fundamental for efficient storage and retrieval of data.\n")
        self.info_text.insert(tk.END, "- They provide an organized way to manage vast datasets effectively.\n\n")

        self.info_text.insert(tk.END, "Types of Data Structures:\n", "underline")
        self.info_text.insert(tk.END, "1. Linear Data Structures:\n", "underline")
        self.info_text.insert(tk.END, "- Array: A fixed-size structure used to store data elements of the same type. Quick access, but resizing can be costly.\n")
        self.info_text.insert(tk.END, "- Linked List: Each element points to the next one, forming a chain. Allows dynamic memory allocation and efficient insertions/deletions.\n")
        self.info_text.insert(tk.END, "- Stack: Follows Last In, First Out (LIFO). Common in recursion, browser history, and undo features.\n")
        self.info_text.insert(tk.END, "- Queue: Follows First In, First Out (FIFO). Useful in task scheduling and real-time processing.\n\n")
        self.info_text.insert(tk.END, "2. Non-Linear Data Structures:\n", "underline")
        self.info_text.insert(tk.END, "- Tree: A hierarchical structure consisting of nodes, starting from a root node. Binary Trees, AVL Trees, and B-Trees are widely used.\n")
        self.info_text.insert(tk.END, "- Graph: Represents relationships between data points (vertices). Examples include social networks, road maps, and communication networks.\n")
        self.info_text.insert(tk.END, "- Hash Table: Maps keys to values for efficient lookup. Used in dictionaries, database indexing, and caching.\n\n")

        self.info_text.insert(tk.END, "Real-World Applications:\n", "underline")
        self.info_text.insert(tk.END, "- Stack: Web browsers use stacks to manage back and forward functionality. Editors like Microsoft Word implement undo features using stacks.\n")
        self.info_text.insert(tk.END, "- Queue: Operating systems use queues for job scheduling. Printers maintain a queue of print jobs.\n")
        self.info_text.insert(tk.END, "- Linked List: Used in dynamic memory allocation and tracking free memory blocks.\n")
        self.info_text.insert(tk.END, "- Tree: File systems, databases, and hierarchical data representation.\n")
        self.info_text.insert(tk.END, "- Graph: GPS systems, social networks, and routing algorithms in computer networks.\n")
        self.info_text.insert(tk.END, "- Hash Table: Frequently used in databases, for instance, to map large datasets efficiently.\n\n")

        self.info_text.insert(tk.END, "Conclusion:\n", "underline")
        self.info_text.insert(tk.END, "Data structures form the backbone of computer science algorithms. Understanding their properties, limitations, and uses is key to building efficient software.\n")

        self.info_text.config(state=tk.DISABLED)  # Disable editing of the text widget

    # Placeholder methods for button actions
    def open_stack_operations(self):
        # Open the Stack Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/newww stack gui.py"])

    def open_queue_operations(self):
        # Open the Queue Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/queue gui.py"])

    def open_singly_linked_list_operations(self):
        # Open the Singly Linked List Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/single link ist gui.py"])

    def open_doubly_linked_list_operations(self):
        # Open the Doubly Linked List Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/doubly link list.py"])

    def open_priority_queue_operations(self):
        # Open the Priority Queue without Heap script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/gui without heap.py"])

    def open_priority_queue_heap_operations(self):
        # Open the Priority Queue with Heap script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/priority queue gui.py"])

    def open_binary_tree_operations(self):
        # Open the Binary tree script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/tree.py"])

    def open_Huffman_operations(self):
        # Open the Huffman Encoding script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/huffman gui.py"])

    def open_graph_operations(self):
        # Open the Graph Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/graph gui.py"])

    def open_graph_bfs_dfs_operations(self):
        # Open the Graph with BFS & DFS Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/graph.guiiii.py"])
    def open_salesman_operations(self):
        # Open the Graph with BFS & DFS Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/salesman guiiiii.py"])
    def open_hash_noncollision_operations(self):
        # Open the hash non collisionOperations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/non collision.py"])
    def open_hash_collision_operations(self):
        # Open the hash collison Operations script
        subprocess.Popen(["python", "C:/Users/asd/AppData/Local/Programs/Python/Python311/collision gui.py"])
       

if __name__ == "__main__":
    root = tk.Tk()
    main_page = MainPage(root)
    root.geometry("1000x700")  # Increased window size
    root.mainloop()
