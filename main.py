import sys
import cv2
import numpy as np
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
        button6 = QPushButton("흑백필터")
        button5 = QPushButton("볼록하게")
        button7 = QPushButton("오목하게")
        button8 = QPushButton("모자이크")
        button9 = QPushButton("경계추출")
        button10 = QPushButton("블러처리")
        button3 = QPushButton("초기화")
        button4 = QPushButton("저장하기")

        button1.clicked.connect(self.showfile)
        button2.clicked.connect(self.flip_image)
        button6.clicked.connect(self.black_white)
        button5.clicked.connect(self.lens)
        button7.clicked.connect(self.lens1)
        button8.clicked.connect(self.mosaic)
        button9.clicked.connect(self.canny)
        button10.clicked.connect(self.blurr)
        button3.clicked.connect(self.clear_label)
        button4.clicked.connect(self.savefile)
        
        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button6)
        sidebar.addWidget(button5)
        sidebar.addWidget(button7)
        sidebar.addWidget(button8)
        sidebar.addWidget(button9)
        sidebar.addWidget(button10)
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

    def showfile(self):
        global file_name
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image = cv2.imread(file_name[0])
        global img2
        global isgray
        isgray = False
        img2 = self.image
        h, w, _ = self.image.shape

        byte_per_line = 3 * w
        image = QImage(self.image.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable1.setPixmap(pixmap)

    def flip_image(self):
        global img2
        global isgray

        img2 = cv2.flip(img2, 1)
        h, w = img2.shape[0], img2.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)
    
    def black_white(self):
        global img2
        global isgray
        if isgray == True:
            return
        else:
            isgray = True
            image = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
            # image = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
            img2 = image
            h, w = image.shape[0], image.shape[1]
            byte_per_line = w
            image = QImage(image.data, w, h, byte_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap(image)
            self.lable2.setPixmap(pixmap)

    def lens(self):
        global img2
        image = img2
        height, width = image.shape[:2]

        exp = 1.1  
        scale = 1
        mapy, mapx = np.indices((height, width), dtype=np.float32)

        mapx = 2 * mapx / (width-1) - 1
        mapy = 2 * mapy / (height-1) - 1

        r, theta = cv2.cartToPolar(mapx, mapy)  
        r[r < scale] = r[r < scale] ** exp

        mapx, mapy = cv2.polarToCart(r, theta)  
        mapx = ((mapx +  1) * width - 1) / 2
        mapy = ((mapy +  1) * height - 1) / 2

        distorted = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
        img2 = distorted

        h, w = distorted.shape[0], distorted.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(distorted.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(distorted.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)

    def lens1(self):
        global img2
        image = img2
        height, width = image.shape[:2]

        exp = 0.9  
        scale = 1
        mapy, mapx = np.indices((height, width), dtype=np.float32)

        mapx = 2 * mapx / (width-1) - 1
        mapy = 2 * mapy / (height-1) - 1

        r, theta = cv2.cartToPolar(mapx, mapy)  
        r[r < scale] = r[r < scale] ** exp

        mapx, mapy = cv2.polarToCart(r, theta)  
        mapx = ((mapx +  1) * width - 1) / 2
        mapy = ((mapy +  1) * height - 1) / 2

        distorted = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
        img2 = distorted

        h, w = distorted.shape[0], distorted.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(distorted.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(distorted.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)

    def mosaic(self):
        global img2
        img = img2
        rate = 10
        while True:
            x, y, w, h = cv2.selectROI("test", img, False)
            if w and h:
                roi = img[y:y+h, x:x+w]
                roi = cv2.resize(roi, (w//rate, h//rate))
                roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_AREA)

                img[y:y+h, x:x+w] = roi
                cv2.imshow("test", img)

            else:
                break
        cv2.destroyAllWindows()


        h, w = img2.shape[0], img2.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)
        
    def canny(self):
        global img2
        img = img2
        global isgray
        isgray = True
        if isgray ==True:
            img_gray = img
        else:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        median = np.median(img_gray)

        lower_threshold = int(max(0, (1.0 - 0.33) * median))
        upper_threshold = int(min(255, (1.0 + 0.33) * median))

        img_canny = cv2.Canny(img_gray, lower_threshold, upper_threshold)
        img2 = img_canny
        h, w = img2.shape[0], img2.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)

    def blurr(self):
        global img2
        img = img2
        blur = cv2.bilateralFilter(img, 5, 75, 75)
        
        img2 = blur
        h, w = img2.shape[0], img2.shape[1]
        if isgray == True:
            byte_per_line = w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_Grayscale8)
        else:
            byte_per_line = 3 * w
            image = QImage(img2.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)

    def savefile(self):
        file_name = QFileDialog.getSaveFileName(self, "이미지 열기", "./")
        list_ = file_name[0]
        list_ = list_.split("/")
        last = list_[-1]
        idx = last.find(".")
        v = last[idx:]
        k = [".jpg", ".jpeg", ".png"]
        if v in k:
            cv2.imwrite(file_name[0], img2)
        else:
            cv2.imwrite(file_name[0]+".jpg", img2)

    def clear_label(self):
        self.lable2.clear()
        
        global img2
        global isgray
        img2 = cv2.imread(file_name[0])
        isgray = False
        h, w, _ = img2.shape

        byte_per_line = 3 * w
        image = QImage(img2.data, w, h, byte_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(image)
        self.lable2.setPixmap(pixmap)



if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   