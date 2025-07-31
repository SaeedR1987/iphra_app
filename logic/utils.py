from PyQt6.QtWidgets import QMessageBox

def handle_error_message(type, error_message, parent = None):
    """
    Appropriately handle error messaging and raise errors.
    """
    if parent is None:
        print(error_message)
    else:
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Input Error")
        msg.setText(error_message)
        msg.exec()

    if type == ValueError: # When using an invalid value
        raise ValueError(error_message)
    elif type == TypeError: # When using wrong class of data
        raise TypeError(error_message)
    elif type == NameError: # when value used before defined
        raise NameError(error_message)
    elif type == IndexError: # when accessing a list or string index which doesnt exist
        raise IndexError(error_message)
    elif type == KeyError: # when accessing a dictionary with a key that doesnt exist
        raise KeyError(error_message) 
    elif type == AttributeError: # When accessing an attribute or method that doesnt exist
        raise AttributeError(error_message)
    elif type == ImportError: # When importing a module that doesnt exist
        raise ImportError(error_message)
    elif type== ZeroDivisionError: # When dividing by zero.
        raise ZeroDivisionError(error_message)
    
