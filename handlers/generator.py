from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import SIZE_PRESETS, MIN_DIMENSION, MAX_DIMENSION, MAX_TEXT_LENGTH
from utils.helpers import parse_dimension_string, validate_hex_color
from services.image_generator import create_placeholder_image
from keyboards.generator import (
    get_size_keyboard,
    get_color_keyboard,
    get_text_keyboard,
    get_format_keyboard,
    get_preview_keyboard,
    get_result_keyboard
)
from keyboards.main import get_main_menu_keyboard

router = Router()

class GeneratorFSM(StatesGroup):
    waiting_for_custom_size = State()
    waiting_for_bg_color = State()
    waiting_for_custom_bg_color = State()
    waiting_for_text = State()
    waiting_for_custom_text = State()
    waiting_for_text_color = State()
    waiting_for_custom_text_color = State()
    waiting_for_format = State()
    preview = State()

# --- STEP 1: SIZE SELECTION ---

@router.callback_query(F.data.in_({"start_generator", "quick_sizes"}))
async def start_generator(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(GeneratorFSM.waiting_for_bg_color)
    await callback.message.edit_text(
        "📐 *Select Image Size*\nChoose a preset or click custom size:",
        parse_mode="Markdown",
        reply_markup=get_size_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("size_preset:"))
async def process_size_preset(callback: CallbackQuery, state: FSMContext):
    idx = int(callback.data.split(":")[1])
    preset_key = list(SIZE_PRESETS.keys())[idx]
    width, height = SIZE_PRESETS[preset_key]
    
    await state.update_data(width=width, height=height)
    await ask_bg_color(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "size_custom")
async def process_custom_size_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GeneratorFSM.waiting_for_custom_size)
    await callback.message.edit_text(
        f"✏️ *Enter Custom Dimensions*\nSend size as `Width x Height` (e.g. `800x600` or `1920 1080`).\n\n"
        f"Limits: Min {MIN_DIMENSION}x{MIN_DIMENSION}, Max {MAX_DIMENSION}x{MAX_DIMENSION}.",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(GeneratorFSM.waiting_for_custom_size)
async def process_custom_size_input(message: Message, state: FSMContext):
    dims = parse_dimension_string(message.text)
    if not dims:
        await message.answer("❌ Invalid format. Please enter dimensions like `800x600` or `1080 1080`:")
        return
    
    w, h = dims
    if not (MIN_DIMENSION <= w <= MAX_DIMENSION and MIN_DIMENSION <= h <= MAX_DIMENSION):
        await message.answer(f"❌ Dimensions out of range! Must be between {MIN_DIMENSION}x{MIN_DIMENSION} and {MAX_DIMENSION}x{MAX_DIMENSION}:")
        return

    await state.update_data(width=w, height=h)
    await ask_bg_color(message, state, edit=False)

# --- STEP 2: BACKGROUND COLOR ---

async def ask_bg_color(target_obj, state: FSMContext, edit: bool = True):
    await state.set_state(GeneratorFSM.waiting_for_bg_color)
    text = "🎨 *Select Background Color*\nChoose a preset color or enter custom HEX code:"
    kb = get_color_keyboard("bg")
    
    if edit:
        await target_obj.edit_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await target_obj.answer(text, parse_mode="Markdown", reply_markup=kb)

@router.callback_query(F.data.startswith("bg_preset:"))
async def process_bg_preset(callback: CallbackQuery, state: FSMContext):
    hex_code = callback.data.split(":")[1]
    await state.update_data(bg_color=hex_code)
    await ask_text_option(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "bg_custom")
async def process_custom_bg_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GeneratorFSM.waiting_for_custom_bg_color)
    await callback.message.edit_text(
        "🎨 *Enter Custom Background Color*\nSend HEX code (e.g., `#3498DB` or `EEEEEE`):",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(GeneratorFSM.waiting_for_custom_bg_color)
async def process_custom_bg_input(message: Message, state: FSMContext):
    hex_code = validate_hex_color(message.text)
    if not hex_code:
        await message.answer("❌ Invalid HEX color code. Please send a valid code like `#3498DB` or `#FFF`:")
        return

    await state.update_data(bg_color=hex_code)
    await ask_text_option(message, state, edit=False)

# --- STEP 3: TEXT OPTION ---

async def ask_text_option(target_obj, state: FSMContext, edit: bool = True):
    await state.set_state(GeneratorFSM.waiting_for_text)
    text = "✏️ *Select Text Option*\nWhat text should appear on the image?"
    kb = get_text_keyboard()
    
    if edit:
        await target_obj.edit_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await target_obj.answer(text, parse_mode="Markdown", reply_markup=kb)

@router.callback_query(F.data == "text_default")
async def process_text_default(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    default_text = f"{data['width']} × {data['height']}"
    await state.update_data(text=default_text)
    await ask_text_color(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "text_none")
async def process_text_none(callback: CallbackQuery, state: FSMContext):
    await state.update_data(text="")
    # If no text, jump directly to format selection
    await ask_format(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "text_custom")
async def process_text_custom_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GeneratorFSM.waiting_for_custom_text)
    await callback.message.edit_text(
        f"✏️ *Enter Custom Text*\nSend the text you want on the image (max {MAX_TEXT_LENGTH} characters):",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(GeneratorFSM.waiting_for_custom_text)
async def process_custom_text_input(message: Message, state: FSMContext):
    text_val = message.text.strip()
    if len(text_val) > MAX_TEXT_LENGTH:
        await message.answer(f"❌ Text too long! Maximum allowed is {MAX_TEXT_LENGTH} characters. Try again:")
        return

    await state.update_data(text=text_val)
    await ask_text_color(message, state, edit=False)

# --- STEP 4: TEXT COLOR ---

async def ask_text_color(target_obj, state: FSMContext, edit: bool = True):
    await state.set_state(GeneratorFSM.waiting_for_text_color)
    text = "🔤 *Select Text Color*\nChoose a preset color or enter custom HEX code:"
    kb = get_color_keyboard("txt")
    
    if edit:
        await target_obj.edit_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await target_obj.answer(text, parse_mode="Markdown", reply_markup=kb)

@router.callback_query(F.data.startswith("txt_preset:"))
async def process_txt_preset(callback: CallbackQuery, state: FSMContext):
    hex_code = callback.data.split(":")[1]
    await state.update_data(text_color=hex_code)
    await ask_format(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "txt_custom")
async def process_custom_txt_prompt(callback: CallbackQuery, state: FSMContext):
    await state.set_state(GeneratorFSM.waiting_for_custom_text_color)
    await callback.message.edit_text(
        "🔤 *Enter Custom Text Color*\nSend HEX code (e.g., `#FFFFFF` or `333333`):",
        parse_mode="Markdown"
    )
    await callback.answer()

@router.message(GeneratorFSM.waiting_for_custom_text_color)
async def process_custom_txt_input(message: Message, state: FSMContext):
    hex_code = validate_hex_color(message.text)
    if not hex_code:
        await message.answer("❌ Invalid HEX color code. Please send a valid code like `#FFFFFF` or `#000`:")
        return

    await state.update_data(text_color=hex_code)
    await ask_format(message, state, edit=False)

# --- STEP 5: FORMAT SELECTION ---

async def ask_format(target_obj, state: FSMContext, edit: bool = True):
    await state.set_state(GeneratorFSM.waiting_for_format)
    text = "📁 *Select Image Format*\nChoose format for your image:"
    kb = get_format_keyboard()
    
    if edit:
        await target_obj.edit_text(text, parse_mode="Markdown", reply_markup=kb)
    else:
        await target_obj.answer(text, parse_mode="Markdown", reply_markup=kb)

@router.callback_query(F.data.startswith("format:"))
async def process_format_selection(callback: CallbackQuery, state: FSMContext):
    img_format = callback.data.split(":")[1]
    await state.update_data(image_format=img_format)
    await show_preview(callback.message, state, edit=True)
    await callback.answer()

# --- STEP 6: PREVIEW & CONFIRM ---

async def show_preview(target_obj, state: FSMContext, edit: bool = True):
    await state.set_state(GeneratorFSM.preview)
    data = await state.get_data()
    
    text_display = data.get("text", "")
    if not text_display:
        text_display = "*(None)*"
        
    text_color_display = data.get("text_color", "N/A") if data.get("text") else "N/A"
    
    preview_text = (
        "🖼 *Placeholder Preview*\n\n"
        f"📐 *Size:* `{data['width']} × {data['height']}`\n"
        f"🎨 *Background:* `{data['bg_color']}`\n"
        f"✏️ *Text:* `{text_display}`\n"
        f"🔤 *Text Color:* `{text_color_display}`\n"
        f"📁 *Format:* `{data['image_format']}`"
    )
    kb = get_preview_keyboard()
    
    if edit:
        await target_obj.edit_text(preview_text, parse_mode="Markdown", reply_markup=kb)
    else:
        await target_obj.answer(preview_text, parse_mode="Markdown", reply_markup=kb)

# --- GENERATION IMPLEMENTATION ---

@router.callback_query(F.data == "confirm_generate")
@router.callback_query(F.data == "confirm_generate_edit")
async def generate_final_image(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data or "width" not in data:
        await callback.answer("⚠️ Session expired. Please start over.", show_alert=True)
        return

    await callback.message.edit_text("⚡ Generating your placeholder image...")
    
    try:
        image_bytes = create_placeholder_image(
            width=data["width"],
            height=data["height"],
            bg_color=data["bg_color"],
            text_color=data.get("text_color", "#333333"),
            text=data.get("text", ""),
            image_format=data["image_format"]
        )
        
        filename = f"placeholder_{data['width']}x{data['height']}.{data['image_format'].lower()}"
        input_file = BufferedInputFile(image_bytes.getvalue(), filename=filename)
        
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=input_file,
            caption="✨ *Your placeholder image is ready!*",
            parse_mode="Markdown",
            reply_markup=get_result_keyboard()
        )
    except Exception as e:
        await callback.message.answer("❌ An error occurred while generating the image. Please try again.")
    await callback.answer()

# --- BACK / CANCEL NAVIGATION ---

@router.callback_query(F.data == "back_to_size")
async def back_to_size(callback: CallbackQuery, state: FSMContext):
    await start_generator(callback, state)

@router.callback_query(F.data == "back_to_bg_color")
async def back_to_bg_color(callback: CallbackQuery, state: FSMContext):
    await ask_bg_color(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "back_to_text_color")
async def back_to_text_color(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("text"):
        await ask_text_option(callback.message, state, edit=True)
    else:
        await ask_text_color(callback.message, state, edit=True)
    await callback.answer()

@router.callback_query(F.data == "cancel_generation")
async def cancel_generation(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Image generation canceled.", reply_markup=get_main_menu_keyboard())
    await callback.answer()
