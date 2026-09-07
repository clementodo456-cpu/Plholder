from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🖼 Generate Image", callback_data="start_generator")],
            [
                InlineKeyboardButton(text="📐 Quick Sizes", callback_data="quick_sizes"),
                InlineKeyboardButton(text="📖 How It Works", callback_data="how_it_works")
            ],
            [InlineKeyboardButton(text="ℹ️ About", callback_data="about_bot")]
        ]
    )

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")]
        ]
    )
