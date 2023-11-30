from PyQt6 import QtWidgets
import sys


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        # 버튼 생성
        self.show_second_button = QtWidgets.QPushButton(
            "Show Second Window", self)
        self.show_second_button.clicked.connect(self.show_second_window)

    def show_second_window(self):
        # 두 번째 창 보이기
        self.second_window.show()


class SecondWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Second Window")

        # 버튼 생성
        self.show_main_button = QtWidgets.QPushButton("Show Main Window", self)
        self.show_main_button.clicked.connect(self.show_main_window)

    def show_main_window(self):
        # 첫 번째 창 보이기
        self.main_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 두 개의 창 생성
    main_window = MainWindow()
    second_window = SecondWindow()

    # 창 간에 참조를 설정
    main_window.second_window = second_window
    second_window.main_window = main_window

    # 애플리케이션 실행
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
