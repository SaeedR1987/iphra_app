
# logic/validators.py

from PyQt6.QtWidgets import QMessageBox

def validate_type(value, expected_type):
    """
    Checks whether a value can be safely converted to the expected type.

    Parameters:
        value (any): The input to check (usually a string from a widget)
        expected_type (type): The expected Python type (e.g., float, int, bool, str)

    Returns:
        (bool, converted_value or error message)
    """
    try:
        if expected_type == bool:
            # Accept strings like "true", "false", "1", "0"
            if isinstance(value, str):
                value = value.strip().lower()
                if value in ("true", "1"):
                    return True, True
                elif value in ("false", "0"):
                    return True, False
                else:
                    raise ValueError(f"Cannot convert '{value}' to boolean.")
            else:
                return True, bool(value)
        else:
            return True, expected_type(value)
    except (ValueError, TypeError) as e:
        return False, f"Expected {expected_type.__name__}, but got invalid value: {value!r}"

def validate_float(text, name, min_value=None, max_value=None, parent=None):
    try:
        value = float(text)
        if min_value is not None and value < min_value:
            raise ValueError(f"{name} must be at least {min_value}.")
        if max_value is not None and value > max_value:
            raise ValueError(f"{name} must be at most {max_value}.")
        return value
    except ValueError as e:
        show_error(f"Invalid value for {name}: {e}", parent)
        return None
    
def validate_int(text, name, min_value=None, max_value=None, parent=None):
    try:
        value = int(text)
        if min_value is not None and value < min_value:
            raise ValueError(f"{name} must be at least {min_value}.")
        if max_value is not None and value > max_value:
            raise ValueError(f"{name} must be at most {max_value}.")
        return value
    except ValueError as e:
        show_error(f"Invalid value for {name}: {e}", parent)
        return None
    
def show_error(message, parent=None):
    QMessageBox.warning(parent, "Input Error", message)