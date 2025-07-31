import os
import re
import time
from pathlib import Path

def is_valid_phone_number(line: str) -> bool:
    line = line.strip()
    # Remove common formatting characters: spaces, dashes, parentheses
    cleaned = re.sub(r"[()\-\s]", "", line)
    # Match cleaned format: must start with + and followed by 8–15 digits
    return re.fullmatch(r"\+\d{8,15}", cleaned) is not None

def scan_file(filename: str):
    print(f"\nScanning '{filename}'...")
    start = time.time()

    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    valid_lines = []
    invalid_lines = []

    for line in lines:
        if is_valid_phone_number(line):
            valid_lines.append(line)
        else:
            invalid_lines.append(line.strip())

    duration = time.time() - start
    print(f"Scan completed in {duration:.2f} seconds.")
    print(f"Valid lines: {len(valid_lines)}")
    print(f"Invalid lines: {len(invalid_lines)}")

    if invalid_lines:
        print("\nInvalid entries:")
        for bad in invalid_lines:
            print(f"  {bad}")

        choice = input("\nDo you want to delete invalid entries from this file? (y/N): ").strip().lower()
        if choice == 'y':
            with open(filename, 'w', encoding='utf-8') as f:
                f.writelines(valid_lines)
            print("Invalid entries removed.")

def detect_txt_files():
    txt_files = [f for f in Path('.').glob("*.txt") if f.is_file()]
    output_files = []
    print("Detected .txt files with phone-like numbers:")
    for file in txt_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith('+') and any(char.isdigit() for char in line):
                    output_files.append(str(file))
                    print(f"  {file}")
                    break
    return output_files

def main():
    print("PhoneGen Scanner - Fast mode")

    candidates = detect_txt_files()
    if not candidates:
        print("No output .txt files found with phone-like data.")
        return

    filename = input("\nEnter the filename you want to scan (or leave blank to cancel): ").strip()
    if filename and os.path.exists(filename):
        scan_file(filename)
    else:
        print("Cancelled or file not found.")

if __name__ == "__main__":
    main()
