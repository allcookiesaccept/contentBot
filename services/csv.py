import pandas
from dataclasses import dataclass


@dataclass()
class CSVFile:
    filename: str
    dataframe: pandas.DataFrame
    type: str


class CSVWorker:
    def __init__(self, filename: str, dataframe: pandas.DataFrame, type: str):
        self.worker = CSVFile(filename, dataframe, type)
        self.rows = len(dataframe)
        self.chunk = 20
        self.filepath = 'content_files/'
        self.ready_files_paths = []

    def __call__(self):

        if self.worker.type == 'photo':
            self.create_file()
            return self.ready_files_paths

        if self.rows > self.chunk:
            self.divide_on_blocks()
        else:
            self.create_file()

        return self.ready_files_paths

    def create_file(self):

        full_path = f"{self.filepath}{self.worker.filename}"
        self.worker.dataframe.to_csv(full_path, encoding="utf-8", sep=";", index=False)
        self.ready_files_paths.append(full_path)



    def divide_on_blocks(self):


        blocks = [
            self.worker.dataframe.iloc[i : i + self.chunk]
            for i in range(0, len(self.worker.dataframe), self.chunk)
        ]

        for i, block in enumerate(blocks):
            filename = f"{self.filepath}{self.worker.filename}_{i}.csv"
            self.ready_files_paths.append(filename)
            block.to_csv(filename, encoding="utf-8", sep=";", index=False)


