import tkinter as tk
from tkinter import filedialog, messagebox
import heapq
import os
import pickle
from tkinter import ttk

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_huffman_codes(node, code="", mapping=None):
    if mapping is None:
        mapping = {}
    if node is not None:
        if node.char is not None:
            mapping[node.char] = code
        build_huffman_codes(node.left, code + "0", mapping)
        build_huffman_codes(node.right, code + "1", mapping)
    return mapping

def encode_file(file_path, output_path):
    with open(file_path, 'r') as file:
        text = file.read()

    freq_dict = {}
    for char in text:
        freq_dict[char] = freq_dict.get(char, 0) + 1

    root = build_huffman_tree(freq_dict)
    codes = build_huffman_codes(root)

    with open(output_path, 'wb') as output_file:
        # Save the Huffman codes for decoding
        pickle.dump(codes, output_file)

        # Encode the text and write it to the file
        encoded_text = ''.join(codes[char] for char in text)
        output_file.write(bytearray(int(encoded_text[i:i+8], 2) for i in range(0, len(encoded_text), 8)))

    messagebox.showinfo("Success", "File compressed successfully!")

def decode_file(file_path, output_path):
    with open(file_path, 'rb') as input_file:
        # Load the Huffman codes
        codes = pickle.load(input_file)

        # Read the encoded text from the file
        encoded_text = ''.join(format(byte, '08b') for byte in input_file.read())

    # Decode the text using the Huffman codes
    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in codes.values():
            decoded_text += next(char for char, code in codes.items() if code == current_code)
            current_code = ""

    with open(output_path, 'w') as output_file:
        output_file.write(decoded_text)

    messagebox.showinfo("Success", "File decompressed successfully!")

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Coding GUI")

        self.compress_file_path = ""
        self.decompress_file_path = ""

        # Compression Frame
        compression_frame = tk.Frame(self.root)
        compression_frame.pack(pady=10)

        tk.Label(compression_frame, text="Compression").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Button(compression_frame, text="Choose File", command=self.choose_file_compress).grid(row=1, column=0, pady=5)
        tk.Label(compression_frame, text="Selected File:").grid(row=1, column=1, pady=5)
        self.selected_compress_file_label = tk.Label(compression_frame, text="")
        self.selected_compress_file_label.grid(row=1, column=2, pady=5)

        tk.Button(compression_frame, text="Compress", command=self.compress_file).grid(row=2, column=0, columnspan=3, pady=10)

        # Decompression Frame
        decompression_frame = tk.Frame(self.root)
        decompression_frame.pack(pady=10)

        tk.Label(decompression_frame, text="Decompression").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Button(decompression_frame, text="Choose File", command=self.choose_file_decompress).grid(row=1, column=0, pady=5)
        tk.Label(decompression_frame, text="Selected File:").grid(row=1, column=1, pady=5)
        self.selected_decompress_file_label = tk.Label(decompression_frame, text="")
        self.selected_decompress_file_label.grid(row=1, column=2, pady=5)

        tk.Button(decompression_frame, text="Decompress", command=self.decompress_file).grid(row=2, column=0, columnspan=3, pady=10)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def choose_file_compress(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_compress_file_label.config(text=os.path.basename(file_path))
            self.compress_file_path = file_path

    def choose_file_decompress(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_decompress_file_label.config(text=os.path.basename(file_path))
            self.decompress_file_path = file_path

    def compress_file(self):
        if not self.compress_file_path:
            messagebox.showwarning("Warning", "Please choose a file for compression.")
            return

        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".huffman")
            if output_path:
                self.status_var.set("Compressing...")
                self.root.update_idletasks()

                encode_file(self.compress_file_path, output_path)

                self.status_var.set("File compressed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.root.update_idletasks()
            self.status_var.set("")

    def decompress_file(self):
        if not self.decompress_file_path:
            messagebox.showwarning("Warning", "Please choose a file for decompression.")
            return

        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if output_path:
                self.status_var.set("Decompressing...")
                self.root.update_idletasks()

                decode_file(self.decompress_file_path, output_path)

                self.status_var.set("File decompressed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.root.update_idletasks()
            self.status_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()