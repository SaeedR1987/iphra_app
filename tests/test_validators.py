import importlib
importlib.reload(logic.validators)
import logic.validators 

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
    """
    result = logic.validators.validate_type(1.5, expected_type=str, name="DEFF of 1.5", parent=None)
    expected = False
    assert result == expected # Expect False

def test_validate_type_case_float_with_int():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 cannot be safely converted to an int due to loss of data.  
    """
    result = logic.validators.validate_type(1.5, expected_type=int, name="DEFF of 1.5", parent=None)
    expected = False
    assert result == expected # Expect False

def test_validate_type_case_float_with_bool():
    """
    Test if the method validate_type functions correctly with float inputs.
    Value of 1.5 is not explicitly a boolean value.  
    """
    result = logic.validators.validate_type(1.5, expected_type=bool, name="DEFF of 1.5", parent=None)
    expected = False
    assert result == expected # Expect False

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
    result = logic.validators.validate_type("Hi", expected_type=float, name="The word Hi", parent=None)
    expected = False
    assert result == expected 

def test_validate_type_case_str_with_int():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi cannot be safely converted to an int.  
    """
    result = logic.validators.validate_type("Hi", expected_type=int, name="The word Hi", parent=None)
    expected = False
    assert result == expected 

def test_validate_type_case_str_with_bool():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of Hi cannot be safely converted to an bool.  
    """
    result = logic.validators.validate_type("Hi", expected_type=bool, name="The word Hi", parent=None)
    expected = False
    assert result == expected 

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
    result = logic.validators.validate_type(True, expected_type=str, name="The bool True", parent=None)
    expected = True
    assert result == expected 

def test_validate_type_case_bool_with_float():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True cannot be explicitly converted to a float.  
    """
    result = logic.validators.validate_type(True, expected_type=float, name="The bool True", parent=None)
    expected = False
    assert result == expected 

def test_validate_type_case_bool_with_int():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of True cannot be safely converted to an int.  
    """
    result = logic.validators.validate_type(True, expected_type=int, name="The bool True", parent=None)
    expected = True
    assert result == expected

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
    Value of 5 can be safely converted to a float.  
    """
    result = logic.validators.validate_type(5, expected_type=str, name="Number 5", parent=None)
    expected = True
    assert result == expected

def test_validate_type_case_int_with_bool():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 5 can be safely converted to a float.  
    """
    result = logic.validators.validate_type(5, expected_type=bool, name="Number 5", parent=None)
    expected = True
    assert result == expected

# CHECK OTHER VALID BOOL VALUES

def test_validate_type_case_bool_alt1():
    """
    Test if the method validate_type functions correctly with string inputs.
    Value of 1 is strictly not convertible to a bool.  
    """
    result = logic.validators.validate_type(1, expected_type=bool, name="1", parent=None)
    expected = True
    assert result == expected

# CHECK NUMERIC STRING CONVERSIONS