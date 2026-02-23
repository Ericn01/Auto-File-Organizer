import re 
from argparse import ArgumentTypeError

def coerce_value(raw_value: str, data_type: str = "str"):
    if raw_value is None:
        return None

    match data_type:
        case "int":
            return int(raw_value)
        case "float":
            return float(raw_value)
        case "bool":
            if isinstance(raw_value, bool):
                return raw_value
            return str(raw_value).strip().lower() in ("true", "1", "yes", "y", "on")
        case "list":
            text = str(raw_value).strip()
            if not text:
                return []
            parts = text.split(",") if "," in text else text.split()
            return [p.strip() for p in parts if p.strip()]
        case _:
            return raw_value
        
def parse_size (size_str : str):
    """Parses a string size (e.g., 100MB, 2GB) into bytes."""
    units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024**3, "TB": 1024**4}
    size_str = size_str.upper() 
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([KMGT]B)$", size_str)

    if not match:
        try:
            bytes = int(size_str)
            return bytes 
        except ValueError:
            raise ArgumentTypeError(f"Invalid size format: {size_str}")
        
    number, unit = match.groups()
    return int(float(number) * units.get(unit, 1))
