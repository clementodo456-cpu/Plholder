from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.main import get_main_menu_keyboard, get_back_to_main_keyboard

router = Router()

START_TEXT = (
    "✨ *Welcome to Placeholder Generator Bot!*\n\n"
    "I help you instantly generate custom placeholder images for web development, UI design, and mockups.\n\n"
    "⚙️ *Features:*\n"
    "• Custom or preset dimensions up to 2000x2000\n"
    "• Custom HEX background & text colors\n"
    "• Auto-scaled dynamic centered text\n"
    "• Supports PNG, JPG, and WEBP formats\n\n"
    "Click *🖼 Generate Image* below to get started!"
)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(START_TEXT, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())

@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(START_TEXT, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())
    await callback.answer()

@router.callback_query(F.data == "how_it_works")
async def cb_how_it_works(callback: CallbackQuery):
    text = (
        "📖 *How It Works*\n\n"
        "1. Click *Generate Image*.\n"
        "2. Choose image size (Presets or Custom width × height).\n"
        "3. Choose a Background Color (Presets or HEX code like `#3498DB`).\n"
        "4. Choose Text options (Default dimensions, custom string, or empty).\n"
        "5. Choose Text Color.\n"
        "6. Select output format (`PNG`, `JPG`, `WEBP`).\n"
        "7. Review settings & generate your image instantly!"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_main_keyboard())
    await callback.answer()

@router.callback_query(F.data == "about_bot")
async def cb_about_bot(callback: CallbackQuery):
    text = (
        "ℹ️ *About Plholdergenbot*\n\n"
        "• *Version:* 1.0.0\n"
        "• *Framework:* Python 3.11 + aiogram 3.x\n"
        "• *Engine:* Pillow (PIL)\n"
        "• *Deployment:* Render Worker\n\n"
        "Built for speed, reliability, and precision."
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=get_back_to_main_keyboard())
    await callback.answer()
