import sys 
import os 
import pathlib
from aug_class import GeneratorImage
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic  

form_ui = uic.loadUiType("form.ui")[0]

class WindowClass(QMainWindow, form_ui):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)

        self.BtnImageLoad.clicked.connect(self.ImageLoad) 

    def ImageLoad(self):
        format = [".jpg", ".png", ".jpeg", ".bmp", ".JPG", ".JPEG", ".BMP"]
        img = QFileDialog.getOpenFileName()
        # img[0] : 경로
        # img[1] : 파일 타입
        global path
        path = img[0]
        checkFile = pathlib.Path(path)

        if checkFile.suffix not in format :
            print("이미지 파일이 아닙니다!")

        self.ImageViewer = QPixmap()
        self.ImageViewer.load(path) 
        self.ImageViewer = self.ImageViewer.scaled(391, 471)
        self.lblImage.setPixmap(self.ImageViewer)
    
    def ParamSave():
        global rotation, widht_shift, height_shift
        global zoom_range, shear_range, horizontal_flip, count  

    def GenStart():
        GeneratorImage.Generator_Image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()