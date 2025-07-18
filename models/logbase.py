class LogBase:
    def __init__(self, df: pd.DataFrame = None):
        self.df = df.copy() if df is not None else pd.DataFrame()

    def to_dict(self) -> List[Dict]:
        return self.df.to_dict(orient="records")

    def from_dict(self, data: List[Dict]) -> None:
        self.df = pd.DataFrame(data)

    def replace_df(self, df: pd.DataFrame):
        self.df = df.copy()

    def validate(self) -> bool:
        return True  # override in subclasses if needed