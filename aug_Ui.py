from ast import Try
import sys 
import os 
import pathlib
from tabnanny import check

from numpy import format_float_positional
from regex import X
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

        self.BtnGenStart.clicked.connect(self.StartGen)
        self.BtnImageLoad.clicked.connect(self.ImageLoad) 
        self.BtnPathSave.clicked.connect(self.PathSave)
        self.BtnConfigChange.clicked.connect(self.TreeWidgetChange)
        self.BtnConfigSave.clicked.connect(self.TreeWidgetChange)
        self.BtnConfigSave.clicked.connect(self.ConfigSave)
        self.BtnConfigLoad.clicked.connect(self.ConfigLoad)
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
        save_path = QFileDialog.getSaveFileName(self, '', filter='txt files (*.txt)')[0]
        param_item = self.TWConfig.topLevelItem(0)

        try : 
            with open(save_path, 'w') as file : 
                for i in range(7):
                    file.write(param_item.child(i).text(0) +'=' 
                    + param_item.child(i).text(1)+"\n")
                    if i == 6 :
                        file.write('save_path='+str(self.save_path)+'\n')
        except :
            pass 
    
    def ConfigLoad(self):
        txt_config = QFileDialog.getOpenFileName()
        txt_config = txt_config[0]
        checkFile = pathlib.Path(txt_config)
        
        try :
            if txt_config == '' or checkFile.suffix != '.txt' :
                pass
            else :
                with open(txt_config, 'r') as file :
                    data = file.readlines()
                    data = list(map(lambda x: x.strip(), data))
                    
                    for idx, val in enumerate(data):
                        val = val.split('=')
                        del data[idx]
                        data.insert(idx, val[1])
                self.TreeWidgetLoad(data)
        except:
            pass

    def TreeWidgetLoad(self, data):
        param_item = self.TWConfig.topLevelItem(0)
        for i in range(7):
            param_item.child(i).setText(1, data[i])

        if int(data[5]) >= 101:
            data[5] = '100'
            param_item.child(5).setText(1, data[5])
        
        self.SldRotation.setValue(int(data[0]))
        self.SldWidthShift.setValue(round(float(data[1])*100))
        self.SldHeightShift.setValue(round(float(data[2])*100))
        self.SldShear.setValue(round(float(data[3])*100))
        self.SldZoom.setValue(round(float(data[4])*100))
        self.TxtCount.setText(data[5])

        if data[6].upper() == 'TRUE':
            self.CboFlip.setCurrentIndex(0)
            self.horizontal_flip = True
        else :
            self.CboFlip.setCurrentIndex(1)
            self.horizontal_flip = False 

        path_item = self.TWConfig.topLevelItem(1)
        if data[7] == 'C:/':
            self.save_path = 'C:/'
            self.split_path = 'C:/'
        else : 
            self.save_path = data[7]
            self.split = data[7].split('/')
            self.split_path = "../" + self.split[-2] + '/' + self.split[-1]
        path_item.setText(1, self.split_path)
        self.lblSavePath.setText(self.split_path)

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

        # 파일명만 뽑아내기
        #print(checkFile.stem)
        #if checkFile.suffix not in format :
            #print("이미지 파일이 아닙니다!")
        try:
            if self.img_path == '' or checkFile.suffix not in format:
                pass
            else :
                self.ImageViewer = QPixmap()
                self.ImageViewer.load(self.img_path) 
                self.ImageViewer = self.ImageViewer.scaled(391, 550)
                self.lblImage.setPixmap(self.ImageViewer)
        except:
            pass

    def StartGen(self):
        GeneratorImage.Generator_Image(
            self.img_path,
            self.save_path, 
            int(self.TxtCount.text()),
            self.SldRotation.value(), 
            round(self.SldWidthShift.value() / 100.0, 1),
            round(self.SldHeightShift.value() / 100.0, 1),
            round(self.SldShear.value() / 100.0, 1),
            round(self.SldZoom.value() / 100.0, 1),
            self.horizontal_flip
            )

    def PathSave(self):
        self.save_path = QFileDialog.getExistingDirectory()
        if self.save_path == "":
            self.save_path = 'C:/'
            self.split_path = 'C:/'
        else:
            self.split = self.save_path.split('/')
            self.split_path = "../" + self.split[-2] + '/' + self.split[-1]
            self.lblSavePath.setText(self.split_path)

    def TreeWidgetChange(self):
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
            self.save_path = 'C:/'
            self.split_path = 'C:/'
        path_item.setText(1, self.split_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()