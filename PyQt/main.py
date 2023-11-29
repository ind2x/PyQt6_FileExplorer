from PyQt6 import QtCore, QtGui, QtWidgets
import sys
from FileExplorer import kFileExplorer
from CheckFileExtension import kCheckFileExtension

class MainHome(object):
    def setupUi(self, Form):
        # 메인 폼의 속성 설정
        Form.setObjectName("Form")
        Form.resize(787, 402)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./image/icon.png"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("")

        # 수평 레이아웃 생성
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 수직 레이아웃 생성
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # 파일탐색기 버튼 생성 및 수직 레이아웃에 추가
        self.Btn_FileExplorer = QtWidgets.QCommandLinkButton(parent=Form)
        self.Btn_FileExplorer.setStyleSheet("font: 700 11pt \"맑은 고딕\";")
        self.Btn_FileExplorer.setObjectName("Btn_FileExplorer")
        self.verticalLayout.addWidget(self.Btn_FileExplorer)

        # 수평 라인 생성 및 수직 레이아웃에 추가
        self.line = QtWidgets.QFrame(parent=Form)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        # 확장자검사 버튼 생성 및 수직 레이아웃에 추가
        self.Btn_CheckFileExtension = QtWidgets.QCommandLinkButton(parent=Form)
        self.Btn_CheckFileExtension.setStyleSheet("font: 700 11pt \"맑은 고딕\";")
        self.Btn_CheckFileExtension.setObjectName("Btn_CheckFileExtension")
        self.verticalLayout.addWidget(self.Btn_CheckFileExtension)

        # 수평 라인 생성 및 수직 레이아웃에 추가
        self.line_2 = QtWidgets.QFrame(parent=Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        # 바이러스검사 버튼 생성 및 수직 레이아웃에 추가
        self.Btn_VirusCheck = QtWidgets.QCommandLinkButton(parent=Form)
        self.Btn_VirusCheck.setStyleSheet("font: 700 11pt \"맑은 고딕\";")
        self.Btn_VirusCheck.setObjectName("Btn_VirusCheck")
        self.verticalLayout.addWidget(self.Btn_VirusCheck)

        # 메인 수평 레이아웃에 수직 레이아웃 추가
        self.horizontalLayout.addLayout(self.verticalLayout)

        # 수직 라인 생성 및 메인 수평 레이아웃에 추가
        self.line_3 = QtWidgets.QFrame(parent=Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)

        # 스타일이 적용된 프레임 생성 및 메인 수평 레이아웃에 추가
        self.frame = QtWidgets.QFrame(parent=Form)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")

        # 프레임 안에 수직 레이아웃 추가
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # 이미지가 있는 프레임 생성 및 수직 레이아웃에 추가
        self.frame_2 = QtWidgets.QFrame(parent=self.frame)
        self.frame_2.setStyleSheet("image: url(./image/title.png);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2.addWidget(self.frame_2)

        # 이미지가 있는 프레임 생성 및 수직 레이아웃에 추가
        self.frame_3 = QtWidgets.QFrame(parent=self.frame)
        self.frame_3.setStyleSheet("image: url(./image/main_image.png);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2.addWidget(self.frame_3)

        # 메인 수평 레이아웃에 프레임 추가
        self.horizontalLayout.addWidget(self.frame)

        # UI 텍스트 설정 함수 호출
        self.retranslateUi(Form)

        # 시그널과 슬롯 연결
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 파일탐색기 버튼에 연결할 함수 지정
        self.Btn_FileExplorer.clicked.connect(self.openFileExplorer)
        self.FileExplorer_form = None

        # 확장자검사 버튼에 연결할 함수 지정
        #self.Btn_CheckFileExtension.clicked.connect(self.openCheckFileExtension)
        self.CheckFileExtension_form = None

        # 바이러스검사 버튼에 연결할 함수 지정
        #self.Btn_VirusCheck.clicked.connect(self.openVirusCheck)
        self.VirusCheck_form = None

    def openFileExplorer(self):
        # 파일탐색기 버튼 클릭 시 실행되는 함수
        self.FileExplorer_form = QtWidgets.QMainWindow()
        ui_file_explorer = kFileExplorer()
        ui_file_explorer.setupUi(self.FileExplorer_form)
        self.FileExplorer_form.show()

    def openCheckFileExtension(self):
        # 확장자검사 버튼 클릭 시 실행되는 함수
        self.CheckFileExtension_form = QtWidgets.QMainWindow()
        ui_check_file_extension = kCheckFileExtension()
        ui_check_file_extension.setupUi(self.CheckFileExtension_form)
        self.CheckFileExtension_form.show()
    
    '''
    def openVirusCheck(self):
        # 바이러스검사 버튼 클릭 시 실행되는 함수
        virus_check_ui = QtWidgets.QWidget()
        virus_check_form = loadUi("virus_check.ui", virus_check_ui)
        virus_check_ui.show()
    '''

    # UI 텍스트를 설정하는 함수
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "5Sorry"))
        self.Btn_FileExplorer.setText(_translate("Form", "파일탐색기"))
        self.Btn_CheckFileExtension.setText(_translate("Form", "확장자검사"))
        self.Btn_VirusCheck.setText(_translate("Form", "바이러스검사"))


# 메인 스크립트 부분
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MainHome()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
