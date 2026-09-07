import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# Constraints
MIN_DIMENSION = 50
MAX_DIMENSION = 2000
MAX_TEXT_LENGTH = 100

# Color Presets (Name -> HEX)
COLOR_PRESETS = {
    "White": "#FFFFFF",
    "Black": "#000000",
    "Gray": "#808080",
    "Light Gray": "#D3D3D3",
    "Blue": "#3498DB",
    "Green": "#2ECC71",
    "Red": "#E74C3C",
    "Purple": "#9B59B6"
}

# Dimension Presets (Label -> (Width, Height))
SIZE_PRESETS = {
    "150 × 150 (Thumbnail)": (150, 150),
    "300 × 200 (Small)": (300, 200),
    "600 × 400 (Medium)": (600, 400),
    "800 × 600 (Standard)": (800, 600),
    "1200 × 800 (Large)": (1200, 800),
    "1920 × 1080 (Full HD)": (1920, 1080),
    "1080 × 1080 (Square)": (1080, 1080),
    "1080 × 1350 (Portrait)": (1080, 1350),
    "1080 × 1920 (Story)": (1080, 1920)
}
