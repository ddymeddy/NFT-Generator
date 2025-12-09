import os
import re
from config import TOTAL_NFT, OUTPUT_IMG, OUTPUT_META

def trim_folder(folder, extension):
    """
    Menghapus file yang nomornya melebihi TOTAL_NFT.
    """
    pattern = re.compile(r"(\d+)\." + extension + "$")
    removed = 0

    for filename in os.listdir(folder):
        match = pattern.search(filename)
        if match:
            number = int(match.group(1))
            if number >= TOTAL_NFT:
                filepath = os.path.join(folder, filename)
                os.remove(filepath)
                removed += 1
                print(f"[🗑] Removed {filepath}")

    return removed


def auto_trim():
    print(f"\n=== AUTO-TRIM NFT FILES ===")
    print(f"Maksimal file yang diperbolehkan: {TOTAL_NFT}\n")

    # Trim PNG output
    removed_png = trim_folder(OUTPUT_IMG, "png")

    # Trim JSON metadata
    removed_json = trim_folder(OUTPUT_META, "json")

    print("\n=== DONE TRIMMING ===")
    print(f"Total PNG deleted : {removed_png}")
    print(f"Total JSON deleted: {removed_json}\n")

    if removed_png == 0 and removed_json == 0:
        print("✔ Tidak ada file yang perlu dihapus.")
    else:
        print("✔ Output sudah dirapikan sesuai TOTAL_NFT.")


if __name__ == "__main__":
    auto_trim()
