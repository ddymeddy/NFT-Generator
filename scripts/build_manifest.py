import os, json
from .config import COLORS

META_ROOT = "metadata"
VIEWER_DIR = "viewer"
OUT_FILE = os.path.join(VIEWER_DIR, "manifest.json")

def numeric_sort_key(name: str):
    try:
        return int(os.path.splitext(name)[0])
    except:
        return 10**18

def main():
    os.makedirs(VIEWER_DIR, exist_ok=True)
    items = []

    for color in COLORS:
        color_dir = os.path.join(META_ROOT, color)
        if not os.path.isdir(color_dir):
            continue

        files = [f for f in os.listdir(color_dir) if f.endswith(".json")]
        files.sort(key=numeric_sort_key)

        for f in files:
            token_id = os.path.splitext(f)[0]
            items.append({
                "color": color,
                "id": int(token_id),
                "meta": f"../metadata/{color}/{token_id}.json",
                "gif": f"../gifs/{color}/{token_id}.gif",
                "png": f"../output/{color}/{token_id}.png"
            })

    with open(OUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(items, fp, indent=2, ensure_ascii=False)

    print(f"✅ manifest dibuat: {OUT_FILE}")
    print(f"✅ total item: {len(items)}")

if __name__ == "__main__":
    main()
