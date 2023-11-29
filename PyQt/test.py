import os
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QDialog, QLabel, QGridLayout

class FileDetailsDialog(QDialog):
    def __init__(self, file_info):
        super().__init__()

        self.setWindowTitle("파일 상세 정보")
        self.setGeometry(200, 200, 400, 300)

        layout = QGridLayout(self)
        labels = ["이름", "경로", "보이는 확장자", "실제 확장자", "숨겨진 확장자", "파일 크기"]

        for row, label in enumerate(labels):
            layout.addWidget(QLabel(label), row, 0)
            layout.addWidget(QLabel(str(file_info[label])), row, 1)


class FileExplorer(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("파일 탐색기")
        self.setGeometry(100, 100, 800, 600)

        # 파일 정보를 표시할 QTableWidget 생성
        self.file_table = QTableWidget(self)
        self.file_table.setColumnCount(4)
        self.file_table.setHorizontalHeaderLabels(["이름", "경로", "확장자", "파일 크기"])

        # 숨겨진 확장자 검사 버튼 생성 및 클릭 이벤트 연결
        self.check_hidden_ext_button = QPushButton("숨겨진 확장자 검사", self)
        self.check_hidden_ext_button.clicked.connect(
            self.check_hidden_extensions)

        # VirusTotal API 키 설정
        # 여기에 본인의 VirusTotal API 키를 넣어주세요
        self.virustotal_api_key = 'fbe03f99673d63e0f6c0a7bb0ef91a17dd7d634c39309dca174001ed1ed9b49c'

        # 바이러스 검사 버튼 생성 및 클릭 이벤트 연결
        self.virus_scan_button = QPushButton("바이러스 검사", self)
        self.virus_scan_button.clicked.connect(self.scan_for_viruses)

        # 디렉토리 설정으로 이동 버튼 생성 및 클릭 이벤트 연결
        self.change_directory_button = QPushButton("디렉토리 설정으로 이동", self)
        self.change_directory_button.clicked.connect(self.change_directory)

        # 레이아웃 생성 및 위젯 추가
        layout = QVBoxLayout(self)
        layout.addWidget(self.file_table)
        layout.addWidget(self.check_hidden_ext_button)
        layout.addWidget(self.virus_scan_button)
        layout.addWidget(self.change_directory_button)

        # 초기 파일 목록 로딩
        self.list_files()

    def list_files(self):
        # 사용자에게 디렉토리 선택 대화상자 표시
        directory = QFileDialog.getExistingDirectory(
            self, "디렉토리 선택", os.getcwd())
        if directory:
            # 파일 목록 초기화
            self.file_table.setRowCount(0)

            # 선택한 디렉토리의 파일 목록 탐색
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    # 파일 정보 얻기
                    file_info = self.get_file_info(file_path)
                    # 테이블에 행 추가
                    self.add_row(file_info)

    def get_file_info(self, file_path):
        # 파일 정보를 얻기 위한 함수
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        visible_extension = os.path.splitext(file_name)[1]
        file_size = os.path.getsize(file_path)

        return {
            "이름": file_name,
            "경로": file_dir,
            "확장자": visible_extension,
            "파일 크기": file_size
        }

    def add_row(self, file_info):
        # 테이블에 행 추가
        row_position = self.file_table.rowCount()
        self.file_table.insertRow(row_position)

        # 파일 정보를 테이블에 삽입
        for col, value in enumerate(file_info.values()):
            item = QTableWidgetItem(str(value))
            self.file_table.setItem(row_position, col, item)

    def get_file_info_detail(self, file_path):
        # 파일 정보를 얻기 위한 함수
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        visible_extension = os.path.splitext(file_name)[1]

        try:
            actual_extension = os.path.splitext(file_name)[1].split('.')[1]
        except IndexError:
            actual_extension = "없음"

        hidden_extension = os.path.splitext(file_name)[
            0][::-1].split('.', 1)[1][::-1] if '.' in os.path.splitext(file_name)[0][::-1] else "없음"

        file_size = os.path.getsize(file_path)

        return {
            "이름": file_name,
            "경로": file_dir,
            "보이는 확장자": visible_extension,
            "실제 확장자": actual_extension,
            "숨겨진 확장자": hidden_extension,
            "파일 크기": file_size
        }

    def show_file_details_dialog(self, file_path):
        # 파일 정보를 얻어오는 함수 호출
        file_info_detail = self.get_file_info_detail(file_path)

        # 새로운 창 생성 및 열기
        dialog = FileDetailsDialog(file_info_detail)
        dialog.exec()

    # check_hidden_extensions 메서드 내용 수정
    def check_hidden_extensions(self):
        selected_row = self.file_table.currentRow()
        if selected_row != -1:
            file_path = os.path.join(self.file_table.item(
                selected_row, 1).text(), self.file_table.item(selected_row, 0).text())

            # 다이얼로그를 열 때 호출되는 함수 호출
            self.show_file_details_dialog(file_path)

    def scan_for_viruses(self):
        selected_row = self.file_table.currentRow()
        if selected_row != -1:
            file_name = self.file_table.item(selected_row, 0).text()
            file_path = os.path.join(self.file_table.item(
                selected_row, 1).text(), file_name)

            self.check_file_security_with_virustotal(file_path)

    def check_file_security_with_virustotal(self, file_path):
        if not os.path.exists(file_path):
            print("해당 파일이 존재하지 않습니다.")
            return

        # VirusTotal API 엔드포인트 및 헤더 설정
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': self.virustotal_api_key}
        files = {'file': (os.path.basename(file_path), open(file_path, 'rb'))}

        # 파일 업로드
        response = requests.post(url, files=files, params=params)
        result = response.json()

        if 'resource' in result:
            # 업로드가 성공하면 결과를 가져와서 파일의 리포트 링크를 생성
            resource = result['resource']
            report_url = f'https://www.virustotal.com/gui/file/{resource}/detection'
            print(f"파일이 업로드되었습니다. 리포트 링크: {report_url}")
        else:
            print("파일 업로드에 실패했습니다.")

    def change_directory(self):
        # 디렉토리 설정으로 이동
        directory = QFileDialog.getExistingDirectory(
            self, "디렉토리 설정으로 이동", os.getcwd())
        if directory:
            os.chdir(directory)
            self.list_files()


if __name__ == "__main__":
    app = QApplication([])
    window = FileExplorer()
    window.show()
    app.exec()