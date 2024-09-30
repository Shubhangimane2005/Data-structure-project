import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def insert_at_position(self, data, position):
        if position < 0:
            messagebox.showerror("Error", "Position must be non-negative.")
            return

        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        prev = None
        current_position = 0

        while current and current_position < position:
            prev = current
            current = current.next
            current_position += 1

        if current_position == position:
            new_node.next = current
            prev.next = new_node
        else:
            messagebox.showerror("Error", "Position out of bounds.")

    def delete_at_beginning(self):
        if not self.head:
            messagebox.showerror("Error", "List is empty.")
            return
        self.head = self.head.next

    def delete_at_end(self):
        if not self.head:
            messagebox.showerror("Error", "List is empty.")
            return
        if not self.head.next:
            self.head = None
            return

        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        second_last.next = None

    def delete_node(self, key):
        temp = self.head

        if temp and temp.data == key:
            self.head = temp.next
            temp = None
            return

        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next

        if temp is None:
            messagebox.showerror("Error", "Node not found.")
            return

        prev.next = temp.next
        temp = None

    def delete_at_position(self, position):
        if position < 0:
            messagebox.showerror("Error", "Position must be non-negative.")
            return

        if not self.head:
            messagebox.showerror("Error", "List is empty.")
            return

        temp = self.head
        if position == 0:
            self.head = temp.next
            temp = None
            return

        prev = None
        current_position = 0

        while temp and current_position < position:
            prev = temp
            temp = temp.next
            current_position += 1

        if temp is None:
            messagebox.showerror("Error", "Position out of bounds.")
            return

        prev.next = temp.next
        temp = None

    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    def traverse(self):
        elements = []
        current = self.head
        while current:
            next_address = id(current.next) if current.next else None
            elements.append((current.data, id(current), next_address))
            current = current.next
        return elements

    def is_empty(self):
        return self.head is None

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

class LinkedListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Singly Linked List Operations")

        self.sll = SinglyLinkedList()

        self.canvas_width = 800
        self.canvas_height = 400
        self.node_width = 120
        self.node_height = 80
        self.node_spacing = 20  # Spacing between nodes
        self.node_start_x = 50   # Starting x position for the first node
        self.node_start_y = 50   # Starting y position for the nodes

        self.create_widgets()
        self.update_head_label()

    def create_widgets(self):
        # Frame for buttons and labels
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Display Name and Roll No
        tk.Label(frame, text="Name: Shubhangi Mane", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=5)
        tk.Label(frame, text="Roll No: S092", font=("Helvetica", 12, "bold")).grid(row=0, column=1, pady=5, padx=5)

        # Canvas to display the linked list
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Head label
        self.head_label = tk.Label(self.root, text="Head: None", font=("Helvetica", 12, "bold"))
        self.head_label.pack()

        # Buttons with larger size and increased text size
        button_font = ('Helvetica', 11, 'bold')
        button_width = 18
        
        tk.Button(frame, text="Insert at Beginning", font=button_font, width=button_width, command=self.insert_at_beginning).grid(row=1, column=0, pady=5, padx=5)
        tk.Button(frame, text="Insert at End", font=button_font, width=button_width, command=self.insert_at_end).grid(row=1, column=1, pady=5, padx=5)
        tk.Button(frame, text="Insert at Position", font=button_font, width=button_width, command=self.insert_at_position).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(frame, text="Delete at Beginning", font=button_font, width=button_width, command=self.delete_at_beginning).grid(row=2, column=1, pady=5, padx=5)
        tk.Button(frame, text="Delete at End", font=button_font, width=button_width, command=self.delete_at_end).grid(row=3, column=0, pady=5, padx=5)
        tk.Button(frame, text="Delete Node by Value", font=button_font, width=button_width, command=self.delete_node).grid(row=3, column=1, pady=5, padx=5)
        tk.Button(frame, text="Delete Node by Position", font=button_font, width=button_width, command=self.delete_at_position).grid(row=4, column=0, pady=5, padx=5)
        tk.Button(frame, text="Search", font=button_font, width=button_width, command=self.search).grid(row=4, column=1, pady=5, padx=5)
        tk.Button(frame, text="Traverse", font=button_font, width=button_width, command=self.traverse).grid(row=5, column=0, pady=5, padx=5)
        tk.Button(frame, text="Check if Empty", font=button_font, width=button_width, command=self.is_empty).grid(row=5, column=1, pady=5, padx=5)
        tk.Button(frame, text="Get Size", font=button_font, width=button_width, command=self.get_size).grid(row=6, column=0, pady=5, padx=5)

    def insert_at_beginning(self):
        data = self.get_data("Enter data to insert at beginning")
        if data is not None:
            self.sll.insert_at_beginning(data)
            self.update_canvas()
            self.update_head_label()

    def insert_at_end(self):
        data = self.get_data("Enter data to insert at end")
        if data is not None:
            self.sll.insert_at_end(data)
            self.update_canvas()
            self.update_head_label()

    def insert_at_position(self):
        data = self.get_data("Enter data to insert")
        position = self.get_position()
        if data is not None and position is not None:
            self.sll.insert_at_position(data, position)
            self.update_canvas()
            self.update_head_label()

    def delete_at_beginning(self):
        self.sll.delete_at_beginning()
        self.update_canvas()
        self.update_head_label()

    def delete_at_end(self):
        self.sll.delete_at_end()
        self.update_canvas()
        self.update_head_label()

    def delete_node(self):
        key = self.get_data("Enter value to delete")
        if key is not None:
            self.sll.delete_node(key)
            self.update_canvas()
            self.update_head_label()

    def delete_at_position(self):
        position = self.get_position()
        if position is not None:
            self.sll.delete_at_position(position)
            self.update_canvas()
            self.update_head_label()

    def search(self):
        key = self.get_data("Enter value to search")
        if key is not None:
            found = self.sll.search(key)
            messagebox.showinfo("Search Result", f"Element {'found' if found else 'not found'} in the list.")

    def traverse(self):
        elements = self.sll.traverse()
        traverse_text = ""
        for data, current_id, next_id in elements:
            traverse_text += f"Data: {data}, Address: {current_id}, Next: {next_id}\n"
        messagebox.showinfo("Linked List", traverse_text)

    def is_empty(self):
        empty = self.sll.is_empty()
        messagebox.showinfo("List Status", f"List is {'empty' if empty else 'not empty'}.")

    def get_size(self):
        size = self.sll.size()
        messagebox.showinfo("List Size", f"Size of the list: {size}")

    def update_canvas(self):
        self.canvas.delete("all")

        elements = self.sll.traverse()
        x = self.node_start_x

        for data, current_id, next_id in elements:
            # Draw rectangle for the node
            self.canvas.create_rectangle(x, self.node_start_y, x + self.node_width, self.node_start_y + self.node_height, outline="black")
            # Draw data inside the rectangle
            self.canvas.create_text(x + self.node_width // 2, self.node_start_y + self.node_height // 4, text=str(data), font=("Helvetica", 12, "bold"))
            # Draw address
            self.canvas.create_text(x + self.node_width // 2, self.node_start_y + self.node_height // 2, text=f"Address: {current_id}", font=("Helvetica", 8))
            # Draw next node address
            self.canvas.create_text(x + self.node_width // 2, self.node_start_y + (3 * self.node_height // 4), text=f"Next: {next_id}", font=("Helvetica", 8))
            # Draw arrow for the link
            if next_id is not None:
                self.canvas.create_line(x + self.node_width, self.node_start_y + self.node_height // 2, x + self.node_width + self.node_spacing, self.node_start_y + self.node_height // 2, arrow=tk.LAST)
            x += self.node_width + self.node_spacing

    def update_head_label(self):
        head_data = "None" if not self.sll.head else self.sll.head.data
        self.head_label.config(text=f"Head: {head_data}")

    def get_data(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def get_position(self):
        return simpledialog.askinteger("Input", "Enter position")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinkedListGUI(root)
    root.mainloop()
