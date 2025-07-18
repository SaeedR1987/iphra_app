class DataManager:
    """
    A class to manage data operations in the application.
    This class is designed to handle data naming, switching, saving. 
    This class may also handle operations across datasets, such as merging data.

    """
    def __init__(self: Session):
        self.datasets: dict[str, Data] = {} # maps dataset names to Data objects
        self.active_dataset: str | None = None  # Optional active dataset name

    def add_dataset(self, 
                    name: str, 
                    data_obj: Data):
        """
        Add a new dataset to the manager.
        This method should add a new dataset with the specified name and data object.
        """
        self.datasets[name] = data_obj
        if self.active_dataset is None:
            self.active_dataset = name

    def remove_dataset(self, name: str):
        """
        Remove a dataset from the manager.
        This method should remove the dataset with the specified name.
        If the removed dataset is the active dataset, set active_dataset to None.
        """
        if name in self.datasets:
            del self.datasets[name]
            if self.active_dataset == name:
                self.active_dataset = None
        else:
            raise ValueError(f"Dataset '{name}' does not exist.")

    def switch_dataset(self, name: str):
        """
        Switch the active dataset to the specified name.
        This method should change the active dataset to the dataset with the specified name.
        """
        if name in self.datasets:
            self.active_dataset = name
        else:
            raise ValueError(f"Dataset '{name}' does not exist.")
        
    def get_dataset(self, name: str) -> Data:
        """
        Get a dataset by name.
        This method should return the dataset object with the specified name.
        If the dataset does not exist, raise an exception.
        """
        if name in self.datasets:
            return self.datasets[name]
        else:
            raise ValueError(f"Dataset '{name}' does not exist.")

    def get_active_dataset(self) -> Data:
        """
        Get the active dataset.
        This method should return the active dataset object.
        If no active dataset is set, raise an exception.
        """
        if self.active_dataset is not None:
            return self.datasets[self.active_dataset]
        else:
            raise ValueError("No active dataset is set.")
        
    def list_dataset_names(self) -> list[str]:
        """
        List the names of all datasets.
        This method should return a list of all dataset names managed by the DataManager.
        """
        return list(self.datasets.keys())
    
    def summary(self) -> str:
        """
        Generate a summary of the datasets.
        This method should return a string summarizing the datasets managed by the DataManager.
        """
        return {
        name: {
            "rows_raw": data.raw_df.shape[0],
            "rows_clean": data.clean_df.shape[0],
            "has_logs": bool(data.cleaning_log or data.deletion_log)
        }
        for name, data in self.datasets.items()
    }

    def to_dict(self) -> dict:
        return {
            "active": self.active_dataset_name,
            "datasets": {
                name: data.to_dict()
                for name, data in self.datasets.items()
            }
        }

    @staticmethod
    def from_dict(data: dict) -> "DataManager":
        manager = DataManager()
        manager.active_dataset_name = data.get("active")
        datasets_dict = data.get("datasets", {})
        for name, data_dict in datasets_dict.items():
            manager.datasets[name] = Data.from_dict(data_dict)
        return manager
    
    def validate_all_datasets(self):
        """
        Validate all datasets in the manager.
        This method should check each dataset for completeness, format, and accuracy.
        """
        for name, data in self.datasets.items():
            if not data.is_valid():
                raise ValueError(f"Dataset '{name}' is not valid.")
            
    def clear_all_datasets(self):
        """
        Clear all datasets in the manager.
        This method should remove all datasets from the manager.
        """
        self.datasets.clear()
        self.active_dataset = None
