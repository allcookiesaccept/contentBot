import pandas
from dataclasses import dataclass
from pathlib import Path

project_folder_path = Path("../contentBot")
content_folder_path = project_folder_path / "content_files"



@dataclass()
class CSVFile:
    filename: str
    dataframe: pandas.DataFrame
    type: str


class CSVWorker:
    def __init__(self, filename: str, dataframe: pandas.DataFrame, type: str):
        self.worker = CSVFile(filename, dataframe, type)
        self.rows = len(dataframe)
        self.chunk = 30
        self.filepath = content_folder_path
        self.ready_files_paths = []

    def __call__(self):

        if self.rows > self.chunk and self.worker.type == "description":
            files = self.divide_on_blocks()
            return files
        else:
            file = self.create_file()
            return file


    def create_file(self):
        full_path = f"{self.filepath}/{self.worker.filename}"
        self.worker.dataframe.to_csv(full_path, encoding="utf-8", sep=";", index=False)
        self.ready_files_paths.append(full_path)
        return self.ready_files_paths

    def divide_on_blocks(self):
        blocks = [
            self.worker.dataframe.iloc[i : i + self.chunk]
            for i in range(0, len(self.worker.dataframe), self.chunk)
        ]
        for i, block in enumerate(blocks):
            filename = f"{i}_{self.worker.filename}"
            block.to_csv(filename, encoding="utf-8", sep=";", index=False)
            self.ready_files_paths.append(filename)
        return self.ready_files_paths