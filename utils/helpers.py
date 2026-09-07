import re
from typing import Tuple, Optional

HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

def validate_hex_color(color_code: str) -> Optional[str]:
    """Validates and normalizes HEX color input (e.g. #FFF or #FFFFFF)."""
    if not color_code:
        return None
    
    color_code = color_code.strip()
    if not color_code.startswith("#"):
        color_code = f"#{color_code}"
        
    if HEX_COLOR_PATTERN.match(color_code):
        if len(color_code) == 4: # #RGB -> #RRGGBB
            color_code = "#" + "".join(c * 2 for c in color_code[1:])
        return color_code.upper()
    return None

def parse_dimension_string(input_str: str) -> Optional[Tuple[int, int]]:
    """Parses user string into (width, height) tuple."""
    cleaned = input_str.lower().strip().replace(" ", "")
    parts = re.split(r"[x,*×]", cleaned)
    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
        return int(parts[0]), int(parts[1])
    return None
