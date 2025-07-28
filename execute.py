import subprocess
import os
import platform
import sys
#phonegen made with <3 by casxx.deb
def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def show_help():
    print("""
Available commands:
  phonegen start         → Start phone number generator
  phonegen scan          → Scan .txt output files for bad numbers
  convert                → Convert .txt files to .csv or .json
  clear                  → Clear the screen
  help                   → Show this help menu
  quit / exit            → Exit the launcher
""")

def main():
    print("Welcome to the PhoneGen Launcher. Type 'help' for commands.")
    print("DISCLAIMER: This software is provided as is, without warranty of any kind. Use at your own risk.")
    while True:
        command = input(">>> ").strip().lower()

        if command == "phonegen start":
            subprocess.run([sys.executable, "phonegen.py"])

        elif command == "phonegen scan":
            subprocess.run([sys.executable, "scan_output.py"])

        elif command == "convert":
            subprocess.run([sys.executable, "convert_tool.py"])

        elif command in ["quit", "exit"]:
            print("Goodbye!")
            break

        elif command == "clear":
            clear_console()

        elif command == "help":
            show_help()

        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()
