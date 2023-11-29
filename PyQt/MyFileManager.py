import os
from datetime import datetime


class FileManager:
    def __init__(self):
        self.directory_path = ''
        
    # 디렉터리 경로 설정 (GUI에서 폴더 경로를 파일탐색기에서 클릭하여 값을 넘겨주는 형태)
    def setDirPath(self, directory_path):
        self.directory_path = directory_path

    # 파일 정보 출력
    def list_files_in_directory(self):
        file_info_list = []

        file_list = os.listdir(self.directory_path)

        for file_name in file_list:
            file_path = os.path.join(self.directory_path, file_name)
            file_size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            extension = os.path.splitext(file_name)[1]

            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            elif file_size < 1024 * 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{file_size / (1024 * 1024 * 1024):.2f} GB"

            modified_time_str = datetime.fromtimestamp(
                modified_time).strftime("%Y-%m-%d %H:%M:%S")

            file_info_list.append({
                'file_name': file_name,
                'file_path': os.path.dirname(file_path),
                'file_size': size_str,
                'modified_time': modified_time_str,
                'extension': extension
            })

        return file_info_list