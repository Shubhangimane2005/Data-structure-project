


import tkinter as tk
from tkinter import messagebox

class HashTable:
    def __init__(self, size=10):
        """Initialize the hash table with a specified size."""
        self.size = size
        self.table = [None] * self.size

    def _hash(self, key):
        """Calculate the index for a given key based on ASCII values."""
        ascii_sum = sum(ord(char) for char in key)
        return ascii_sum % self.size

    def insert(self, key):
        """Insert a key into the hash table with its value as the ASCII sum."""
        value = sum(ord(char) for char in key)  # Generate value as ASCII sum
        index = self._hash(key)
        if self.table[index] is not None:
            return f"Collision: key '{key}' hashes to index {index}, which is already occupied."
        self.table[index] = (key, value)
        return f"Inserted: ({key}, {value}) at index {index}"

    def delete(self, key):
        """Delete a key-value pair from the hash table."""
        index = self._hash(key)
        if self.table[index] is not None:
            self.table[index] = None
            return f"Deleted key '{key}' from index {index}."
        return f"Key '{key}' not found."

    def get(self, key):
        """Retrieve the value associated with a given key."""
        index = self._hash(key)
        if self.table[index] is None:
            return None  # Key not found
        return index, self.table[index][1]  # Return index and value

    def display(self):
        """Display the contents of the hash table."""
        output = []
        for i, item in enumerate(self.table):
            if item is not None:
                output.append(f"Index {i}: {item}")
            else:
                output.append(f"Index {i}: None")
        return "\n".join(output)

    def size(self):
        """Return the current number of elements in the hash table."""
        return sum(1 for item in self.table if item is not None)

    def display_ascii_values(self, key):
        """Display ASCII values of each character in the given key."""
        return ', '.join(f"{char}: {ord(char)}" for char in key)

class HashTableGUI:
    def __init__(self, master):
        self.master = master
        master.title("Hash Table GUI")
        self.hash_table = HashTable()

        self.label = tk.Label(master, text="SHUBHANGI MANE: S092", font=("Arial", 14))
        self.label.pack(pady=10)
        self.label = tk.Label(master, text="Hash Table Operations", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 12), width=40)
        self.entry.pack(pady=5)

        self.insert_button = tk.Button(master, text="Insert", command=self.insert, font=("Arial", 12), width=15)
        self.insert_button.pack(pady=5)

        self.delete_button = tk.Button(master, text="Delete", command=self.delete, font=("Arial", 12), width=15)
        self.delete_button.pack(pady=5)

        self.display_button = tk.Button(master, text="Display All Records", command=self.display, font=("Arial", 12), width=15)
        self.display_button.pack(pady=5)

        self.size_button = tk.Button(master, text="Size", command=self.display_size, font=("Arial", 12), width=15)
        self.size_button.pack(pady=5)

        self.search_button = tk.Button(master, text="Search", command=self.search, font=("Arial", 12), width=15)
        self.search_button.pack(pady=5)

        self.result_text = tk.Text(master, height=20, width=50, font=("Arial", 12))
        self.result_text.pack(pady=10)

    def clear_text(self):
        self.result_text.delete(1.0, tk.END)

    def insert(self):
        key = self.entry.get().strip()
        if key:
            result = self.hash_table.insert(key)
            if "Inserted" in result:
                # Show the inserted value immediately
                index = self.hash_table._hash(key)
                value = sum(ord(char) for char in key)
                self.display_log(f"{result}\nInserted value: {value}")
            else:
                self.display_log(result)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def delete(self):
        key = self.entry.get().strip()
        if key:
            result = self.hash_table.delete(key)
            self.display_log(result)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def display(self):
        result = self.hash_table.display()
        self.display_log(result)

    def display_size(self):
        current_size = self.hash_table.size()
        self.display_log(f"Current size of the hash table: {current_size}")

    def search(self):
        key = self.entry.get().strip()
        if key:
            result = self.hash_table.get(key)
            if result is None:
                message = f"Key '{key}' not found."
                self.display_log(message)
            else:
                index, value = result
                message = f"Value for '{key}' at index {index}: {value}"
                self.display_log(message)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a key.")

    def display_log(self, message):
        """Display the message in the text area."""
        self.clear_text()
        self.result_text.insert(tk.END, message + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    gui = HashTableGUI(root)
    root.mainloop()
