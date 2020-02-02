def str_bool(s: str) -> bool:
    """Converts string ('0' or '1') to boolean"""
    return s == '1'

def bool_str(b: bool) -> str:
    """Converts boolean to string ('0' or '1')"""
    return '1' if b else '0'