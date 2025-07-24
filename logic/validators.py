
# logic/validators.py

import pandas as pd
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime, time
from typing import Union, Tuple, Optional
from PyQt6.QtCore import QTime

def show_error(message, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Input Error")
    msg.setText(message)
    msg.exec()

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

    # Lists, tuples, and dicts are not valid inputs for this method.
    if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, dict):
        error_message = f"{name} must be a single value and cannot be a list, tuple, or dict."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise TypeError(error_message)

    # Check possible combinations for expected type str and handle accordingly.
    if expected_type == str:

        # If string and is empty, raise ValueError
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                error_message = f"{name} cannot be empty."
                if parent is None:
                    print(error_message)
                else:
                    show_error(error_message, parent)
                raise ValueError(error_message)
            return True
        
        # If not a string and string is expected, raise TypeError
        if not isinstance(value, str):
            error_message = f"{name} must be a string."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message)
            raise TypeError(error_message)

    elif expected_type == bool:
                
        if isinstance(value, str):
            # If str that is not safely convertible to bool, raise ValueError.
                error_message = f"{name} must be either True or False."
                if value.lower() not in ("true","True","false", "False"):
                    if parent is None:
                        print(error_message)
                    else:
                        show_error(error_message, parent)
                    raise TypeError(error_message)
                return True
        elif (isinstance(value, (int, float)) and not isinstance(value, bool)):
            # Prohibit all other cases from being considered a boolean
            error_message = f"{name} must be a boolean."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message, parent)
            raise TypeError(error_message)
        elif isinstance(value, bool):
            return True
        else:
            # Prohibit all other cases from being considered a boolean
            error_message = f"{name} must be a boolean."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message, parent)
            raise TypeError(error_message)
                    
    elif expected_type == float:
        
        # If boolean and expected type is int or float, raise TypeError
        if isinstance(value, bool):
            error_message = f"{name} must be a {expected_type.__name__}, not a boolean."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message, parent)
            raise TypeError(error_message)
        elif isinstance(value, str):
            try:
                expected_type(value)
                return True
            except:
                error_message = f"{name} cannot be converted to float."
                if parent is None:
                    print(error_message)
                else:
                    show_error(error_message, parent)
                raise TypeError(error_message)
        elif (isinstance(value, (int, float)) and not isinstance(value, bool)):
            return True
        else:
            # Prohibit all other cases from being considered a boolean
            error_message = f"{name} must be a float."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message, parent)
            raise TypeError(error_message)

    elif expected_type == int:

        if isinstance(value, float) and not isinstance(value, bool): 
        # If float not safely convertible to an integer, return ValueError
            if not value.is_integer():
                error_message = f"{value} is not a whole number."
                if parent is None:
                    print(error_message)
                else:
                    show_error(error_message, parent)
                raise ValueError(error_message)
            else:
                return True
        elif isinstance(value, str):
            try:
                expected_type(value)
                return True
            except:
                error_message = f"{name} cannot be converted to int."
                if parent is None:
                    print(error_message)
                else:
                    show_error(error_message, parent)
                raise TypeError(error_message)
        elif isinstance(value, int) and not isinstance(value, bool):
            return True
        else:
                error_message = f"{name} must be a {expected_type.__name__}."
                if parent is None:
                    print(error_message)
                else:
                    show_error(error_message, parent)
                raise TypeError(error_message)
    else:
        
    # if value is of expected type, return True
        if isinstance(value, expected_type):
            return True
        else:
            error_message = f"{name} must be a valid {expected_type.__name__}."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message, parent)
            raise TypeError(error_message)
    
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
        if parent is None:
            print(f"{name} must be a valid number.")
            return False, None
        else:
            show_error(f"{name} must be a valid number.", parent)
            return False, None

    if min_value is not None and value < min_value:
        error_message = f"{name} must be at least {min_value}."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise ValueError(error_message)
    if max_value is not None and value > max_value:
        error_message = f"{name} must be at most {max_value}."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise ValueError(error_message)

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
        if parent is None:
            print(f"{name} must be a valid number.")
            return False, None
        else:
            show_error(f"{name} must be a valid number.", parent)
            return False, None
        
        

    if min_value is not None and value < min_value:
        error_message = f"{name} must be at least {min_value}."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise ValueError(error_message)

    if max_value is not None and value > max_value:
        error_message = f"{name} must be at most {max_value}."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise ValueError(error_message)
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
        error_message = f"Invalid value for {name}. Must be one of: {allowed_str}"
        if parent is None:
            print(error_message)
        else:
            show_error(error_message, parent)
        raise ValueError(error_message)

def validate_dataframe(df: pd.DataFrame, required_columns=None, name="Uploaded File", parent = None) -> bool:
    """
    Validates the structure and content of a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The dataframe to validate.
        required_columns (list of str): Columns that must be present.
        name (str): Name used in error messages.
        parent: Optional parent widget for QMessageBox display.
    
    Returns:
        bool: True if valid, False if not.
    """

    if not isinstance(df, pd.DataFrame):
        if parent is None:
            print(f"{name} is not a valid DataFrame.")
            return False
        else:
            show_error(f"{name} is not a valid DataFrame.", parent)
            return False
    
    if df.empty:
        if parent is None:
            print(f"{name} is empty. Please provide a valid file.")
            return False
        else:
            show_error(f"{name} is empty. Please provide a valid file.", parent)
            return False
    
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            if parent is None:
                print(f"{name} is missing required columns: {', '.join(missing)}")
                return False
            else:
                show_error(f"{name} is missing required columns: {', '.join(missing)}", parent)
                return False
    
    return True

def validate_time(value, name = "Time", parent = None) -> tuple[bool, time | None]:
    """
    Validates whether the given value can be interpreted as a valid time.
    
    Parameters:
        value (str or QTime): The input time, either as a string ("HH:MM"), QTime object, or datetime.time object.
        name (str): Name used in error messages.
        parent: Optional parent widget for QMessageBox display.
        
    Returns:
        tuple: (True, datetime.time) if valid; Otherwise raises Value or Type Errors.
    """
    # Handle QTime input
    if isinstance(value, QTime):
        if value.isValid():
            return True, time(value.hour(), value.minute())
        else:
            error_message = f"{name} is not a valid time input."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message)
            raise ValueError(error_message)
        
    elif isinstance(value, time):
        # Normalize to hour and minute only (discard seconds/microseconds)
        return True, time(value.hour, value.minute)

    # Handle string input
    elif isinstance(value, str):
        try:
            parsed = datetime.strptime(value.strip(), "%H:%M").time()
            return True, parsed
        except:
            error_message = f"{name} is not a valid time input."
            if parent is None:
                print(error_message)
            else:
                show_error(error_message)
            raise ValueError(error_message)
    else:
        error_message = f"Invalid type for type input. {name} must be a QTime or str value."
        if parent is None:
            print(error_message)
        else:
            show_error(error_message)
        raise TypeError(error_message)

    


