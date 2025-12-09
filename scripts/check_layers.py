import os
from PIL import Image

ASSETS_DIR = "assets"

def is_transparent(img):
    if img.mode != "RGBA":
        return False

    alpha = img.split()[-1]
    return alpha.getextrema()[0] == 0  # cek apakah ada pixel transparan

def check_folder(folder):
    print(f"\nChecking folder: {folder}")
    for file in os.listdir(folder):
        if file.endswith(".png"):
            path = os.path.join(folder, file)
            img = Image.open(path)

            if not is_transparent(img):
                print(f"❌ NOT TRANSPARENT: {path}")
            else:
                print(f"✔ Transparent: {path}")

def main():
    print("=== Checking PNG Layers ===\n")

    for root, dirs, files in os.walk(ASSETS_DIR):
        for d in dirs:
            check_folder(os.path.join(root, d))

    print("\n=== Done Checking ===")

if __name__ == "__main__":
    main()
