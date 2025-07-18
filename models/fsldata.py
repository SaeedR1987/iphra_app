class FSLData(Data):
    
    def __init__(self):
        return super().__init_subclass__()  

    def fsl_checks_cleaning_log(self, data, log):
        """
        Perform checks on the raw data for household food consumption data.
        This method should check for common issues in MUAC data such as outliers, missing values, and inconsistencies.
        """
        pass
