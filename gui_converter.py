import os
import csv
import json
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

OUTPUT_DIR = Path("output")


def is_valid_number(line: str) -> bool:
    line = line.strip()
    cleaned = line.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    return cleaned.startswith('+') and cleaned[1:].isdigit() and 8 <= len(cleaned[1:]) <= 15


def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def convert_to_csv(numbers, base_name):
    csv_path = OUTPUT_DIR / f"{base_name}.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['PhoneNumber'])
        for number in numbers:
            writer.writerow([number])


def convert_to_json(numbers, base_name):
    json_path = OUTPUT_DIR / f"{base_name}.json"
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump({'phone_numbers': numbers}, json_file, indent=2)


def convert_to_clean_txt(numbers, base_name):
    txt_path = OUTPUT_DIR / f"{base_name}_clean.txt"
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for number in numbers:
            txt_file.write(number + '\n')


def process_files(file_paths, formats, output_callback):
    ensure_output_dir()
    total_numbers = 0
    start = time.time()

    for file_path in file_paths:
        path = Path(file_path)
        base_name = path.stem
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        numbers = [line.strip() for line in lines if is_valid_number(line)]
        output_callback(f"{path.name} → {len(numbers)} valid phone numbers")

        if 'csv' in formats:
            convert_to_csv(numbers, base_name)
        if 'json' in formats:
            convert_to_json(numbers, base_name)
        if 'txt' in formats:
            convert_to_clean_txt(numbers, base_name)

        total_numbers += len(numbers)

    end = time.time()
    output_callback(f"\nDONE: {total_numbers} phone numbers converted in {end - start:.2f} seconds.")
    output_callback(f"Output folder: {OUTPUT_DIR.resolve()}")


class PhoneGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PhoneGen Converter")
        self.file_paths = []

        self.setup_widgets()

    def setup_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")

        self.file_label = ttk.Label(frame, text="No files selected")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky="w")

        ttk.Button(frame, text="Select .txt Files", command=self.select_files).grid(row=1, column=0, pady=5)

        self.format_csv = tk.BooleanVar()
        self.format_json = tk.BooleanVar()
        self.format_txt = tk.BooleanVar()

        ttk.Checkbutton(frame, text="CSV", variable=self.format_csv).grid(row=1, column=1)
        ttk.Checkbutton(frame, text="JSON", variable=self.format_json).grid(row=1, column=2)
        ttk.Checkbutton(frame, text="Clean TXT", variable=self.format_txt).grid(row=1, column=3)

        ttk.Button(frame, text="Convert", command=self.run_conversion).grid(row=2, column=0, columnspan=2, pady=10)

        self.output_box = tk.Text(frame, height=10, width=80, state="disabled")
        self.output_box.grid(row=3, column=0, columnspan=4)

    def select_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        self.file_paths = list(paths)
        if self.file_paths:
            self.file_label.config(text=f"Selected: {len(self.file_paths)} file(s)")
        else:
            self.file_label.config(text="No files selected")

    def write_output(self, message):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", message + "\n")
        self.output_box.configure(state="disabled")
        self.output_box.see("end")

    def run_conversion(self):
        if not self.file_paths:
            messagebox.showerror("Error", "No files selected")
            return

        formats = set()
        if self.format_csv.get():
            formats.add('csv')
        if self.format_json.get():
            formats.add('json')
        if self.format_txt.get():
            formats.add('txt')

        if not formats:
            messagebox.showerror("Error", "No formats selected")
            return

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.configure(state="disabled")

        process_files(self.file_paths, formats, self.write_output)


if __name__ == "__main__":
    root = tk.Tk()
    app = PhoneGenGUI(root)
    root.mainloop()
