import sys
import os

# Tambahkan root project ke PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OUTPUT_IMG
from PIL import Image

GIF_NAME = "collection_preview.gif"

def main():
    print("=== GENERATING GIF ===")

    files = sorted(f for f in os.listdir(OUTPUT_IMG) if f.endswith(".png"))

    if not files:
        print("No images found.")
        return

    images = [Image.open(os.path.join(OUTPUT_IMG, f)).convert("RGBA") for f in files]

    images[0].save(
        GIF_NAME,
        save_all=True,
        append_images=images[1:],
        duration=200,
        loop=0
    )

    print(f"GIF saved as {GIF_NAME}")


if __name__ == "__main__":
    main()
