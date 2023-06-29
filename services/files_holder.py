import os
from pathlib import Path

def create_content_folder(root_path):

    path = f'{root_path}/content_files'
    if not os.path.exists(path):
        os.mkdir(path)
#
# def save_csv_with_processed(filename, filepath, csv_data):
#     with open(f'{filepath}/{filename}', 'w', encoding=) as file