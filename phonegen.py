import random
import multiprocessing
import os
import signal
print("\n \nWelcome to phonegen by casxx.deb or also known as ShadyShift :). \nCan you make a choice? \n \n")
print("IMPORTANT! This project not a final release, I will add more features in the future! If you have ideas, fork the project or reach out to me! \n \n")

#made with <3 by Casxx.deb or also known on my github as ShadyShift
#This is my simple yet effective phonegen

COUNTRY_PHONE_DATA = { #Used later for ask with countrie.
    'US': {'code': b'+1 ', 'prefixes': [b'201',b'202',b'212',b'213',b'310',b'415',b'646',b'718',b'917'], 'length':7},
    'NL': {'code': b'+31 ', 'prefixes': [b'6'], 'length':8},
    'GB': {'code': b'+44 ', 'prefixes': [b'7'], 'length':9},
    'DE': {'code': b'+49 ', 'prefixes': [b'15',b'16',b'17'], 'length':8},
    'FR': {'code': b'+33 ', 'prefixes': [b'6',b'7'], 'length':8},
    'IN': {'code': b'+91 ', 'prefixes': [b'9',b'8',b'7',b'6'], 'length':9},
    'BR': {'code': b'+55 ', 'prefixes': [b'9',b'8',b'7'], 'length':8},
    'AU': {'code': b'+61 ', 'prefixes': [b'4'], 'length':8},
    'CA': {'code': b'+1 ', 'prefixes': [b'204',b'236',b'250',b'289',b'306',b'343',b'365',b'403',b'416',b'418'], 'length':7},
    'ZA': {'code': b'+27 ', 'prefixes': [b'6',b'7',b'8'], 'length':7},
    'RU': {'code': b'+7 ', 'prefixes': [b'9'], 'length':9},
    'MX': {'code': b'+52 ', 'prefixes': [b'55',b'56',b'33'], 'length':7},
    'JP': {'code': b'+81 ', 'prefixes': [b'70',b'80',b'90'], 'length':8},
    'KR': {'code': b'+82 ', 'prefixes': [b'10'], 'length':8},
    'IT': {'code': b'+39 ', 'prefixes': [b'3'], 'length':9},
    'ES': {'code': b'+34 ', 'prefixes': [b'6',b'7'], 'length':8},
    'SE': {'code': b'+46 ', 'prefixes': [b'7'], 'length':8},
    'NO': {'code': b'+47 ', 'prefixes': [b'4',b'9'], 'length':7},
    'FI': {'code': b'+358 ', 'prefixes': [b'4',b'5'], 'length':7},
    'PL': {'code': b'+48 ', 'prefixes': [b'5',b'6',b'7'], 'length':7},
    'BE': {'code': b'+32 ', 'prefixes': [b'4'], 'length':8},
    'AT': {'code': b'+43 ', 'prefixes': [b'6'], 'length':7},
    'CH': {'code': b'+41 ', 'prefixes': [b'7'], 'length':7},
    'IE': {'code': b'+353 ', 'prefixes': [b'8',b'9'], 'length':7},
    'NZ': {'code': b'+64 ', 'prefixes': [b'2',b'21',b'22',b'27'], 'length':6},
    'SG': {'code': b'+65 ', 'prefixes': [b'8',b'9'], 'length':7},
    'MY': {'code': b'+60 ', 'prefixes': [b'1'], 'length':8},
    'TH': {'code': b'+66 ', 'prefixes': [b'8',b'9'], 'length':7},
    'PH': {'code': b'+63 ', 'prefixes': [b'9'], 'length':9},
    'AR': {'code': b'+54 ', 'prefixes': [b'9'], 'length':8},
    'CL': {'code': b'+56 ', 'prefixes': [b'9'], 'length':8},
    'CO': {'code': b'+57 ', 'prefixes': [b'3',b'5'], 'length':7},
    'EG': {'code': b'+20 ', 'prefixes': [b'10',b'11'], 'length':8},
    'UA': {'code': b'+380 ', 'prefixes': [b'50',b'67',b'96',b'97'], 'length':7},
    'IL': {'code': b'+972 ', 'prefixes': [b'50',b'52',b'54',b'55'], 'length':7},
    'TR': {'code': b'+90 ', 'prefixes': [b'5'], 'length':9},
    'SA': {'code': b'+966 ', 'prefixes': [b'5'], 'length':8},
    'AE': {'code': b'+971 ', 'prefixes': [b'50',b'55',b'56'], 'length':7},
    'ID': {'code': b'+62 ', 'prefixes': [b'8'], 'length':8},
    'VN': {'code': b'+84 ', 'prefixes': [b'9'], 'length':8},
    'PK': {'code': b'+92 ', 'prefixes': [b'3'], 'length':9},
    'NG': {'code': b'+234 ', 'prefixes': [b'7',b'8',b'9'], 'length':7},
    'KE': {'code': b'+254 ', 'prefixes': [b'7'], 'length':7},
}
#Add more if neccary 
def generate_numbers(countries, batch_size, verbose, max_bytes, temp_filename, stop_flag):
    total_written = 0
    with open(temp_filename, 'wb', buffering=16*1024*1024) as f:
        while not stop_flag.value:
            batch = []
            for _ in range(batch_size):
                country = random.choice(countries)
                data = COUNTRY_PHONE_DATA[country]
                prefix = random.choice(data['prefixes'])
                length = data['length']
                number_body = bytearray(random.choice(b'0123456789') for _ in range(length))
                number_bytes = data['code'] + prefix + number_body + b'\n'

                if verbose:
                    print(number_bytes.decode('ascii').strip())

                batch.append(number_bytes)

            chunk = b''.join(batch)
            f.write(chunk)
            total_written += len(chunk)

            if max_bytes > 0 and total_written >= max_bytes:
                stop_flag.value = True
                break

def main():
    print("Available countries:", ', '.join(sorted(COUNTRY_PHONE_DATA.keys())))
    countries_input = input("Enter country codes (comma separated, or 'ALL' for all): ").strip().upper()
    if countries_input == 'ALL':
        countries = list(COUNTRY_PHONE_DATA.keys())
    else:
        countries = [c.strip() for c in countries_input.split(",") if c.strip() in COUNTRY_PHONE_DATA]

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

    # Signal handler to catch Ctrl+C and stop gracefully
    def signal_handler(sig, frame):
        print("\nStopping gracefully...")
        stop_flag.value = True

    signal.signal(signal.SIGINT, signal_handler)

    try:
        for i in range(cpu_count):
            p = multiprocessing.Process(target=generate_numbers, args=(
                countries, batch_size, verbose, max_bytes_per_worker, temp_files[i], stop_flag))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # Combine temp files into final file
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
                os.remove(tf)

if __name__ == "__main__":
    main()
