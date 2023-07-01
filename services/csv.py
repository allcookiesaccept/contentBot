import pandas
from dataclasses import dataclass


@dataclass()
class CSVFile:
    filename: str
    dataframe: pandas.DataFrame


class CSVWorker:

    def __init__(self, filename: str, dataframe: pandas.DataFrame):

        self.worker = CSVFile(filename, dataframe)
        self.rows = len(dataframe)



    def create_file(self, path: str = '') -> str:

        full_path = f'{path}{self.worker.filename}'
        self.worker.dataframe.to_csv(full_path, encoding="utf-8", sep=";", index=False)
        return full_path

    def divide_on_blocks(self, chunk: int = 10):

        blocks = [self.worker.dataframe.iloc[i:i + chunk] for i in range(0, len(self.worker.dataframe), chunk)]
        for i, block in enumerate(blocks):
            filename = f'{self.worker.filename}_{i}.csv'
            block.to_csv(filename, encoding="utf-8", sep=";", index=False
    )



