class Tool:
    """
    A class to represent a tool in the application.
    This class is designed to manage the tools used in the application,
    including the creation of tools, updating them, and managing tool data.
    """
    def __init__(self, xlsform : pd.Dataframe):
        self.version = Session.SUPPORTED_VERSION
        self.xlsform = {}

    def add_module(self, 
                   indicator: list, 
                   data: pd.Dataframe):
        """
        Add a module to the tool.
        This method should create a new module with the specified name, description, and data.
        """
        pass
    
    def remove_module(self,
                      indicator: list, 
                      data: pd.Dataframe):
        """
        Remove a module from the tool.
        This method should delete the module with the specified name from the tool.
        """
        pass

    def to_dict(self):
        """
        Convert the tool data to a dictionary format.
        This method should return the tool data in a format suitable for serialization or storage.
        """
        return {
            "version": self.version,
            "data": self.data
        }
    
    @staticmethod
    def from_dict(data):
        """
        Load the tool data from a dictionary format.
        This method should populate the tool attributes from the provided dictionary.
        """
        tool = Tool()
        tool.version = data.get("version", Session.SUPPORTED_VERSION)
        tool.data = data.get("data", {})
        return tool    