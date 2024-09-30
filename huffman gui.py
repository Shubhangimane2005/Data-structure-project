import heapq
from collections import Counter
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# Node class to store character, frequency, left child, and right child
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = None if freq is None else freq
        self.left = None
        self.right = None

    # Comparator method for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

# Function to build Huffman tree
def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

# Function to generate Huffman codes
def generate_huffman_codes(node, prefix="", huffman_code={}):
    if node:
        if node.char is not None:
            huffman_code[node.char] = prefix
        else:
            generate_huffman_codes(node.left, prefix + "0", huffman_code)
            generate_huffman_codes(node.right, prefix + "1", huffman_code)
    return huffman_code

# Function to draw Huffman tree on canvas
def draw_huffman_tree(node, canvas, x, y, dx, dy):
    if node:
        if node.char is not None:
            canvas.create_text(x, y, text=f"{node.char}\n{node.freq}", tags='node', anchor=tk.N)
        if node.left:
            canvas.create_line(x, y, x - dx, y + dy, tags='line')
            draw_huffman_tree(node.left, canvas, x - dx, y + dy, dx / 2, dy)
        if node.right:
            canvas.create_line(x, y, x + dx, y + dy, tags='line')
            draw_huffman_tree(node.right, canvas, x + dx, y + dy, dx / 2, dy)

# Function to perform Huffman encoding and store results
def huffman_encoding():
    text = input_entry.get()
    
    if not text:
        messagebox.showwarning("Input Error", "Please enter a string to encode.")
        return
    
    global tree_root, huffman_code
    tree_root = build_huffman_tree(text)
    huffman_code = generate_huffman_codes(tree_root)
    
    codes_text.delete(1.0, tk.END)
    codes_text.insert(tk.END, "Huffman Codes:\n")
    for char, code in huffman_code.items():
        codes_text.insert(tk.END, f"{char}: {code}\n")
    
    global total_bits, avg_bits
    total_bits = sum(len(huffman_code[char]) * freq for char, freq in Counter(text).items())
    avg_bits = total_bits / len(text)
    
    encoded_string = ''.join(huffman_code[char] for char in text)
    encoded_string_var.set(encoded_string)
    encoded_string_frame.pack(pady=10)

def show_total_bits():
    total_bits_var.set(total_bits)
    total_bits_frame.pack(pady=5)

def show_avg_bits():
    avg_bits_var.set(f"{avg_bits:.2f}")
    avg_bits_frame.pack(pady=5)

# Function to show the Huffman tree in a new window with vertical scrollbar
def show_tree_view():
    # Create a new Toplevel window
    tree_window = tk.Toplevel(root)
    tree_window.title("Huffman Tree View")
    tree_window.geometry("800x600")

    # Create a Frame to hold the Canvas and Scrollbar
    tree_frame = tk.Frame(tree_window)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar for the Canvas
    tree_scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas to display the Huffman tree
    tree_canvas = tk.Canvas(tree_frame, bg='white', width=800, height=500, yscrollcommand=tree_scrollbar.set)
    tree_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrollbar for canvas
    tree_scrollbar.config(command=tree_canvas.yview)

    # Set scroll region large enough to accommodate tree structure
    tree_canvas.config(scrollregion=(0, 0, 1600, 2000))

    # Draw the Huffman tree on the canvas
    draw_huffman_tree(tree_root, tree_canvas, 800, 20, 100, 100)

    # Button to close the tree view window
    close_button = tk.Button(tree_window, text="Close", command=tree_window.destroy, font=("Helvetica", 14), width=20, height=2)
    close_button.pack(pady=10)

# Function to clear all fields
def clear_all():
    input_entry.delete(0, tk.END)
    codes_text.delete(1.0, tk.END)
    encoded_string_var.set("")
    total_bits_var.set("")
    avg_bits_var.set("")

# Create the main application window
root = tk.Tk()
root.title("Huffman Encoding")
root.geometry("800x600")

# Create a frame and scrollbar for the main window
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

main_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a canvas for the main window with vertical scrolling
main_canvas = tk.Canvas(main_frame, yscrollcommand=main_scrollbar.set)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

main_scrollbar.config(command=main_canvas.yview)

# Configure scroll region for the main window canvas
main_canvas.config(scrollregion=(0, 0, 800, 1200))

# Create a window inside the canvas for widgets
main_window = tk.Frame(main_canvas)
main_canvas.create_window((0, 0), window=main_window, anchor=tk.NW)

# Name label (Shubhangi Mane) in bold
name_label = tk.Label(main_window, text="Shubhangi Mane", font=("Helvetica", 14, "bold"))
name_label.pack(pady=10)

# Input label and entry
input_label = tk.Label(main_window, text="Enter the string to encode:", font=("Helvetica", 14))
input_label.pack(pady=10)
input_entry = tk.Entry(main_window, width=50, font=("Helvetica", 14))
input_entry.pack(pady=10)

# Button to perform Huffman encoding
encode_button = tk.Button(main_window, text="Encode", command=huffman_encoding, font=("Helvetica", 14), width=15, height=2)
encode_button.pack(pady=10)

# Button to show tree view
tree_view_button = tk.Button(main_window, text="Show Tree View", command=show_tree_view, font=("Helvetica", 14), width=15, height=2)
tree_view_button.pack(pady=10)

# Button to clear all fields
clear_button = tk.Button(main_window, text="Delete All", command=clear_all, font=("Helvetica", 14), width=15, height=2)
clear_button.pack(pady=10)

# Text box with vertical scrollbar to display Huffman codes
codes_text = scrolledtext.ScrolledText(main_window, height=10, width=50, font=("Helvetica", 12), wrap=tk.WORD)
codes_text.pack(pady=10)

# Initialize StringVar variables
encoded_string_var = tk.StringVar()
total_bits_var = tk.StringVar()
avg_bits_var = tk.StringVar()

# Frame to display the encoded string
encoded_string_frame = tk.Frame(main_window)
encoded_string_frame.pack_forget()

encoded_string_label = tk.Label(encoded_string_frame, text="Encoded string:", font=("Helvetica", 14))
encoded_string_label.pack(pady=5)
encoded_string_display = tk.Label(encoded_string_frame, textvariable=encoded_string_var, font=("Helvetica", 14))
encoded_string_display.pack(pady=5)

# Button to show total bits required
total_bits_button = tk.Button(main_window, text="Show Total Bits", command=show_total_bits, font=("Helvetica", 14), width=20, height=2)
total_bits_button.pack(pady=10)

# Frame to display total bits required
total_bits_frame = tk.Frame(main_window)
total_bits_frame.pack_forget()

total_bits_label = tk.Label(total_bits_frame, text="Total bits required:", font=("Helvetica", 14))
total_bits_label.pack(pady=5)
total_bits_display = tk.Label(total_bits_frame, textvariable=total_bits_var, font=("Helvetica", 14))
total_bits_display.pack(pady=5)

# Button to show average bits per character
avg_bits_button = tk.Button(main_window, text="Show Average Bits", command=show_avg_bits, font=("Helvetica", 14), width=20, height=2)
avg_bits_button.pack(pady=10)

# Frame to display average bits per character
avg_bits_frame = tk.Frame(main_window)
avg_bits_frame.pack_forget()

avg_bits_label = tk.Label(avg_bits_frame, text="Average bits per character:", font=("Helvetica", 14))
avg_bits_label.pack(pady=5)
avg_bits_display = tk.Label(avg_bits_frame, textvariable=avg_bits_var, font=("Helvetica", 14))
avg_bits_display.pack(pady=5)

root.mainloop()
