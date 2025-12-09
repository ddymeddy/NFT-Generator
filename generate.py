import os
import json
import random
from PIL import Image
from config import traits_config, TOTAL_NFT, ASSETS_DIR, OUTPUT_IMG, OUTPUT_META


# ---------------------------
# PILIH TRAIT BERDASARKAN RARITY
# ---------------------------
def choose_trait(traits):
    names = list(traits.keys())
    weights = list(traits.values())
    return random.choices(names, weights=weights, k=1)[0]


# ---------------------------
# MERGE LAYER PNG
# ---------------------------
def merge_layers(layers):
    base = layers[0]
    for layer in layers[1:]:
        base = Image.alpha_composite(base, layer)
    return base


# ---------------------------
# SAVE METADATA
# ---------------------------
def save_metadata(token_id, filename, attributes):
    data = {
        "name": f"NFT #{token_id}",
        "description": "Auto-generated NFT variation",
        "image": f"{OUTPUT_IMG}/{filename}.png",
        "attributes": [
            {"trait_type": t, "value": v.replace(".png", "")}
            for t, v in attributes.items()
        ]
    }

    # hanya 00000.json, bukan 0.json
    meta_filename = f"{filename}.json"
    meta_path = os.path.join(OUTPUT_META, meta_filename)

    with open(meta_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[✔] Metadata saved: {meta_filename}")


# ---------------------------
# GENERATE SATU NFT
# ---------------------------
def generate_traits_hash():
    chosen = {}
    for trait, files in traits_config.items():
        chosen_file = choose_trait(files)
        chosen[trait] = chosen_file
    return chosen, hash(frozenset(chosen.items()))


def generate_nft_image(filename, chosen_traits):
    layers = []

    for trait_folder, trait_file in chosen_traits.items():
        img_path = os.path.join(ASSETS_DIR, trait_folder, trait_file)
        img = Image.open(img_path).convert("RGBA")
        layers.append(img)

    final = merge_layers(layers)
    final.save(os.path.join(OUTPUT_IMG, f"{filename}.png"))


# ---------------------------
# MAIN GENERATOR
# ---------------------------
def main():
    os.makedirs(OUTPUT_IMG, exist_ok=True)
    os.makedirs(OUTPUT_META, exist_ok=True)

    print("\n=== GENERATING NFT COLLECTION ===")

    used_hashes = set()
    token_id = 0

    while token_id < TOTAL_NFT:
        chosen_traits, traits_hash = generate_traits_hash()

        # Cek duplicate
        if traits_hash in used_hashes:
            continue  # skip & regenerate

        used_hashes.add(traits_hash)

        filename = str(token_id).zfill(5)

        print(f"\n[✔] NFT #{token_id} UNIQUE — generating...")

        # Generate image
        generate_nft_image(filename, chosen_traits)

        # Save metadata
        save_metadata(token_id, filename, chosen_traits)

        print(f"[OK] Saved {filename}.png & metadata")

        token_id += 1

    print("\n=== DONE — All NFTs generated UNIQUE ===")


if __name__ == "__main__":
    main()
