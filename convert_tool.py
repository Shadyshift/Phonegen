import os
import csv
import json
import time
from pathlib import Path

OUTPUT_DIR = Path("output")

def is_valid_number(line: str) -> bool:
    line = line.strip()
    # Remove formatting characters
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

def get_txt_files():
    return [f for f in os.listdir('.') if f.endswith('.txt')]

def prompt_files(files):
    print("Choose files to convert. Choose multiple separated by commas:")
    for i, file in enumerate(files):
        print(f" [{i+1}] {file}")
    selected = input("File numbers (e.g. 1,3,4): ").strip().split(',')
    return [files[int(i)-1] for i in selected if i.strip().isdigit() and 1 <= int(i) <= len(files)]

def prompt_formats():
    print("\nSelect file type(s) to generate:")
    print(" [1] CSV")
    print(" [2] JSON")
    print(" [3] Clean TXT")
    selected = input("Choose one or more types (e.g. 1,2): ").strip().split(',')
    return {int(i) for i in selected if i.strip().isdigit() and 1 <= int(i) <= 3}

def main():
    files = get_txt_files()
    if not files:
        print("No .txt files found.")
        return

    selected_files = prompt_files(files)
    if not selected_files:
        print("No valid files selected.")
        return

    formats = prompt_formats()
    if not formats:
        print("No output format selected.")
        return

    ensure_output_dir()

    total_numbers = 0
    start = time.time()

    for file in selected_files:
        path = Path(file)
        base_name = path.stem
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        numbers = [line.strip() for line in lines if is_valid_number(line)]
        print(f"{file} → {len(numbers)} valid phone numbers")

        if 1 in formats:
            convert_to_csv(numbers, base_name)
        if 2 in formats:
            convert_to_json(numbers, base_name)
        if 3 in formats:
            convert_to_clean_txt(numbers, base_name)

        total_numbers += len(numbers)

    end = time.time()
    print(f"\nDONE: {total_numbers} valid phone numbers converted in {end - start:.2f} seconds.")
    print(f"Output saved to: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
