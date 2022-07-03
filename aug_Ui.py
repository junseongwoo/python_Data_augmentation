from ast import Try
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

        self.initStyleSheet()
        self.initConfig()

        self.BtnImageLoad.clicked.connect(self.ImageLoad) 
        self.BtnPathSave.clicked.connect(self.PathSave)
        self.BtnConfigSave.clicked.connect(self.TreeWidgetSave)
        self.BtnConfigSave.clicked.connect(self.ConfigSave)
        self.SldRotation.valueChanged.connect(self.ValueChange)
        self.SldZoom.valueChanged.connect(self.ValueChange)
        self.SldWidthShift.valueChanged.connect(self.ValueChange)
        self.SldHeightShift.valueChanged.connect(self.ValueChange)
        self.SldShear.valueChanged.connect(self.ValueChange)

    def initStyleSheet(self):
        self.lblImage.setStyleSheet("color:red;"
                                    "background-color: #b5b5b5;"
                                    )

    def initConfig(self):
        self.img_path = None
        self.save_path = 'C:/'
        self.rotation = 0
        self.shear_range = 0
        self.zoom_range = 0
        self.width_shift = 0
        self.height_shift = 0 
        self.horizontal_flip = True
        self.count = 10 
    
    '''
    to do list 
    '''
    def ConfigSave(self):
        save_path = QFileDialog.getSaveFileName(self, filter='.txt')[0]
        file = open(save_path, 'w')
        text = self.TWConfig.currentItem()
        file.write(text)
        file.close()
    
    #def ConfigLoad(self):

    def ValueChange(self):
        self.lblRotation.setText("±" + str(self.SldRotation.value()) + '°')
        self.lblZoom.setText("±" + str(self.SldZoom.value())+ "%")
        self.lblWidthShift.setText("±" + str(self.SldWidthShift.value())+ "%")
        self.lblHeightShift.setText("±" + str(self.SldHeightShift.value())+ "%")
        self.lblShear.setText("±" + str(self.SldShear.value())+ '°')
        #self.lblZoom.setText("±" + str(round(self.SldZoom.value() / 100.0, 1)) + "%")

    def ImageLoad(self):
        format = [".jpg", ".png", ".jpeg", ".bmp", ".JPG", ".JPEG", ".BMP"]
        img = QFileDialog.getOpenFileName()
        # img[0] : 경로
        # img[1] : 파일 타입
        
        self.img_path = img[0]
        checkFile = pathlib.Path(self.img_path)
        print(checkFile.stem)

        if checkFile.suffix not in format :
            print("이미지 파일이 아닙니다!")

        self.ImageViewer = QPixmap()
        self.ImageViewer.load(self.img_path) 
        self.ImageViewer = self.ImageViewer.scaled(391, 550)
        self.lblImage.setPixmap(self.ImageViewer)
    
    def StartGen():
        GeneratorImage.Generator_Image

    def PathSave(self):
        self.save_path = QFileDialog.getExistingDirectory()
        if self.save_path == "":
            self.save_path = 'C:/'
        else:
            self.split = self.save_path.split('/')
            self.save_path = "../" + self.split[-2] + '/' + self.split[-1]
            self.lblSavePath.setText(self.save_path)
        print(self.TWConfig.takeTopLevelItem(0))
        print(str(self.TWConfig.takeTopLevelItem(1)))
        
    def TreeWidgetSave(self):
        parameter_item = self.TWConfig.topLevelItem(0)
        parameter_item.child(0).setText(1, str(self.SldRotation.value()))
        parameter_item.child(1).setText(1, str(round(self.SldWidthShift.value() / 100.0, 1)))
        parameter_item.child(2).setText(1, str(round(self.SldHeightShift.value() / 100.0, 1)))
        parameter_item.child(3).setText(1, str(round(self.SldShear.value() / 100.0 , 1)))
        parameter_item.child(4).setText(1, str(round(self.SldZoom.value() / 100.0, 1)))

        if int(self.TxtCount.text()) >= 101:
            self.TxtCount.setText("100")
        parameter_item.child(5).setText(1, str(self.TxtCount.text()))

        if self.CboFlip.currentText() == 'On':
            self.horizontal_flip = True
        else :
            self.horizontal_flip = False
        parameter_item.child(6).setText(1, str(self.horizontal_flip))

        path_item = self.TWConfig.topLevelItem(1) 
        if self.lblSavePath.text() == 'C:/':
            self.save_path = self.save_path
        path_item.setText(1, self.save_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()