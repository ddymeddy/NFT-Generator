# scripts/config.py
IMAGE_SIZE = (1024, 1024)

GIF_ROOT = "gifs"
GIF_DURATION = 300  # ms per frame

PREVIEW_MAX_SIZE = (512, 512)   # biar file gif gak kegedean
PREVIEW_DURATION = 120          # ms per frame
PREVIEW_EVERY_N = 1             # 1 = ambil semua; 2 = tiap 2 gambar, dst


ASSETS_DIR = "assets"
COLORS = ["abu", "orange", "putih"]
LAYERS = ["background", "badan", "kepala", "wajah", "props"]

TOTAL_PER_COLOR = 100  # jumlah NFT untuk tiap warna

NFT_NAME_PREFIX = "Abu Orange Putih NFT"
DESCRIPTION = "NFT collection generated from color-based layered assets."
