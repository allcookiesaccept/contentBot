from config.models import CSVFile
import os


class CSVWorker:

    project_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, processed_data: CSVFile):
        self.worker = processed_data
        self.rows = len(processed_data.dataframe)
        self.chunk = 100
        self.ready_files_paths = []
        self.__create_content_files_directory()

    def __create_content_files_directory(self):

        self.content_files_directory = os.path.join(CSVWorker.project_folder_path, 'content_files')

        if not os.path.exists(self.content_files_directory):
            os.makedirs(self.content_files_directory)

    def __call__(self):

        if self.worker.type == "with_description" and self.rows > self.chunk:
            self.divide_on_blocks()
        else:
            self.create_file()

        return self.ready_files_paths


    def create_file(self) -> list:
        file_path = os.path.join(self.content_files_directory, self.worker.filename)
        self.worker.dataframe.to_csv(file_path, encoding="utf-8", sep=";", index=False)
        self.ready_files_paths.append(file_path)

    def divide_on_blocks(self) -> list:

        blocks = [
            self.worker.dataframe.iloc[i : i + self.chunk]
            for i in range(0, len(self.worker.dataframe), self.chunk)
        ]

        for i, block in enumerate(blocks):
            filename = f"{i}_{self.worker.filename}"
            file_path = os.path.join(self.content_files_directory, filename)
            block.to_csv(file_path, encoding="utf-8", sep=";", index=False)
            self.ready_files_paths.append(file_path)
