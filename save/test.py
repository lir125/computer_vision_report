import sys
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog


class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("photoshop program")
        
        #menu bar
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("파일")
        exit = QAction("나가기", self, triggered=QApplication.quit)
        self.menu_file.addAction(exit)

        #main rayout
        main_layout = QHBoxLayout()

        #side bar menu button
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("좌우반전")
        button3 = QPushButton("새로고침")
        button4 = QPushButton("저장하기")

        button1.clicked.connect(self.showfile)
        button2.clicked.connect(self.flip_image)
        button3.clicked.connect(self.clear_label)
        button4.clicked.connect(self.savefile)
        
        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)

        main_layout.addLayout(sidebar)

        self.lable1 = QLabel(self)
        self.lable1.setFixedSize(640, 480)
        main_layout.addWidget(self.lable1)

        self.lable2 = QLabel(self)
        self.lable2.setFixedSize(640, 480)
        main_layout.addWidget(self.lable2)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def file_name_load(self):
        global file_name
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")

    def showfile(self):
        self.file_name_load()
        print(file_name)
        self.image = cv2.imread(file_name[0])
        h, w, _ = self.image.shape
        byte_per_line = 3 * w
        image = QImage(self.image.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable1.setPixmap(pixmap)

    def flip_image(self):
        image = cv2.flip(self.image, 1)
        global img2
        img2 = image
        h, w, _ = image.shape
        byte_per_line = 3 * w
        image = QImage(image.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)

        self.lable2.setPixmap(pixmap)

    def savefile(self):
        list_ = list(file_name[0].split("/"))
        list_.pop()
        list_ = "/".join(list_)
        newname = input()
        list_ = list_ + "/" + newname + ".jpg"
        print(list_)
        cv2.imwrite(list_, img2)

    def clear_label(self):
        self.lable2.clear()


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   