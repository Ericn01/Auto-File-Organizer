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
        
