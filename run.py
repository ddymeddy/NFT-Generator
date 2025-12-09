import sys
import os
import subprocess

# Path folder scripts
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

# Mapping command → script yang dijalankan
COMMANDS = {
    "gif": "generate_gif.py",
    "clean": "clean_metadata.py",
    "normalize": "normalize_assets.py",
    "check": "check_layers.py",
    "trim": "auto_trim.py",
}

def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.exists(script_path):
        print(f"❌ Script tidak ditemukan: {script_path}")
        return

    print(f"▶ Menjalankan: {script_name}\n")
    subprocess.run(["python", script_path])


def main():
    if len(sys.argv) < 2:
        print("\n❗ Penggunaan:")
        print("  python run.py <command>\n")
        print("Perintah tersedia:")
        for cmd in COMMANDS:
            print(f"  - {cmd}")
        print("\nContoh:")
        print("  python run.py gif")
        print("  python run.py clean\n")
        return

    command = sys.argv[1]

    if command not in COMMANDS:
        print(f"❌ Command '{command}' tidak dikenali.")
        print("Gunakan salah satu dari:")
        for cmd in COMMANDS:
            print(f"  - {cmd}")
        return

    run_script(COMMANDS[command])


if __name__ == "__main__":
    main()
