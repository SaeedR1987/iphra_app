import importlib
#importlib.reload(logic.validators)
import logic.validators 
import pandas as pd
import os
import pytest
from PyQt6.QtCore import QTime
from datetime import datetime, time

# CHECK VALIDATE TYPE

def test_validate_type_case_float_with_float():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 is a float.  
    """
    result = logic.validators.validate_type(1.5, expected_type=float, name="DEFF of 1.5", parent=None)
    expected = True
    assert result == expected # Expect True

def test_validate_type_case_float_with_str():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 will not be silently converted to str.
    Expect to raise a TypeError.  
    """
    with pytest.raises(TypeError, match = "DEFF of 1.5 must be a string."):
        logic.validators.validate_type(1.5, expected_type=str, name="DEFF of 1.5", parent=None)

def test_validate_type_case_float_with_int():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 cannot be safely converted to an int due to loss of data. 
    Expect to raise a TypeError.  
    """
    with pytest.raises(ValueError, match = "1.5 is not a whole number."):
        logic.validators.validate_type(1.5, expected_type=int, name="DEFF of 1.5", parent=None)
    
def test_validate_type_case_float_with_bool():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 is not explicitly a boolean value.  
    """
    with pytest.raises(TypeError, match = "DEFF of 1.5 must be a boolean."):
        logic.validators.validate_type(1.5, expected_type=bool, name="DEFF of 1.5", parent=None)
    
def test_validate_type_case_str_with_str():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi is a str.  
    """
    result = logic.validators.validate_type("Hi", expected_type=str, name="The word Hi", parent=None)
    expected = True
    assert result == expected 

def test_validate_type_case_str_with_float():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi cannot be safely converted to an float.  
    """
    with pytest.raises(TypeError, match = "The word Hi cannot be converted to float."):
        logic.validators.validate_type("Hi", expected_type=float, name="The word Hi", parent=None)
    
def test_validate_type_case_str_with_int():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi cannot be safely converted to an int.  
    """
    with pytest.raises(TypeError, match = "The word Hi cannot be converted to int."):
        logic.validators.validate_type("Hi", expected_type=int, name="The word Hi", parent=None)

def test_validate_type_case_str_with_bool():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi cannot be safely converted to an bool.  
    """
    with pytest.raises(TypeError, match = "The word Hi must be either True or False."):
        logic.validators.validate_type("Hi", expected_type=bool, name="The word Hi", parent=None)
    
def test_validate_type_case_bool_with_bool():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True is a boolean.  
    """
    result = logic.validators.validate_type(True, expected_type=bool, name="The bool True", parent=None)
    expected = True
    assert result == expected 

def test_validate_type_case_bool_with_str():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True cannot be explicitly converted to a str.  
    """
    with pytest.raises(TypeError, match = "The bool True must be a string."):
        logic.validators.validate_type(True, expected_type=str, name="The bool True", parent=None)
    
def test_validate_type_case_bool_with_float():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True cannot be explicitly converted to a float.
    Expects to raise a TypeError.   
    """
    with pytest.raises(TypeError, match = "The bool True must be a float, not a boolean."):
        logic.validators.validate_type(True, expected_type=float, name="The bool True", parent=None)
        
def test_validate_type_case_bool_with_int():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True cannot be safely converted to an int.
    Expects to raise a TypeError.  
    """
    with pytest.raises(TypeError, match = "The bool True must be a int."):
        logic.validators.validate_type(True, expected_type=int, name="The bool True", parent=None)

def test_validate_type_case_int_with_int():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 5 is an int.  
    """
    result = logic.validators.validate_type(5, expected_type=int, name="Number 5", parent=None)
    expected = True
    assert result == expected

def test_validate_type_case_int_with_float():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 5 can be safely converted to a float.  
    """
    result = logic.validators.validate_type(5, expected_type=float, name="Number 5", parent=None)
    expected = True
    assert result == expected

def test_validate_type_case_int_with_str():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 5 cannot be safely converted to a str.  
    """
    with pytest.raises(TypeError, match = "Number 5 must be a string."):
        logic.validators.validate_type(5, expected_type=str, name="Number 5", parent=None)

def test_validate_type_case_int_with_bool():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 5 cannot be safely converted to a boolean.  
    """
    with pytest.raises(TypeError, match = "Number 5 must be a boolean."):
        logic.validators.validate_type(5, expected_type=bool, name="Number 5", parent=None)

# CHECK VALIDATE TYPE OTHER VALID BOOL VALUES

def test_validate_type_case_bool_alt1():
    """
    Test if the method validate_type functions correctly with expected type boolean.
    Value of 1 is strictly not convertible to a bool in this function.  
    """
    with pytest.raises(TypeError, match = "1 must be a boolean"):
        logic.validators.validate_type(1, expected_type=bool, name="1", parent=None)

def test_validate_type_case_bool_alt2():
    """
    Test if the method validate_type functions correctly with expected type boolean.
    Value of 0 is strictly not convertible to a bool in this function.  
    """
    with pytest.raises(TypeError, match = "0 must be a boolean"):
        logic.validators.validate_type(0, expected_type=bool, name="0", parent=None)

def test_validate_type_case_bool_alt3():
    """
    Test if the method validate_type functions correctly with expected type boolean.
    Value of yes is strictly not convertible to a bool in this function.  
    """
    with pytest.raises(TypeError, match = "yes must be either True or False."):
        logic.validators.validate_type("yes", expected_type=bool, name="yes", parent=None)
    
def test_validate_type_case_bool_alt4():
    """
    Test if the method validate_type functions correctly with expected type boolean.
    Value of no is strictly not convertible to a bool in this function.  
    """
    with pytest.raises(TypeError, match = "no must be either True or False."):
        logic.validators.validate_type("no", expected_type=bool, name="no", parent=None)

# CHECK VALIDATE TYPE NUMERIC STRING CONVERSIONS

def test_validate_type_case_num_str1():
    """
    Test if the method validate_type functions correctly with numeric inputs as str.
    Value of 1.5 as a str is convertible to a float.  
    """
    result = logic.validators.validate_type("1.5", expected_type=float, name="1.5", parent=None)
    expected = True
    assert result == expected

def test_validate_type_case_num_str2():
    """
    Test if the method validate_type functions correctly with numeric inputs as str.
    Value of 1 as a str is convertible to an int.  
    """
    result = logic.validators.validate_type("1", expected_type=int, name="1", parent=None)
    expected = True
    assert result == expected

def test_validate_type_case_num_str3():
    """
    Test if the method validate_type functions correctly with numeric inputs as str.
    Value of 1.5 as a str is not safely convertible to an int.  
    """
    with pytest.raises(TypeError, match = "Deff of 1.5 cannot be converted to int."):
        logic.validators.validate_type("1.5", expected_type=int, name="Deff of 1.5", parent=None)

def test_validate_type_case_num_str4():
    """
    Test if the method validate_type functions correctly with numeric inputs as str.
    Value of 1 as a str is safely convertible to a float.  
    """
    result = logic.validators.validate_type("1", expected_type=float, name="1", parent=None)
    expected = True
    assert result == expected

# CHECK VALIDATE DATAFRAME

def test_validate_dataframe_csv_valid():
    # Load a valid test file
    file_path = os.path.join(os.path.dirname(__file__), "assets", "csv_valid_test.csv")
    df = pd.read_csv(file_path)
    result = logic.validators.validate_dataframe(df, required_columns=["id", "name", "age"])
    assert result is True

def test_validate_dataframe_xlsx_valid():
    # Load a valid test file
    file_path = os.path.join(os.path.dirname(__file__), "assets", "xlsx_valid_test.xlsx")
    df = pd.read_excel(file_path)
    result = logic.validators.validate_dataframe(df, required_columns=["id", "name", "age"])
    assert result is True

def test_validate_dataframe_csv_missing_column():
    # Load a test file missing required columns
    file_path = os.path.join(os.path.dirname(__file__), "assets", "csv_valid_test.csv")
    df = pd.read_csv(file_path)

    result = logic.validators.validate_dataframe(df, required_columns=["id", "name", "missing_column"])
    assert result is False

def test_validate_dataframe_xlsx_missing_column():
    # Load a test file missing required columns
    file_path = os.path.join(os.path.dirname(__file__), "assets", "xlsx_valid_test.xlsx")
    df = pd.read_excel(file_path)

    result = logic.validators.validate_dataframe(df, required_columns=["id", "name", "missing_column"])
    assert result is False

# CHECK VALIDATE FLOAT

def test_validate_float_case_valid():
    """
    Test if the method validate_float functions correctly float input.
    Value of 15.5 is between minimum of 10 and maximum of 20.  
    """
    result, value = logic.validators.validate_float(15.5, min_value= 10, max_value=20, name = "15.5", parent=None)
    expected = True
    assert result == expected, value == 15.5

def test_validate_float_case_invalid_max():
    """
    Test if the method validate_float functions correctly float input.
    Value of 15.5 is above acceptable range of minimum of 10 and maximum of 15.  
    """
    result, value = logic.validators.validate_float(15.5, min_value= 10, max_value=15, name = "15.5", parent=None)
    expected = False
    assert result == expected, value == 15.5

def test_validate_float_case_invalid_min():
    """
    Test if the method validate_float functions correctly float input.
    Value of 15.5 is below acceptable range of minimum of 20 and maximum of 25.  
    """
    result, value = logic.validators.validate_float(15.5, min_value= 20, max_value=25, name = "15.5", parent=None)
    expected = False
    assert result == expected, value == 15.5

def test_validate_float_case_invalid_str():
    """
    Test if the method validate_float functions correctly float input.
    Value of Hi is not an acceptable input.  
    """
    result, value = logic.validators.validate_float("Hi", min_value= 20, max_value=25, name = "Hi", parent=None)
    expected = False
    assert result == expected, value == 15.5

# CHECK VALIDATE INT

def test_validate_int_case_valid():
    """
    Test if the method validate_int functions correctly int input.
    Value of 15 is between minimum of 10 and maximum of 20.  
    """
    result, value = logic.validators.validate_int(15, min_value= 10, max_value=20, name = "15", parent=None)
    expected = True
    assert result == expected, value == 15

def test_validate_int_case_invalid_max():
    """
    Test if the method validate_float functions correctly int input.
    Value of 15 is above acceptable range of minimum of 10 and maximum of 14.  
    """
    result, value = logic.validators.validate_int(15.5, min_value= 10, max_value=14, name = "15", parent=None)
    expected = False
    assert result == expected, value == 15

def test_validate_int_case_invalid_min():
    """
    Test if the method validate_int functions correctly int input.
    Value of 15 is below acceptable range of minimum of 20 and maximum of 25.  
    """
    result, value = logic.validators.validate_int(15, min_value= 20, max_value=25, name = "15", parent=None)
    expected = False
    assert result == expected, value == 15

def test_validate_int_case_invalid_str():

    """
    Test if the method validate_int functions correctly int input.
    Value of Hi is not an acceptable input.  
    """
    result, value = logic.validators.validate_int("Hi", min_value= 20, max_value=25, name = "Hi", parent=None)
    expected = False
    assert result == expected, value == 15

# CHECK VALIDATE STRING CHOICES

def test_validate_str_choice_case_valid():
    """
    Test if the method validate_str_choice functions correctly with valid input.
    Value of Hi is an acceptable input for allowed values Hi, Hello, and Howdy.  
    """
    result, value = logic.validators.validate_string_choice("Hi", allowed_values = ["Hi", "Hello", "Howdy"] , name = "Hi", parent=None)
    expected = True
    assert result == expected, value == "Hi"

def test_validate_str_choice_case_invalid():
    """
    Test if the method validate_str_choice functions correctly with valid input.
    Value of Hey is not an acceptable input for allowed values Hi, Hello, and Howdy  
    """
    result, value = logic.validators.validate_string_choice("Hey", allowed_values = ["Hi", "Hello", "Howdy"] , name = "Hey", parent=None)
    expected = False
    assert result == expected, value == "Hey"

# CHECK VALIDATE TIME 

def test_validate_time_case_valid_qtime():
    """
    Test if the method validate_time functions correctly with valid input.
    Value of QTime(14, 30) should return True and parsed value.
    """
    result, value = logic.validators.validate_time(value = QTime(14, 30), name = "Time Test")
    expected = True
    assert result == expected, value == datetime.time(14,30)

def test_validate_time_case_valid_str():
    """
    Test if the method validate_time functions correctly with valid input.
    Value of "14:30" should return True and parsed value.
    """
    result, value = logic.validators.validate_time(value = "14:30", name = "Time Test")
    expected = True
    assert result == expected, value == datetime.time(14,30)

def test_validate_time_case_invalid_qtime():
    """
    Test if the method validate_time functions correctly with valid input.
    Value of QTime(25, 30) should throw a ValueError.
    """
    with pytest.raises(ValueError, match = "Time Test is not a valid time input."):
        logic.validators.validate_time(value = QTime(25, 30), name = "Time Test")

def test_validate_time_case_invalid_str():
    """
    Test if the method validate_time functions correctly with valid input.
    Value of "25:30" should throw a ValueError.
    """
    with pytest.raises(ValueError, match = "Time Test is not a valid time input."):
        logic.validators.validate_time(value = "25:30", name = "Time Test")

def test_validate_time_case_invalid_float():
    """
    Test if the method validate_time functions correctly with valid input.
    A float value should throw a TypeError.
    """
    with pytest.raises(TypeError, match = "Invalid type for type input. Time Test must be a QTime or str value."):
        logic.validators.validate_time(value = 25.526, name = "Time Test")

def test_validate_time_case_invalid_int():
    """
    Test if the method validate_time functions correctly with valid input.
    An int value should throw a TypeError.
    """
    with pytest.raises(TypeError, match = "Invalid type for type input. Time Test must be a QTime or str value."):
        logic.validators.validate_time(value = 14, name = "Time Test")