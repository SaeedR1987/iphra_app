
# logic/validators.py

from PyQt6.QtWidgets import QMessageBox

def validate_type(value, expected_type, name="Value", parent=None):
    """
    Validates whether a value is of the expected type or can be safely converted to it.
    Displays a GUI error message using show_error if validation fails.

    Parameters:
        value (any): The input to validate (e.g., from a widget).
        expected_type (type): The desired Python type (float, int, bool, str, etc.).
        name (str): Field name for more informative error messages.
        parent (QWidget, optional): Parent widget for QMessageBox, if used in GUI.

    Returns:
        bool: True if value is valid or convertible to the expected type, False otherwise.
    """
    # Normalize string inputs (e.g., from QLineEdit)
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            if parent is None:
                print(f"Error: {name} must be a valid {expected_type.__name__}.")
                return False
            else:
                show_error(f"{name} cannot be empty.", parent)
                return False
            
    if isinstance(value, bool) and expected_type in (int, float):
        if parent is None:
            print(f"{name} must be a {expected_type.__name__}, not a boolean.")
            return False
        else:
            show_error(f"{name} must be a {expected_type.__name__}, not a boolean.", parent)
            return False
        
    try:
        if expected_type == str:
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string.")
            if value.strip() == "":
                raise ValueError(f"{name} cannot be empty.")
            return True
        if expected_type == bool:
            if isinstance(value, bool):
                return True
            if isinstance(value, str):
                if value.lower() in ("true", "1", "yes"):
                    return True
                if value.lower() in ("false", "0", "no"):
                    return True
            if parent is None:
                print(f"{name} must be either True or False (or 'true'/'false').")
            else: 
                show_error(f"{name} must be either True or False (or 'true'/'false').", parent)
            return False

        if expected_type == int:
            # Prevent accepting float with decimals
            if isinstance(value, float) and not value.is_integer():
                raise ValueError()
            if isinstance(value, str) and '.' in value:
                if float(value).is_integer():
                    return True
                raise ValueError()
            int(value)
            return True


        if isinstance(value, expected_type):
            return True
        
        # Add this after checking isinstance(value, expected_type)
        if expected_type == int and isinstance(value, float):
            if not value.is_integer():  # 1.0 is OK, but 1.5 is not
                raise ValueError(f"{value} is not a whole number.")
            
        # Try to convert
        if expected_type in [float, str]:
            expected_type(value)
            return True

    except (ValueError, TypeError):
        if parent is None:
            print(f"Error: {name} must be a valid {expected_type.__name__}.")
            return False
        else:
            show_error(f"{name} must be a valid {expected_type.__name__}.", parent)
            return False

def validate_float(text, name, min_value=None, max_value=None, parent=None):
    """
    Validates that the input text can be converted to a float and is within the specified range.

    Parameters:
        text (str): The input string to validate.
        name (str): The name of the field (used in error messages).
        min_value (float, optional): Minimum allowed value.
        max_value (float, optional): Maximum allowed value.
        parent (QWidget, optional): Parent widget for QMessageBox if used in a GUI.

    Returns:
        bool: True if valid, False if not.
    """
    try:
        value = float(text)
    except ValueError:
        show_error(f"{name} must be a valid number.", parent)
        return False, None

    if min_value is not None and value < min_value:
        show_error(f"{name} must be at least {min_value}.", parent)
        return False, None
    if max_value is not None and value > max_value:
        show_error(f"{name} must be at most {max_value}.", parent)
        return False, None

    return True, value

def validate_int(text, name, min_value=None, max_value=None, parent=None):
    """
    Validates whether the input text can be converted to an integer
    and optionally checks if it falls within a specified range.

    Parameters:
        text (str): The input text to validate.
        name (str): A descriptive name for the field (used in error messages).
        min_value (int, optional): Minimum allowed value.
        max_value (int, optional): Maximum allowed value.
        parent (QWidget, optional): Parent widget for error messages.

    Returns:
        (bool, int or None): Tuple of success flag and the validated integer (or None if failed).
    """
    try:
        value = int(text)
    except ValueError:
        show_error(f"{name} must be a valid number.", parent)
        return False, None

    if min_value is not None and value < min_value:
        show_error(f"{name} must be at least {min_value}.", parent)
        return False, None
    if max_value is not None and value > max_value:
        show_error(f"{name} must be at most {max_value}.", parent)
        return False, None

    return True, value

def validate_string_choice(text, name, allowed_values, parent=None):
    """
    Validates that the input string is one of the allowed string values.

    Parameters:
        text (str): The input string to validate.
        name (str): The name of the field (used in error messages).
        allowed_values (list or set): Collection of allowed string values (case-sensitive).
        parent (QWidget, optional): Parent widget for QMessageBox if used in a GUI.

    Returns:
        bool: True if valid, False if not.
        str or None: The validated string, or None if invalid.
    """
    if text in allowed_values:
        return True, text
    else:
        allowed_str = ", ".join(map(str, allowed_values))
        show_error(f"Invalid value for {name}. Must be one of: {allowed_str}", parent)
        return False, None

def show_error(message, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Input Error")
    msg.setText(message)
    msg.exec()

