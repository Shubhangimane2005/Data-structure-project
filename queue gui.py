import tkinter as tk
from tkinter import messagebox

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("dequeue from empty queue")

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("peek from empty queue")

    def search_by_value(self, value):
        for i, item in enumerate(self.items):
            if item == value:
                return i
        return -1

    def search_by_position(self, position):
        if 0 <= position < len(self.items):
            return self.items[position]
        else:
            raise IndexError("position out of range")

    def size(self):
        return len(self.items)

    def traversal(self):
        return self.items.copy()

class QueueGUI:
    def __init__(self, root):
        self.queue = Queue()
        
        self.root = root
        self.root.title("NAME = SHUBHANGI MANE                             ROLL NO = S092")
        self.root.geometry("900x600")
        self.title_label = tk.Label(root, text="S092 : Shubhangi Mane.", font=("Arial", 24, "bold"), bg="lightblue", fg="darkblue")
        self.title_label.pack(pady=20)
        self.title_label = tk.Label(root, text="QUEUE OPERATIONS", font=("Arial", 24, "bold"), bg="lightblue", fg="darkblue")
        self.title_label.pack(pady=20)
        
        self.frame = tk.Frame(root, bg="lightblue")
        self.frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        self.label = tk.Label(self.frame, text="Enter element:", font=("Arial", 16), bg="lightblue")
        self.label.grid(row=0, column=0, pady=10)
        
        self.entry = tk.Entry(self.frame, width=30, font=("Arial", 16))
        self.entry.grid(row=0, column=1, columnspan=2, pady=10)
        
        button_font = ("Arial", 14, "bold")
        
        self.enqueue_button = tk.Button(self.frame, text="Enqueue", font=button_font, bg="green", fg="white", command=self.enqueue)
        self.enqueue_button.grid(row=1, column=0, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.dequeue_button = tk.Button(self.frame, text="Dequeue", font=button_font, bg="red", fg="white", command=self.dequeue)
        self.dequeue_button.grid(row=1, column=1, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.peek_button = tk.Button(self.frame, text="Peek", font=button_font, bg="orange", fg="white", command=self.peek)
        self.peek_button.grid(row=1, column=2, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.search_value_button = tk.Button(self.frame, text="Search by Value", font=button_font, bg="purple", fg="white", command=self.search_by_value)
        self.search_value_button.grid(row=2, column=0, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.search_position_button = tk.Button(self.frame, text="Search by Position", font=button_font, bg="blue", fg="white", command=self.search_by_position)
        self.search_position_button.grid(row=2, column=1, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.size_button = tk.Button(self.frame, text="Size", font=button_font, bg="brown", fg="white", command=self.size)
        self.size_button.grid(row=2, column=2, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.is_empty_button = tk.Button(self.frame, text="Is Empty", font=button_font, bg="pink", fg="white", command=self.is_empty)
        self.is_empty_button.grid(row=3, column=0, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.traversal_button = tk.Button(self.frame, text="Traversal", font=button_font, bg="cyan", fg="white", command=self.traversal)
        self.traversal_button.grid(row=3, column=1, pady=10, padx=5, ipadx=10, ipady=5)
        
        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg="white")
        self.canvas.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.update_queue_canvas()

    def update_queue_canvas(self):
        self.canvas.delete("all")
        items = self.queue.traversal()
        for i, item in enumerate(items):
            x0, y0 = i * 140 + 10, 50
            x1, y1 = x0 + 120, y0 + 100
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen", outline="black")
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=item, font=("Arial", 18, "bold"))

    def enqueue(self):
        item = self.entry.get()
        if item:
            self.queue.enqueue(item)
            self.update_queue_canvas()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an item to enqueue.")

    def dequeue(self):
        try:
            item = self.queue.dequeue()
            self.update_queue_canvas()
            messagebox.showinfo("Dequeue", f"Dequeued: {item}")
        except IndexError as e:
            messagebox.showerror("Queue Error", str(e))

    def peek(self):
        try:
            item = self.queue.peek()
            messagebox.showinfo("Peek", f"Peek: {item}")
        except IndexError as e:
            messagebox.showerror("Queue Error", str(e))

    def search_by_value(self):
        value = self.entry.get()
        if value:
            position = self.queue.search_by_value(value)
            if position != -1:
                messagebox.showinfo("Search by Value", f"Value found at position: {position}")
            else:
                messagebox.showinfo("Search by Value", "Value not found")
        else:
            messagebox.showwarning("Input Error", "Please enter a value to search.")

    def search_by_position(self):
        try:
            position = int(self.entry.get())
            item = self.queue.search_by_position(position)
            messagebox.showinfo("Search by Position", f"Item at position {position}: {item}")
        except (ValueError, IndexError) as e:
            messagebox.showerror("Input Error", str(e))

    def size(self):
        size = self.queue.size()
        messagebox.showinfo("Size", f"Queue size: {size}")

    def is_empty(self):
        empty = self.queue.is_empty()
        messagebox.showinfo("Is Empty", f"Is queue empty: {empty}")

    def traversal(self):
        items = self.queue.traversal()
        messagebox.showinfo("Traversal", f"Queue traversal: {items}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = QueueGUI(root)
    root.mainloop()
