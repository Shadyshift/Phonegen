import time

import os

# Choose which dataset to use
try:
    from country_data import COUNTRY_PHONE_DATA
except ImportError:
    from landline_data_full import LANDLINE_PHONE_DATA as COUNTRY_PHONE_DATA

VALID_CODES = {
    data["code"].decode().strip(): {
        "prefixes": [p.decode() for p in data["prefixes"]],
        "length": data["length"]
    }
    for data in COUNTRY_PHONE_DATA.values()
    for code in [data["code"].decode().strip()]
}

def is_valid_number(line):
    try:
        line = line.decode().strip()
        if not line:
            return False, "Empty line"

        parts = line.split(" ", 1)
        if len(parts) != 2:
            return False, "Missing country code or number"

        code, number = parts
        if code not in VALID_CODES:
            return False, f"Unknown country code: {code}"

        if not number.isdigit():
            return False, "Contains non-digit characters"

        for prefix in VALID_CODES[code]["prefixes"]:
            if number.startswith(prefix):
                expected_length = VALID_CODES[code]["length"] + len(prefix)
                if len(number) != expected_length:
                    return False, f"Wrong number length: expected {expected_length}, got {len(number)}"
                return True, None

        return False, f"Invalid prefix in: {number}"
    except Exception as e:
        return False, f"Decode error: {e}"

def scan_output_file():
    filename = input("Enter the filename to scan (e.g. output.txt): ").strip()
    if not filename or not os.path.exists(filename):
        print(f"❌ File '{filename}' not found.")
        return

    start = time.time()
    bad_lines = []
    good_lines = []

    with open(filename, 'rb') as f:
        for idx, line in enumerate(f, 1):
            is_valid, reason = is_valid_number(line)
            if is_valid:
                good_lines.append(line)
            else:
                bad_lines.append((idx, line.decode(errors='ignore').strip(), reason))

    elapsed = time.time() - start
    print(f"\nScanned {idx} lines in {elapsed:.2f} seconds.")

    if bad_lines:
        print(f"\nFound {len(bad_lines)} invalid lines:\n")
        for lineno, text, reason in bad_lines[:20]:
            print(f"[Line {lineno}] {reason} → {text}")
        if len(bad_lines) > 20:
            print("... (more lines hidden)")

        choice = input("\nDelete bad lines and save cleaned file? (y/N): ").strip().lower()
        if choice == 'y':
            with open(filename, 'wb') as f:
                f.writelines(good_lines)
            print("Cleaned file saved.")
        else:
            print("No changes made.")
    else:
        print("No issues found!")

if __name__ == "__main__":
    scan_output_file()
