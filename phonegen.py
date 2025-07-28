
import random
import multiprocessing
import os
import signal

# User chooses data type
from landline_data_full import LANDLINE_PHONE_DATA
from country_data import COUNTRY_PHONE_DATA  # Assuming original mobile data lives here

print("\n \nWelcome to phonegen by casxx.deb or also known as ShadyShift :).\nCan you make a choice?\n \n")
print("IMPORTANT! This project is not a final release. I will add more features in the future! If you have ideas, fork the project or reach out to me!\n \n")
print("Also very important! +999 is a placeholder")

def generate_numbers(countries, batch_size, verbose, max_bytes, temp_filename, stop_flag, data_source):
    total_written = 0
    with open(temp_filename, 'wb', buffering=16*1024*1024) as f:
        while not stop_flag.value:
            batch = []
            for _ in range(batch_size):
                country = random.choice(countries)
                data = data_source[country]
                prefix = random.choice(data['prefixes'])
                length = data['length']
                number_body = bytearray(random.choices(b'0123456789', k=length))
                number_bytes = data['code'] + prefix + number_body + b'\n'

                if verbose:
                    print(number_bytes.decode('ascii', errors='ignore').strip())

                batch.append(number_bytes)

            chunk = b''.join(batch)
            f.write(chunk)
            total_written += len(chunk)

            if max_bytes > 0 and total_written >= max_bytes:
                stop_flag.value = True
                break

def main():
    use_landline = input("Generate extra countries? (y/N): ").strip().lower() == 'y'
    DATA_SOURCE = LANDLINE_PHONE_DATA if use_landline else COUNTRY_PHONE_DATA

    print("Available countries:", ', '.join(sorted(DATA_SOURCE.keys())))
    countries_input = input("Enter country codes (comma separated, or 'ALL' for all): ").strip().upper()
    if countries_input == 'ALL':
        countries = list(DATA_SOURCE.keys())
    else:
        countries = [c.strip() for c in countries_input.split(",") if c.strip() in DATA_SOURCE]

    if not countries:
        print("No valid countries selected.")
        return

    filename = input("Output filename (default output.txt): ").strip()
    if not filename:
        filename = "output.txt"

    max_mb = input("Max file size in MB (0 for unlimited): ").strip()
    try:
        max_bytes = int(max_mb) * 1024 * 1024
        if max_bytes < 0:
            max_bytes = 0
    except:
        max_bytes = 0

    verbose_input = input("Enable verbose mode? It is slower but also cooler (y/N): ").strip().lower()
    verbose = verbose_input == 'y'

    cpu_count = multiprocessing.cpu_count()
    print(f"Using {cpu_count} processes...")

    max_bytes_per_worker = max_bytes // cpu_count if max_bytes > 0 else 0
    batch_size = 100000

    stop_flag = multiprocessing.Value('b', False)

    temp_files = [f"temp_output_{i}.txt" for i in range(cpu_count)]
    processes = []

    def signal_handler(sig, frame):
        print("\nStopping gracefully...")
        stop_flag.value = True

    signal.signal(signal.SIGINT, signal_handler)

    try:
        for i in range(cpu_count):
            p = multiprocessing.Process(target=generate_numbers, args=(
                countries, batch_size, verbose, max_bytes_per_worker, temp_files[i], stop_flag, DATA_SOURCE))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        with open(filename, 'wb') as outfile:
            for tf in temp_files:
                with open(tf, 'rb') as infile:
                    while True:
                        chunk = infile.read(16*1024*1024)
                        if not chunk:
                            break
                        outfile.write(chunk)
                os.remove(tf)

        print(f"Done! Generated numbers saved in '{filename}'")

    except KeyboardInterrupt:
        stop_flag.value = True
        print("\nStopped by user, cleaning up...")
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()
        for tf in temp_files:
            if os.path.exists(tf):
                os.remove(tf) #removes tmp files

if __name__ == "__main__":
    main()
