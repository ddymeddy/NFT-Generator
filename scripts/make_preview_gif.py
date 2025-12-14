import os
from PIL import Image
from .config import COLORS, PREVIEW_MAX_SIZE, PREVIEW_DURATION, PREVIEW_EVERY_N

OUTPUT_ROOT = "output"
PREVIEW_OUT = "preview"

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def numeric_sort_key(filename: str):
    # "123.png" -> 123
    name = os.path.splitext(filename)[0]
    try:
        return int(name)
    except:
        return 10**18

def load_frames_from_output(color: str):
    folder = os.path.join(OUTPUT_ROOT, color)
    if not os.path.isdir(folder):
        print(f"⚠️ Folder tidak ada: {folder}")
        return []

    files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    files.sort(key=numeric_sort_key)

    # sampling (kalau 300 frame terlalu besar, bisa ambil tiap N)
    files = files[::PREVIEW_EVERY_N]

    frames = []
    for f in files:
        path = os.path.join(folder, f)
        img = Image.open(path).convert("RGBA")

        # downscale agar ukuran GIF tidak meledak
        img.thumbnail(PREVIEW_MAX_SIZE)

        # GIF butuh mode P (palette) agar lebih kecil
        frames.append(img.convert("P", palette=Image.Palette.ADAPTIVE))

    return frames

def save_gif(frames, out_path):
    if not frames:
        print(f"⚠️ Tidak ada frame untuk {out_path}")
        return

    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=PREVIEW_DURATION,
        loop=0,
        optimize=True
    )
    print(f"✅ Saved: {out_path} ({len(frames)} frames)")

def main():
    ensure_dir(PREVIEW_OUT)

    # 1) Preview per warna
    all_frames = []
    for color in COLORS:
        frames = load_frames_from_output(color)
        save_gif(frames, os.path.join(PREVIEW_OUT, f"preview_{color}.gif"))
        all_frames.extend(frames)

    # 2) Preview gabungan semua warna (abu -> orange -> putih)
    save_gif(all_frames, os.path.join(PREVIEW_OUT, "preview_all.gif"))

if __name__ == "__main__":
    main()
