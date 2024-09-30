import tkinter as tk
from tkinter import messagebox
import heapq

class PriorityQueue:
    def __init__(self):
        self.queue = []  # This list will store the heap.
        self.entry_finder = {}  # Dictionary to keep track of the heap entries.
        self.counter = 0  # Unique sequence count to handle elements with the same priority.

    def enqueue(self, priority, item):
        """Add a new item or update the priority of an existing item."""
        if item in self.entry_finder:
            self.remove_item(item)
        count = self.counter
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.queue, entry)
        self.counter += 1

    def dequeue(self):
        """Remove and return the lowest priority item."""
        while self.queue:
            priority, count, item = heapq.heappop(self.queue)
            if item is not None:
                del self.entry_finder[item]
                return item
        raise KeyError('pop from an empty priority queue')

    def peek(self):
        """Return the lowest priority item without removing it."""
        while self.queue:
            priority, count, item = self.queue[0]
            if item is not None:
                return item
            heapq.heappop(self.queue)  # Remove invalid entry.
        raise KeyError('peek from an empty priority queue')

    def remove_item(self, item):
        """Mark an existing item as REMOVED."""
        entry = self.entry_finder.pop(item)
        entry[-1] = None

    def search_by_value(self, value):
        """Return the position of an item by its value."""
        for i, entry in enumerate(self.queue):
            if entry[2] == value:
                return i
        return -1

    def search_by_position(self, position):
        """Return the value of an item by its position."""
        if 0 <= position < len(self.queue):
            return self.queue[position][2]
        return None

    def size(self):
        """Return the size of the queue."""
        return len(self.entry_finder)

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.entry_finder) == 0

    def traverse(self):
        """Traverse the queue."""
        return [entry[2] for entry in self.queue if entry[2] is not None]

class PriorityQueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NAME = SHUBHANGI MANE                           ROLL NO = S092")
        self.root.geometry("1000x800")
        self.root.config(bg="lightblue")

        self.pq = PriorityQueue()

        title = tk.Label(self.root, text="Priority Queue Operations ( With Heap)", font=("Arial", 24, "bold"), bg="lightblue")
        title.pack(pady=10)

        self.frame = tk.Frame(self.root, bg="lightblue")
        self.frame.pack(pady=20)

        self.priority_label = tk.Label(self.frame, text="Priority:", font=("Arial", 14, "bold"), bg="lightblue")
        self.priority_label.grid(row=0, column=0, padx=10, pady=10)
        self.priority_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.priority_entry.grid(row=0, column=1, padx=10, pady=10)

        self.item_label = tk.Label(self.frame, text="Item:", font=("Arial", 14, "bold"), bg="lightblue")
        self.item_label.grid(row=1, column=0, padx=10, pady=10)
        self.item_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.item_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.frame, text="Enqueue", font=("Arial", 14, "bold"), bg="green", fg="white", command=self.enqueue)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        self.remove_button = tk.Button(self.frame, text="Dequeue", font=("Arial", 14, "bold"), bg="red", fg="white", command=self.dequeue)
        self.remove_button.grid(row=2, column=1, padx=10, pady=10)

        self.peek_button = tk.Button(self.frame, text="Peek", font=("Arial", 14, "bold"), bg="yellow", fg="black", command=self.peek)
        self.peek_button.grid(row=3, column=0, padx=10, pady=10)

        self.size_button = tk.Button(self.frame, text="Size", font=("Arial", 14, "bold"), bg="blue", fg="white", command=self.size)
        self.size_button.grid(row=3, column=1, padx=10, pady=10)

        self.traverse_button = tk.Button(self.frame, text="Traverse", font=("Arial", 14, "bold"), bg="purple", fg="white", command=self.traverse)
        self.traverse_button.grid(row=4, column=0, padx=10, pady=10)

        self.search_value_label = tk.Label(self.frame, text="Search by Value:", font=("Arial", 14, "bold"), bg="lightblue")
        self.search_value_label.grid(row=5, column=0, padx=10, pady=10)
        self.search_value_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.search_value_entry.grid(row=5, column=1, padx=10, pady=10)

        self.search_value_button = tk.Button(self.frame, text="Search", font=("Arial", 14, "bold"), bg="orange", fg="white", command=self.search_by_value)
        self.search_value_button.grid(row=6, column=0, padx=10, pady=10)

        self.search_pos_label = tk.Label(self.frame, text="Search by Position:", font=("Arial", 14, "bold"), bg="lightblue")
        self.search_pos_label.grid(row=7, column=0, padx=10, pady=10)
        self.search_pos_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.search_pos_entry.grid(row=7, column=1, padx=10, pady=10)

        self.search_pos_button = tk.Button(self.frame, text="Search", font=("Arial", 14, "bold"), bg="orange", fg="white", command=self.search_by_position)
        self.search_pos_button.grid(row=8, column=0, padx=10, pady=10)

        self.is_empty_button = tk.Button(self.frame, text="Check if Empty", font=("Arial", 14, "bold"), bg="brown", fg="white", command=self.check_if_empty)
        self.is_empty_button.grid(row=8, column=1, padx=10, pady=10)

        # Canvas to display the priority queue
        self.canvas = tk.Canvas(self.root, width=1200, height=400, bg="white")
        self.canvas.pack(pady=20)

    def enqueue(self):
        try:
            priority = int(self.priority_entry.get())
            item = self.item_entry.get()
            if item == "":
                messagebox.showerror("Error", "Item cannot be empty")
                return
            self.pq.enqueue(priority, item)
            messagebox.showinfo("Success", f"Enqueued '{item}' with priority {priority}")
            self.priority_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.update_canvas()
        except ValueError:
            messagebox.showerror("Error", "Priority must be an integer")

    def dequeue(self):
        try:
            item = self.pq.dequeue()
            messagebox.showinfo("Success", f"Dequeued item: {item}")
            self.update_canvas()
        except KeyError:
            messagebox.showerror("Error", "Priority queue is empty")

    def peek(self):
        try:
            item = self.pq.peek()
            messagebox.showinfo("Peek", f"Peek item: {item}")
        except KeyError:
            messagebox.showerror("Error", "Priority queue is empty")

    def size(self):
        size = self.pq.size()
        messagebox.showinfo("Size", f"Size of queue: {size}")

    def traverse(self):
        items = self.pq.traverse()
        messagebox.showinfo("Traverse", f"Queue traversal: {items}")

    def search_by_value(self):
        value = self.search_value_entry.get()
        position = self.pq.search_by_value(value)
        if position != -1:
            messagebox.showinfo("Search Result", f"Item '{value}' found at position: {position}")
        else:
            messagebox.showinfo("Search Result", f"Item '{value}' not found")

    def search_by_position(self):
        try:
            position = int(self.search_pos_entry.get())
            value = self.pq.search_by_position(position)
            if value is not None:
                messagebox.showinfo("Search Result", f"Item at position {position}: {value}")
            else:
                messagebox.showinfo("Search Result", f"No item found at position {position}")
        except ValueError:
            messagebox.showerror("Error", "Position must be an integer")

    def check_if_empty(self):
        is_empty = self.pq.is_empty()
        messagebox.showinfo("Check if Empty", f"Is queue empty? {is_empty}")

    def update_canvas(self):
        self.canvas.delete("all")
        items = self.pq.traverse()
        for i, item in enumerate(items):
            # Increased width of rectangles and spacing
            self.canvas.create_rectangle(50 + i * 200, 50, 300 + i * 200, 150, fill="lightgreen")
            self.canvas.create_text(175 + i * 200, 100, text=f"{item} (Priority {self.pq.queue[i][0]})", font=("Arial", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PriorityQueueGUI(root)
    root.mainloop()
