import tkinter as tk
from tkinter import simpledialog, messagebox

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
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
        new_node.prev = last

    def insert_at_position(self, data, position):
        if position < 0:
            messagebox.showerror("Error", "Position must be non-negative.")
            return

        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
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
            new_node.prev = prev
            if prev:
                prev.next = new_node
            if current:
                current.prev = new_node
        else:
            messagebox.showerror("Error", "Position out of bounds.")

    def delete_at_beginning(self):
        if not self.head:
            messagebox.showerror("Error", "List is empty.")
            return
        self.head = self.head.next
        if self.head:
            self.head.prev = None

    def delete_at_end(self):
        if not self.head:
            messagebox.showerror("Error", "List is empty.")
            return
        if not self.head.next:
            self.head = None
            return

        last = self.head
        while last.next:
            last = last.next
        if last.prev:
            last.prev.next = None

    def delete_node(self, key):
        temp = self.head

        if temp and temp.data == key:
            self.head = temp.next
            if self.head:
                self.head.prev = None
            temp = None
            return

        while temp and temp.data != key:
            temp = temp.next

        if temp is None:
            messagebox.showerror("Error", "Node not found.")
            return

        if temp.next:
            temp.next.prev = temp.prev
        if temp.prev:
            temp.prev.next = temp.next
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
            if self.head:
                self.head.prev = None
            temp = None
            return

        current_position = 0

        while temp and current_position < position:
            temp = temp.next
            current_position += 1

        if temp is None:
            messagebox.showerror("Error", "Position out of bounds.")
            return

        if temp.next:
            temp.next.prev = temp.prev
        if temp.prev:
            temp.prev.next = temp.next
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
            prev_address = id(current.prev) if current.prev else id(self.head)
            next_address = id(current.next) if current.next else None
            elements.append((current.data, id(current), prev_address, next_address))
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
        self.root.title("Doubly Linked List Operations")

        self.dll = DoublyLinkedList()

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
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.head_label = tk.Label(self.root, text="Head: None", font=("Helvetica", 12, "bold"))
        self.head_label.pack()

        button_font = ('Helvetica', 10)

        tk.Button(frame, text="Insert at Beginning", font=button_font, command=self.insert_at_beginning).grid(row=0, column=0, pady=5, padx=5)
        tk.Button(frame, text="Insert at End", font=button_font, command=self.insert_at_end).grid(row=0, column=1, pady=5, padx=5)
        tk.Button(frame, text="Insert at Position", font=button_font, command=self.insert_at_position).grid(row=1, column=0, pady=5, padx=5)
        tk.Button(frame, text="Delete at Beginning", font=button_font, command=self.delete_at_beginning).grid(row=1, column=1, pady=5, padx=5)
        tk.Button(frame, text="Delete at End", font=button_font, command=self.delete_at_end).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(frame, text="Delete Node by Value", font=button_font, command=self.delete_node).grid(row=2, column=1, pady=5, padx=5)
        tk.Button(frame, text="Delete Node by Position", font=button_font, command=self.delete_at_position).grid(row=3, column=0, pady=5, padx=5)
        tk.Button(frame, text="Search", font=button_font, command=self.search).grid(row=3, column=1, pady=5, padx=5)
        tk.Button(frame, text="Traverse", font=button_font, command=self.traverse).grid(row=4, column=0, pady=5, padx=5)
        tk.Button(frame, text="Check if Empty", font=button_font, command=self.is_empty).grid(row=4, column=1, pady=5, padx=5)
        tk.Button(frame, text="Get Size", font=button_font, command=self.get_size).grid(row=5, column=0, pady=5, padx=10)

    def insert_at_beginning(self):
        data = self.get_data("Enter data to insert at beginning")
        if data is not None:
            self.dll.insert_at_beginning(data)
            self.update_canvas()
            self.update_head_label()

    def insert_at_end(self):
        data = self.get_data("Enter data to insert at end")
        if data is not None:
            self.dll.insert_at_end(data)
            self.update_canvas()
            self.update_head_label()

    def insert_at_position(self):
        data = self.get_data("Enter data to insert")
        position = self.get_position()
        if data is not None and position is not None:
            self.dll.insert_at_position(data, position)
            self.update_canvas()
            self.update_head_label()

    def delete_at_beginning(self):
        self.dll.delete_at_beginning()
        self.update_canvas()
        self.update_head_label()

    def delete_at_end(self):
        self.dll.delete_at_end()
        self.update_canvas()
        self.update_head_label()

    def delete_node(self):
        key = self.get_data("Enter value to delete")
        if key is not None:
            self.dll.delete_node(key)
            self.update_canvas()
            self.update_head_label()

    def delete_at_position(self):
        position = self.get_position()
        if position is not None:
            self.dll.delete_at_position(position)
            self.update_canvas()
            self.update_head_label()

    def search(self):
        key = self.get_data("Enter value to search")
        if key is not None:
            found = self.dll.search(key)
            messagebox.showinfo("Search Result", f"Element {'found' if found else 'not found'} in the list.")

    def traverse(self):
        elements = self.dll.traverse()
        traverse_text = ""
        for data, current_address, prev_address, next_address in elements:
            traverse_text += f"Data: {data}\nAddr: {current_address}\nPrev: {prev_address}\nNext: {next_address}\n\n"
        messagebox.showinfo("List Elements", traverse_text)

    def is_empty(self):
        empty = self.dll.is_empty()
        messagebox.showinfo("Is Empty?", f"List is {'empty' if empty else 'not empty'}.")

    def get_size(self):
        size = self.dll.size()
        messagebox.showinfo("Size of List", f"Size: {size}")

    def get_data(self, prompt):
        data = simpledialog.askinteger("Input", prompt)
        return data

    def get_position(self):
        position = simpledialog.askinteger("Input", "Enter position")
        return position

    def update_head_label(self):
        head_address = id(self.dll.head) if self.dll.head else None
        self.head_label.config(text=f"Head: {head_address}")

    def update_canvas(self):
        self.canvas.delete("all")
        current = self.dll.head
        x, y = self.node_start_x, self.node_start_y

        while current:
            # Draw node box
            node_text = f"Data: {current.data}\nAddr: {id(current)}\nPrev: {id(current.prev) if current.prev else id(self.dll.head)}\nNext: {id(current.next) if current.next else None}"
            self.canvas.create_rectangle(x, y, x + self.node_width, y + self.node_height, fill="lightblue")
            self.canvas.create_text(x + self.node_width // 2, y + self.node_height // 2, text=node_text, font=("Helvetica", 10), justify="center")

            if current.prev:
                # Draw backward arrow from previous node to current node
                prev_arrow_start_x = x - self.node_spacing
                prev_arrow_start_y = y + self.node_height // 2
                self.canvas.create_line(prev_arrow_start_x, prev_arrow_start_y, x, y + self.node_height // 2, arrow=tk.LAST)

            if current.next:
                # Draw forward arrow from current node to next node
                next_arrow_start_x = x + self.node_width
                next_arrow_start_y = y + self.node_height // 2
                next_arrow_end_x = next_arrow_start_x + self.node_spacing
                self.canvas.create_line(next_arrow_start_x, next_arrow_start_y, next_arrow_end_x, y + self.node_height // 2, arrow=tk.LAST)

                # Draw backward arrow from next node to current node
                next_prev_arrow_end_x = next_arrow_end_x + self.node_width
                self.canvas.create_line(next_prev_arrow_end_x, y + self.node_height // 2, next_arrow_end_x, y + self.node_height // 2, arrow=tk.LAST)

            # Update coordinates for the next node
            x += self.node_width + 2 * self.node_spacing
            current = current.next

if __name__ == "__main__":
    root = tk.Tk()
    gui = LinkedListGUI(root)
    root.mainloop()
