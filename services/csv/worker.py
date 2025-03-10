from config.models import CSVFile
from pathlib import Path
import os

project_folder_path = Path(__file__).parent.parent

class CSVWorker:
    def __init__(self, processed_data: CSVFile):
        self.worker = processed_data
        self.rows = len(processed_data.dataframe)
        self.chunk = 100
        self.ready_files_paths = []
        self.content_files_directory = project_folder_path / "content_files"

        self.__check_content_files_directory()

    def __check_content_files_directory(self) -> None:
        if not os.path.exists(self.content_files_directory):
            os.makedirs(self.content_files_directory)

        return

    def __call__(self) -> list:
        if self.worker.type == "with_description" and self.rows > self.chunk:
            self.__divide_on_blocks()
        else:
            self.__create_file()
        return self.ready_files_paths

    def __create_file(self):
        file_path = self.content_files_directory / self.worker.filename
        self.worker.dataframe.to_csv(file_path, encoding="utf-8", sep=";", index=False)
        self.ready_files_paths.append(str(file_path))
        

    def __divide_on_blocks(self) -> None:
        blocks = [
            self.worker.dataframe.iloc[i : i + self.chunk]
            for i in range(0, len(self.worker.dataframe), self.chunk)
        ]

        for i, block in enumerate(blocks):
            filename = f"{i}_{self.worker.filename}"
            file_path = os.path.join(self.content_files_directory, filename)
            block.to_csv(file_path, encoding="utf-8", sep=";", index=False)
            self.ready_files_paths.append(file_path)
        return
