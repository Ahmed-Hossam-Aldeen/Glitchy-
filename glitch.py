from PyQt5 import QtWidgets, uic
import sys
from PyQt5.uic.properties import QtCore
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

import glitch_this
import requests # to get image from the web
import shutil # to save it locally
import os 

class MainWindow(QtWidgets.QMainWindow):      
    def __init__(self):   
        super(MainWindow, self).__init__()
        uic.loadUi('glitch.ui', self)
        self.download.clicked.connect(self.downloadz)
        self.glitch.clicked.connect(self.glitchz)
        self.setWindowTitle("Glitchy!")
        self.show() 
    
    def downloadz(self):
    ## Set up the image URL and filename
        image_url = self.plainTextEdit.toPlainText()
        self.filename = image_url.split('/')[-1]
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream = True)
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            with open(self.filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print('Image sucessfully Downloaded: ',self.filename)
        else:
            print('Image Couldn\'t be retreived')
    
    
    def glitchz(self):
        gain = self.horizontalSlider.value()/10
        #print(gain)
        
        if self.color.isChecked():
            color = "-c"
        else:
            color = ""           
        if self.sideline.isChecked():
            sideline = "-s"
        else:
            sideline = ""        
            
        command =(f'glitch_this {self.filename} {gain} {sideline} {color} -f')
        os.system(command)
        
        glitchedFileName = "glitched_"+ self.filename
        pixmap = QPixmap(glitchedFileName)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)        
app = 0            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()                    