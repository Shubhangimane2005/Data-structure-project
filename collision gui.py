
import tkinter as tk
from tkinter import messagebox

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def insert(self, key):
        value = sum(ord(char) for char in key)
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return f"Updated: ({key}, {value}) at index {index}"
        self.table[index].append([key, value])
        return f"Inserted: ({key}, {value}) at index {index}"

    def delete(self, key):
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return f"Deleted key '{key}' from index {index}."
        return f"Key '{key}' not found."

    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return index, item[1]
        return None

    def display(self):
        output = []
        for i, items in enumerate(self.table):
            if items:
                values = ' '.join(str(item) for item in items)
                output.append(f"Index {i}: {values}")
            else:
                output.append(f"Index {i}: None")
        return "\n".join(output)

    def get_size(self):
        return sum(len(items) for items in self.table)

    def display_ascii_values(self, key):
        return ', '.join(f"{char}: {ord(char)}" for char in key)


class HashTableGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hash Table GUI")
        self.hash_table = HashTable()
        self.operation_log = []  # Log to store operation history

        # Add your name and roll number label
        self.name_label = tk.Label(master, text="SHUBHANGI MANE, Roll No: S092", font=("Arial", 12))
        self.name_label.pack(pady=5)

        self.label = tk.Label(master, text="Hash Table Operations", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 12), width=40)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.handle_enter)  # Bind the Enter key

        self.insert_button = tk.Button(master, text="Insert", command=self.insert, font=("Arial", 12), width=15)
        self.insert_button.pack(pady=5)

        self.delete_button = tk.Button(master, text="Delete", command=self.delete, font=("Arial", 12), width=15)
        self.delete_button.pack(pady=5)

        self.display_button = tk.Button(master, text="Display", command=self.display, font=("Arial", 12), width=15)
        self.display_button.pack(pady=5)

        self.size_button = tk.Button(master, text="Size", command=self.display_size, font=("Arial", 12), width=15)
        self.size_button.pack(pady=5)

        self.search_button = tk.Button(master, text="Search", command=self.search, font=("Arial", 12), width=15)
        self.search_button.pack(pady=5)

        self.result_text = tk.Text(master, height=20, width=50, font=("Arial", 12))
        self.result_text.pack(pady=10)

    def clear_text(self):
        self.result_text.delete(1.0, tk.END)

    def handle_enter(self, event):
        """Handle Enter key press to clear the entry field."""
        self.entry.delete(0, tk.END)  # Clear the entry field

    def insert(self):
        key = self.entry.get().strip()
        if key:
            try:
                result = self.hash_table.insert(key)
                ascii_values = self.hash_table.display_ascii_values(key)
                self.operation_log.append(result)  # Log the operation
                self.operation_log.append(f"ASCII Values: {ascii_values}")
                self.display_log()
                self.handle_enter(None)  # Clear the entry field
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def delete(self):
        key = self.entry.get().strip()
        if key:
            try:
                result = self.hash_table.delete(key)
                self.operation_log.append(result)  # Log the operation
                self.display_log()
                self.handle_enter(None)  # Clear the entry field
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def display(self):
        try:
            result = self.hash_table.display()
            self.operation_log.append(result)  # Log the operation
            self.display_log()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_size(self):
        try:
            current_size = self.hash_table.get_size()
            size_message = f"Current size of the hash table: {current_size}"
            self.operation_log.append(size_message)  # Log the operation
            self.display_log()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search(self):
        key = self.entry.get().strip()
        if key:
            try:
                result = self.hash_table.get(key)
                if result is None:
                    message = f"Key '{key}' not found."
                    self.operation_log.append(message)  # Log the operation
                else:
                    index, value = result
                    message = f"Value for '{key}' at index {index}: {value}"
                    self.operation_log.append(message)  # Log the operation
                self.display_log()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def display_log(self):
        """Display the log of operations in the text area."""
        self.clear_text()
        for entry in self.operation_log:
            self.result_text.insert(tk.END, entry + "\n")


if __name__ == "__main__":
    root = tk.Tk()
    gui = HashTableGUI(root)
    root.mainloop()


