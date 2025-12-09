import os
from PIL import Image

ASSETS_DIR = "assets"
CANVAS_SIZE = (512, 512)

def normalize_image(path):
    img = Image.open(path).convert("RGBA")
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))

    # center image
    x = (CANVAS_SIZE[0] - img.width) // 2
    y = (CANVAS_SIZE[1] - img.height) // 2

    canvas.paste(img, (x, y), img)
    canvas.save(path)

    print(f"✔ Normalized: {path}")


def main():
    print("=== NORMALIZING ASSETS ===\n")

    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.endswith(".png"):
                normalize_image(os.path.join(root, file))

    print("\n✔ All assets normalized!")

if __name__ == "__main__":
    main()
