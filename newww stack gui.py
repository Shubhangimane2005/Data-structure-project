import tkinter as tk
from tkinter import messagebox

class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Operations")
        self.stack = []

        # Create a main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame for the content
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Bind the configuration to update the scroll region
        self.content_frame.bind("<Configure>", self.on_frame_configure)

        self.create_widgets()

    def create_widgets(self):
        # Left section for stack operations
        self.left_frame = tk.Frame(self.content_frame)
        self.left_frame.pack(side="left", padx=10, pady=5)

        # Right section for text info
        self.right_frame = tk.Frame(self.content_frame)
        self.right_frame.pack(side="right", padx=10, pady=5)

        # Left side widgets for stack operations
        self.label = tk.Label(self.left_frame, text="S092 : Shubhangi Mane", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=5)

        self.label = tk.Label(self.left_frame, text="Stack Operations", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=5)

        # Increased size of canvas
        self.stack_canvas = tk.Canvas(self.left_frame, width=300, height=400, bg="white")
        self.stack_canvas.pack(pady=10)

        self.push_label = tk.Label(self.left_frame, text="Element to Push:", font=("Helvetica", 16))
        self.push_label.pack(pady=2)

        self.push_entry_var = tk.StringVar()
        # Increased text size in entry field
        self.push_entry = tk.Entry(self.left_frame, textvariable=self.push_entry_var, font=("Helvetica", 16), width=15)
        self.push_entry.pack(pady=2)

        # Updated button sizes and text
        self.push_button = tk.Button(self.left_frame, command=self.push, text="Push", font=("Helvetica", 16), width=15)
        self.push_button.pack(pady=5)

        self.pop_button = tk.Button(self.left_frame, command=self.pop, text="Pop", font=("Helvetica", 16), width=15)
        self.pop_button.pack(pady=5)

        self.peek_button = tk.Button(self.left_frame, command=self.peek, text="Peek", font=("Helvetica", 16), width=15)
        self.peek_button.pack(pady=5)

        self.empty_button = tk.Button(self.left_frame, command=self.is_empty, text="Is Empty?", font=("Helvetica", 16), width=15)
        self.empty_button.pack(pady=5)

        self.size_button = tk.Button(self.left_frame, command=self.size, text="Size", font=("Helvetica", 16), width=15)
        self.size_button.pack(pady=5)

        self.traverse_button = tk.Button(self.left_frame, command=self.traverse, text="Traverse", font=("Helvetica", 16), width=15)
        self.traverse_button.pack(pady=5)

        # New buttons for search operations
        self.search_value_button = tk.Button(self.left_frame, command=self.search_by_value, text="Search by Value", font=("Helvetica", 16), width=18)
        self.search_value_button.pack(pady=5)

        self.search_position_button = tk.Button(self.left_frame, command=self.search_by_position, text="Search by Position", font=("Helvetica", 16), width=18)
        self.search_position_button.pack(pady=5)

        self.quit_button = tk.Button(self.left_frame, command=self.quit, text="Quit", font=("Helvetica", 16), width=15)
        self.quit_button.pack(pady=5)

        self.result_label = tk.Label(self.left_frame, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=5)

        self.draw_stack()

        # Right side widgets for description text - Bigger and More Descriptive
        self.info_label = tk.Label(self.right_frame, text="What is a Stack?", font=("Helvetica", 20, "bold"))
        self.info_label.pack(anchor="w", padx=10, pady=5)

        self.info_text1 = tk.Label(self.right_frame, 
            text="A stack is a linear data structure that follows the LIFO (Last-In-First-Out) principle. \nThe most recent element added is the first one to be removed. "
            "It allows access only to the top element.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.info_text1.pack(anchor="w", padx=10, pady=5)

        # Explaining Push Operation
        self.push_info_label = tk.Label(self.right_frame, text="1. Push Operation", font=("Helvetica", 20, "bold"))
        self.push_info_label.pack(anchor="w", padx=10, pady=5)

        self.push_info_text = tk.Label(self.right_frame, 
            text="The Push operation adds an element to the top of the stack. \nIf the stack is full, it will result in Stack Overflow.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.push_info_text.pack(anchor="w", padx=10, pady=5)

        # Explaining Pop Operation
        self.pop_info_label = tk.Label(self.right_frame, text="2. Pop Operation", font=("Helvetica", 20, "bold"))
        self.pop_info_label.pack(anchor="w", padx=10, pady=5)

        self.pop_info_text = tk.Label(self.right_frame, 
            text="The Pop operation removes the top element from the stack. \nIf the stack is empty, it will result in Stack Underflow.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.pop_info_text.pack(anchor="w", padx=10, pady=5)

        # Explaining Peek Operation
        self.peek_info_label = tk.Label(self.right_frame, text="3. Peek Operation", font=("Helvetica", 20, "bold"))
        self.peek_info_label.pack(anchor="w", padx=10, pady=5)

        self.peek_info_text = tk.Label(self.right_frame, 
            text="The Peek operation allows you to see the top element of the stack without removing it.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.peek_info_text.pack(anchor="w", padx=10, pady=5)

        # Explaining Is Empty Operation
        self.empty_info_label = tk.Label(self.right_frame, text="4. Is Empty Operation", font=("Helvetica", 20, "bold"))
        self.empty_info_label.pack(anchor="w", padx=10, pady=5)

        self.empty_info_text = tk.Label(self.right_frame, 
            text="The Is Empty operation checks whether the stack has any elements. \nIf it's empty, this operation returns True.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.empty_info_text.pack(anchor="w", padx=10, pady=5)

        # Explaining Size Operation
        self.size_info_label = tk.Label(self.right_frame, text="5. Size Operation", font=("Helvetica", 20, "bold"))
        self.size_info_label.pack(anchor="w", padx=10, pady=5)

        self.size_info_text = tk.Label(self.right_frame, 
            text="The Size operation returns the number of elements currently present in the stack.", 
            font=("Helvetica", 16), wraplength=400, justify="left")
        self.size_info_text.pack(anchor="w", padx=10, pady=5)

        # Explaining LIFO Principle
        self.lifo_info_label = tk.Label(self.right_frame, text="LIFO Principle", font=("Helvetica", 20, "bold"))
        self.lifo_info_label.pack(anchor="w", padx=10, pady=5)

        self.lifo_info_text = tk.Label(self.right_frame, 
            text="Stacks operate on the LIFO (Last-In-First-Out) principle. \nThis means the last element added to the stack is the first one to be removed.", 
            font=("Helvetica", 16, "bold"), wraplength=400, justify="left")
        self.lifo_info_text.pack(anchor="w", padx=10, pady=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_stack(self):
        self.stack_canvas.delete("all")
        y = 10  # Start position for drawing stack elements
        for i, element in enumerate(reversed(self.stack)):
            self.stack_canvas.create_rectangle(10, y, 280, y + 30, fill="lightblue")
            self.stack_canvas.create_text(150, y + 15, text=str(element), font=("Helvetica", 14))
            y += 35

    def push(self):
        element = self.push_entry_var.get()
        if element:
            self.stack.append(element)
            self.result_label.config(text=f"Pushed: {element}")
            self.push_entry_var.set("")
            self.draw_stack()
        else:
            messagebox.showerror("Input Error", "Please enter an element to push.")

    def pop(self):
        if self.stack:
            popped_element = self.stack.pop()
            self.result_label.config(text=f"Popped: {popped_element}")
            self.draw_stack()
        else:
            messagebox.showerror("Stack Underflow", "Cannot pop from an empty stack.")

    def peek(self):
        if self.stack:
            top_element = self.stack[-1]
            self.result_label.config(text=f"Top Element: {top_element}")
        else:
            messagebox.showerror("Stack Empty", "Cannot peek into an empty stack.")

    def is_empty(self):
        empty_status = "Stack is empty." if not self.stack else "Stack is not empty."
        self.result_label.config(text=empty_status)

    def size(self):
        self.result_label.config(text=f"Stack Size: {len(self.stack)}")

    def traverse(self):
        if self.stack:
            traversal_order = " -> ".join(self.stack)
            self.result_label.config(text=f"Stack Elements: {traversal_order}")
        else:
            messagebox.showerror("Stack Empty", "Cannot traverse an empty stack.")

    def search_by_value(self):
        value = self.push_entry_var.get()
        if value in self.stack:
            index = self.stack.index(value)
            self.result_label.config(text=f"Element '{value}' found at position: {index}")
        else:
            messagebox.showerror("Search Error", f"Element '{value}' not found in the stack.")

    def search_by_position(self):
        try:
            position = int(self.push_entry_var.get())
            if 0 <= position < len(self.stack):
                self.result_label.config(text=f"Element at position {position}: {self.stack[-(position + 1)]}")
            else:
                messagebox.showerror("Position Error", "Position out of bounds.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer position.")

    def quit(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    stack_app = StackGUI(root)
    root.mainloop()
