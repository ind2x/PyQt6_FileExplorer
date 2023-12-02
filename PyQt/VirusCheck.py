from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os
from MyFileManager import FileManager
import requests

file_manager = FileManager()

if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 경우
    script_directory = os.path.dirname(sys.executable) + '\\..'
else:
    # 일반적으로 실행되는 경우
    script_directory = os.path.dirname(os.path.realpath(__file__))

class VirusTotalFileAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "x-apikey": api_key
        }

    def analyze_file(self, file_path, file_size):
        # Step 1: File Upload
        # If the file to be uploaded is bigger than 32MB, 
        # please use the /files/upload_url endpoint instead which admits files up to 650MB.
        size = float(file_size.split()[0])
        byte = file_size.split()[1]

        if byte == "MB" and size > 32:
            upload_url = "https://www.virustotal.com/api/v3/files/upload_url"
        else:
            upload_url = "https://www.virustotal.com/api/v3/files"

        files = {"file": (file_path, open(file_path, "rb"),
                          "application/octet-stream")}
        upload_response = requests.post(
            upload_url, files=files, headers=self.headers)
        upload_data = upload_response.json()

        # Check if the upload was successful
        if upload_response.status_code != 200:
            print("File upload failed.")
            return None

        analysis_id = upload_data["data"]["id"]

        # Step 2: Get Analysis Report
        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
        analysis_response = requests.get(analysis_url, headers=self.headers)
        analysis_data = analysis_response.json()

        return analysis_data

    @staticmethod
    def extract_results(analysis_data):
        if not analysis_data or "data" not in analysis_data:
            print("Invalid analysis data.")
            return None

        file_info = analysis_data["meta"]["file_info"]
        sha256 = file_info.get("sha256", {})

        attributes = analysis_data["data"]["attributes"]

        # Extract relevant information
        stats = attributes.get("stats", {})
        malicious_count = stats.get("malicious", 0)
        undetected_count = stats.get("undetected", 0)

        return {
            "report_link": f'https://www.virustotal.com/gui/file/{sha256}/detection',
            "malicious_count": malicious_count,
            "undetected_count": undetected_count
        }


class kVirusCheck(object):
    def setupUi(self, MainWindow):
        # 디렉터리 경로 저장
        self.directory = ''

        # MainWindow 설정
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 585)
        MainWindow.setStyleSheet("")

        # 아이콘 설정
        icon_path = os.path.join(script_directory, 'image', 'icon.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        # centralwidget 설정
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # verticalLayout 설정
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # horizontalLayout_2 설정 (버튼 레이아웃)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Btn_home 설정
        self.Btn_home = QtWidgets.QPushButton(parent=MainWindow)
        self.Btn_home.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.Btn_home.setObjectName("Btn_home")
        self.horizontalLayout_2.addWidget(self.Btn_home)

        # Btn_close 설정
        self.Btn_close = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Btn_close.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.Btn_close.setObjectName("Btn_close")
        self.horizontalLayout_2.addWidget(self.Btn_close)

        # 폴더 선택
        self.Btn_SetDirectoryPath = QtWidgets.QPushButton(
            parent=self.centralwidget)
        self.Btn_SetDirectoryPath.setStyleSheet(
            "background-color: rgb(85, 170, 255);")
        self.Btn_SetDirectoryPath.setObjectName("Btn_SetDirectoryPath")
        self.horizontalLayout_2.addWidget(self.Btn_SetDirectoryPath)

        # 바이러스 검사 버튼
        self.Btn_VirusCheck = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Btn_VirusCheck.setStyleSheet(
            "background-color: rgb(85, 170, 255);")
        self.Btn_VirusCheck.setObjectName("VirusCheck")
        self.horizontalLayout_2.addWidget(self.Btn_VirusCheck)

        # Btn_refresh 설정
        self.Btn_refresh = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Btn_refresh.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.Btn_refresh.setObjectName("Btn_refresh")
        self.horizontalLayout_2.addWidget(self.Btn_refresh)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # horizontalLayout 설정 (검색 및 콤보박스 레이아웃)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 검색 입력란 설정
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        # 검색 기능을 위한 함수 정의
        def search_table():
            search_text = self.lineEdit.text().lower()  # 검색어를 소문자로 변환하여 비교
            for row_idx in range(self.tableWidget.rowCount()):
                row_hidden = True
                for col_idx in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row_idx, col_idx)
                    if item is not None:
                        cell_data = item.text().lower()
                        if search_text in cell_data:
                            row_hidden = False
                            break
                self.tableWidget.setRowHidden(row_idx, row_hidden)

        # 검색어가 변경될 때마다 검색 함수 호출
        self.lineEdit.textChanged.connect(search_table)

        # 콤보 박스 설정
        self.comboBox = QtWidgets.QComboBox(parent=self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(100, 22))
        self.comboBox.setMaximumSize(QtCore.QSize(150, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("전체")
        self.comboBox.addItem("문서")
        self.comboBox.addItem("실행파일")
        self.comboBox.addItem("사진")
        self.horizontalLayout.addWidget(self.comboBox)

        # verticalLayout에 horizontalLayout 추가
        self.verticalLayout.addLayout(self.horizontalLayout)

        # scrollArea_2 설정
        self.scrollArea_2 = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea_2.setStyleSheet("")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")

        # scrollAreaWidgetContents_2 설정
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 816, 482))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # tableWidget 설정
        self.tableWidget = QtWidgets.QTableWidget(
            parent=self.scrollAreaWidgetContents_2)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1200, 1200))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(1200, 1200))
        self.tableWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.tableWidget.setMouseTracking(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)

        # 테이블 열 헤더 설정
        self.tableWidget.setHorizontalHeaderLabels(
            ["이름", "경로", "사이즈", "바이러스 체크", "진행 상태", "링크"])
        header = self.tableWidget.horizontalHeader()

        # 파일 경로를 넘겨받으면 해당 경로에 있는 목록 출력
        # 사용자에게 디렉토리 선택 대화상자 표시
        self.setDirectoryPath()

        self.horizontalLayout_3.addWidget(self.tableWidget)

        # scrollArea_2에 scrollAreaWidgetContents_2 설정
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        # verticalLayout에 scrollArea_2 추가
        self.verticalLayout.addWidget(self.scrollArea_2)

        # MainWindow에 centralwidget 설정
        MainWindow.setCentralWidget(self.centralwidget)

        # statusbar 설정
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 버튼 동작 연결
        self.Btn_home.clicked.connect(MainWindow.close)
        self.Btn_close.clicked.connect(self.close_window)
        self.Btn_SetDirectoryPath.clicked.connect(self.setDirectoryPath)
        self.Btn_VirusCheck.clicked.connect(self.VirusCheck)
        self.Btn_refresh.clicked.connect(self.refresh)

        # F5 단축키 설정
        self.actionRefresh = QtGui.QAction(MainWindow)
        self.actionRefresh.setShortcut(
            QtGui.QKeySequence(QtCore.Qt.Key.Key_F5))
        self.actionRefresh.triggered.connect(self.refresh)
        MainWindow.addAction(self.actionRefresh)

        # UI 다시 설정
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 콤보 박스 선택에 따라 테이블 필터링
        self.comboBox.currentIndexChanged.connect(self.filter_table)

    # table 설정
    def showTable(self):
        # 테이블 초기화
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        if file_manager.directory_path == '':
            pass
        else:
            # 데이터를 테이블에 추가
            files_info = file_manager.list_files_in_directory()
            for row_idx, row_data in enumerate(files_info):
                path = os.path.join(
                    row_data["file_path"], row_data["file_name"])
                isfile = os.path.isfile(path)

                if isfile:
                    row_idx = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_idx)  # 행 추가

                    # '진행상태'열 초기화
                    progress_item = QtWidgets.QTableWidgetItem("검사 전")
                    self.tableWidget.setItem(row_idx, 3, progress_item)

                    for col_idx, key in enumerate(["file_name", "file_path", "file_size"]):
                        item = QtWidgets.QTableWidgetItem(str(row_data[key]))
                        item.setFlags(
                            item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                        item.setFlags(
                            item.flags() & ~QtCore.Qt.ItemFlag.ItemIsDropEnabled)
                        self.tableWidget.setItem(row_idx, col_idx, item)

    # 버튼에 대한 동작수행 함수 정의
    def goHome(self):
        # 메인 화면으로 이동
        if self.parent is not None and isinstance(self.parent, QtWidgets.QMainWindow):
            self.parent.close()  # 현재 파일 탐색기 창을 닫음

    def close_window(self):
        # 파일 종료
        sys.exit(0)

    def setDirectoryPath(self):
        # 폴더 선택
        # 사용자에게 디렉토리 선택 대화상자 표시
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(
            None, "디렉토리 선택", os.getcwd())

        # 파일 경로를 넘겨받으면 해당 경로에 있는 목록 출력
        file_manager.setDirPath(self.directory)

        self.showTable()

    def VirusCheck(self):
        # 바이러스 검사
        for row_idx in range(self.tableWidget.rowCount()):
            # 파일명, 파일 경로 추출
            file_name = self.tableWidget.item(row_idx, 0).text()
            file_path = self.tableWidget.item(row_idx, 1).text()
            file_size = self.tableWidget.item(row_idx, 2).text()
            item_path = os.path.join(file_path, file_name)

            # 열 '진행상태'를 '검사 중'으로 변경
            progress_item = QtWidgets.QTableWidgetItem("검사 중")
            progress_item.setFlags(
                progress_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.tableWidget.setItem(row_idx, 4, progress_item)

            # Perform virus check and get results
            report_link, malicious_count, undetected_count = self.performVirusCheck(
                item_path, file_size)

            # '바이러스 체크' 열에 결과 값 넣기
            virus_check_item = QtWidgets.QTableWidgetItem(
                f"{malicious_count} / {undetected_count}")
            virus_check_item.setFlags(
                virus_check_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.tableWidget.setItem(row_idx, 3, virus_check_item)

            # '진행 상태' 열에 결과 값 넣기
            progress_item = QtWidgets.QTableWidgetItem("검사 완료")
            progress_item.setFlags(
                progress_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.tableWidget.setItem(row_idx, 4, progress_item)

            # '링크' 열에 버튼 추가 및 연결
            link_button = QtWidgets.QPushButton("Report Link")
            link_button.clicked.connect(
                lambda _, link=report_link: self.openReportLink(link))
            self.tableWidget.setCellWidget(row_idx, 5, link_button)

    def performVirusCheck(self, file_path, file_size):
        # Instantiate the VirusTotalFileAnalyzer with your API key
        virus_total_analyzer = VirusTotalFileAnalyzer(
            api_key='fbe03f99673d63e0f6c0a7bb0ef91a17dd7d634c39309dca174001ed1ed9b49c')

        # 바이러스 체크 실행 및 결과 가져오기
        analysis_data = virus_total_analyzer.analyze_file(file_path, file_size)

        # Extract relevant results using the provided method
        results = VirusTotalFileAnalyzer.extract_results(analysis_data)

        return results['report_link'], results['malicious_count'], results['undetected_count']

    def openReportLink(self, link):
        # Report 링크 열기
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))

    def refresh(self):
        # 현재 디렉토리의 파일 목록을 다시 가져와서 테이블에 표시
        file_manager.setDirPath(self.directory)

        self.showTable()

        # 새로고침 시 화면이 빠르게 꺼졌다 켜지는 것 같은 이펙트 대신에 statusBar에 문구 출력
        # 문구 출력 후 1초 후에 timeout 시그널이 발생하면 statusBar에 있는 문구를 지움
        self.statusbar.showMessage("Status: 새로고침")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.statusbar.clearMessage)
        self.timer.start(1000)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # 메인창 이름 설정
        MainWindow.setWindowTitle(_translate("MainWindow", "5Sorry"))

        # 버튼 이름 설정
        self.Btn_home.setText(_translate("MainWindow", "메인 홈으로 이동"))
        self.Btn_close.setText(_translate("MainWindow", "닫기"))
        self.Btn_SetDirectoryPath.setText(_translate("MainWindow", "폴더 선택"))
        self.Btn_VirusCheck.setText(_translate("MainWindow", "바이러스 검사"))
        self.Btn_refresh.setText(_translate("MainWindow", "새로고침(F5)"))

        # 콤보 박스 이름 설정
        self.comboBox.setItemText(0, _translate("MainWindow", "전체"))
        self.comboBox.setItemText(1, _translate("MainWindow", "문서"))
        self.comboBox.setItemText(2, _translate("MainWindow", "실행파일"))
        self.comboBox.setItemText(3, _translate("MainWindow", "사진"))

        # 테이블 헤더 이름 설정
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "이름"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "경로"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "사이즈"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "바이러스 체크"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "진행상태"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "링크"))

    def filter_table(self):
        selected_option = self.comboBox.currentText()
        for row_idx in range(self.tableWidget.rowCount()):
            # 파일명, 파일 경로 추출
            file_name = self.tableWidget.item(row_idx, 0).text()
            file_path = self.tableWidget.item(row_idx, 1).text()
            item_path = os.path.join(file_path, file_name)
            _, file_extension = os.path.splitext(item_path)  # 확장자 추출
            if selected_option == "전체":
                self.tableWidget.setRowHidden(row_idx, False)
            elif selected_option == "실행파일" and file_extension.lower() in {'.exe', '.bat', '.cmd', '.msi', '.sh', '.dll', '.ps1', '.com', '.jar', '.vbs'}:
                self.tableWidget.setRowHidden(row_idx, False)
            elif selected_option == "문서" and file_extension.lower() in {'.txt', '.doc', '.docx', '.pdf', '.xml', '.docx', '.hwp', '.hwpx', '.py', '.c', '.cpp', '.java', '.ppt', '.html', '.css', '.js', '.md'}:
                self.tableWidget.setRowHidden(row_idx, False)
            elif selected_option == "사진" and file_extension.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.ico', '.WMF', '.bmp'}:
                self.tableWidget.setRowHidden(row_idx, False)
            else:
                self.tableWidget.setRowHidden(row_idx, True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = kVirusCheck()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
