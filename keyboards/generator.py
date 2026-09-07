from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SIZE_PRESETS, COLOR_PRESETS

def get_size_keyboard() -> InlineKeyboardMarkup:
    keyboard = []
    # 2 buttons per row
    row = []
    for index, label in enumerate(SIZE_PRESETS.keys()):
        row.append(InlineKeyboardButton(text=label, callback_data=f"size_preset:{index}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton(text="✏️ Custom Size", callback_data="size_custom")])
    keyboard.append([InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_generation")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_color_keyboard(color_type: str) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    for name, hex_code in COLOR_PRESETS.items():
        row.append(InlineKeyboardButton(text=f"{name}", callback_data=f"{color_type}_preset:{hex_code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton(text="🎨 Custom HEX Code", callback_data=f"{color_type}_custom")])
    keyboard.append([
        InlineKeyboardButton(text="🔙 Back", callback_data="back_to_size"),
        InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_generation")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_text_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Use Default (Dimensions)", callback_data="text_default")],
            [InlineKeyboardButton(text="🚫 No Text", callback_data="text_none")],
            [InlineKeyboardButton(text="✏️ Enter Custom Text", callback_data="text_custom")],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_bg_color"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_generation")
            ]
        ]
    )

def get_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="PNG", callback_data="format:PNG"),
                InlineKeyboardButton(text="JPG", callback_data="format:JPG"),
                InlineKeyboardButton(text="WEBP", callback_data="format:WEBP")
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_text_color"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_generation")
            ]
        ]
    )

def get_preview_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Generate Image", callback_data="confirm_generate")],
            [
                InlineKeyboardButton(text="✏️ Edit Settings", callback_data="start_generator"),
                InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_generation")
            ]
        ]
    )

def get_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Create Another", callback_data="start_generator")],
            [InlineKeyboardButton(text="⚙️ Change Settings", callback_data="confirm_generate_edit")]
        ]
    )
