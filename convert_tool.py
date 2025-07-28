import os
import csv
import json
import time
from pathlib import Path

def is_valid_number(line: str) -> bool:
    return line.strip().startswith('+') and line.strip()[1:].replace(' ', '').isdigit()

def convert_to_csv(numbers, base_path):
    csv_path = base_path.with_suffix('.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['PhoneNumber'])
        for number in numbers:
            writer.writerow([number])

def convert_to_json(numbers, base_path):
    json_path = base_path.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump({'phone_numbers': numbers}, json_file, indent=2)

def convert_to_clean_txt(numbers, base_path):
    clean_path = base_path.with_name(base_path.stem + '_clean.txt')
    with open(clean_path, 'w', encoding='utf-8') as txt_file:
        for number in numbers:
            txt_file.write(number + '\n')

def get_txt_files():
    return [f for f in os.listdir('.') if f.endswith('.txt')]

def prompt_files(files):
    print("Choose files to convert. Choose multiple seperated by a ,")
    for i, file in enumerate(files):
        print(f" [{i+1}] {file}")
    selected = input("Bestandnummers (bijv: 1,3,4): ").strip().split(',')
    return [files[int(i)-1] for i in selected if i.strip().isdigit() and 1 <= int(i) <= len(files)]

def prompt_formats():
    print("\nFiletype:")
    print(" [1] CSV")
    print(" [2] JSON")
    print(" [3] Clean TXT")
    selected = input("Choose a filetype or multiple seperated by a ,: ").strip().split(',')
    return {int(i) for i in selected if i.strip().isdigit() and 1 <= int(i) <= 3}

def main():
    files = get_txt_files()
    if not files:
        print("Didn't find any txt files")
        return

    selected_files = prompt_files(files)
    if not selected_files:
        print("Illigal files selected")
        return

    formats = prompt_formats()
    if not formats:
        print("Nothing selected")
        return

    total_numbers = 0
    start = time.time()

    for file in selected_files:
        path = Path(file)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        numbers = [line.strip() for line in lines if is_valid_number(line)]
        print(f"file: {file} → {len(numbers)} PhoneNumbers")

        if 1 in formats:
            convert_to_csv(numbers, path)
        if 2 in formats:
            convert_to_json(numbers, path)
        if 3 in formats:
            convert_to_clean_txt(numbers, path)

        total_numbers += len(numbers)

    end = time.time()
    print(f"\nREADY! {total_numbers} Phonenumbers in {end - start:.2f} seconds.")

if __name__ == "__main__":
    main()
