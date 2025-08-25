import os

class Settings:
    def __init__(self) -> None:
        self.DATASET_PATH = os.environ.get("DATASET_PATH", "Framingham.csv")
        self.EXPORT_DPI = int(os.environ.get("EXPORT_DPI", "144"))
