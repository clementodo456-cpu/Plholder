from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from services.image_generator import create_placeholder_image
from utils.helpers import parse_dimension_string
from aiogram.types import BufferedInputFile

router = Router()

@router.message(Command("placeholder"))
async def cmd_placeholder(message: Message):
    """
    Quick command endpoint.
    Usage: /placeholder 800 600
    """
    args = message.text.split()[1:]
    
    if len(args) < 2:
        await message.answer("⚠️ Usage: `/placeholder <width> <height>`\nExample: `/placeholder 800 600`", parse_mode="Markdown")
        return

    dim = parse_dimension_string(f"{args[0]}x{args[1]}")
    if not dim:
        await message.answer("❌ Invalid dimensions. Example: `/placeholder 800 600`", parse_mode="Markdown")
        return

    w, h = dim
    if not (50 <= w <= 2000 and 50 <= h <= 2000):
        await message.answer("⚠️ Dimensions must be between 50x50 and 2000x2000.", parse_mode="Markdown")
        return

    msg = await message.answer("⏳ Generating placeholder...")
    try:
        image_bytes = create_placeholder_image(
            width=w,
            height=h,
            bg_color="#CCCCCC",
            text_color="#333333",
            text=f"{w} × {h}",
            image_format="PNG"
        )
        input_file = BufferedInputFile(image_bytes.getvalue(), filename=f"placeholder_{w}x{h}.png")
        await message.answer_photo(photo=input_file, caption=f"✨ Quick Placeholder: `{w}×{h}`", parse_mode="Markdown")
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Failed to generate placeholder.")
