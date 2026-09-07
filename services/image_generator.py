import io
import os
from PIL import Image, ImageDraw, ImageFont
from config import MIN_DIMENSION, MAX_DIMENSION

def get_font(font_size: int) -> ImageFont.ImageFont:
    """Loads default or system TrueType font."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # Standard Debian/Render font
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "C:\\Windows\\Fonts\\arial.ttf", # Windows fallback
        "/System/Library/Fonts/Helvetica.ttc" # macOS fallback
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_placeholder_image(
    width: int,
    height: int,
    bg_color: str,
    text_color: str,
    text: str,
    image_format: str
) -> io.BytesIO:
    """Generates placeholder image and returns in-memory BytesIO buffer."""
    
    # Enforce safe dimension limits
    width = max(MIN_DIMENSION, min(width, MAX_DIMENSION))
    height = max(MIN_DIMENSION, min(height, MAX_DIMENSION))
    
    format_upper = image_format.upper()
    mode = "RGB" if format_upper == "JPEG" or format_upper == "JPG" else "RGBA"
    
    # Create Base Canvas
    image = Image.new(mode, (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    if text:
        # Dynamically scale font to fit image boundaries
        max_text_width = int(width * 0.85)
        max_text_height = int(height * 0.85)
        
        font_size = min(width, height)
        font = get_font(font_size)
        
        # Calculate dynamic size using font bounding box
        while font_size > 8:
            font = get_font(font_size)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            if text_w <= max_text_width and text_h <= max_text_height:
                break
            font_size -= 2
            
        # Recalculate text size for precise centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = (width - text_w) / 2 - bbox[0]
        y = (height - text_h) / 2 - bbox[1]
        
        draw.text((x, y), text, fill=text_color, font=font)
        
    # Save Image to Memory Buffer
    buffer = io.BytesIO()
    save_format = "JPEG" if format_upper in ["JPG", "JPEG"] else format_upper
    
    if save_format == "JPEG":
        image = image.convert("RGB")
        image.save(buffer, format=save_format, quality=95)
    elif save_format == "WEBP":
        image.save(buffer, format=save_format, quality=90)
    else:
        image.save(buffer, format="PNG", optimize=True)
        
    buffer.seek(0)
    return buffer
