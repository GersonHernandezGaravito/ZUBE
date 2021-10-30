# -*- Coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLabel,  QGridLayout
from .plugins.pyqt5_custom import MessageCustom, InputCustom, ButtonCustom, BoxInfoCustom, TableWidgetCustom, MultipleLayoutWidgetCustom
from config import Settings, Routes
import os

class RecordingAppInterface(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'ZUBE'
        self.left = 0
        self.top = 0
        self.width = 450
        self.height = 550
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createForm() 
        self.infoGroupBox = BoxInfoCustom(title=".:: Información de grabación ::.")
        self.infoButton = ButtonCustom()
        self.tableWidget = TableWidgetCustom()
        
 
        # BOX - LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.formGroupBox) 
        self.layout.addWidget(self.infoGroupBox) 
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
        # MOSTRAR WIDGET
        self.show()

    def createForm(self):
        layout = QFormLayout()

        self.formGroupBox = QGroupBox("Grabación")
        self.btnRecord = ButtonCustom("Grabar ", styles=Settings.style_btn_info, path_icon=Routes.icon_microphone)
        self.btnStop = ButtonCustom("Detener ", styles=Settings.style_btn_danger, path_icon=Routes.icon_stop)
        
        self.btnMicAD = ButtonCustom("", styles=Settings.style_btn_mic, path_icon=Routes.icon_microfono_d)
        self.btnAudAD = ButtonCustom("", styles=Settings.style_btn_mic, path_icon=Routes.icon_audio_d)
        
        if(os.path.isfile('credentials.json')):
            self.btnUser = ButtonCustom(path_icon=Routes.icon_logout, styles=Settings.style_btn_user)
        else:
            self.btnUser = ButtonCustom(path_icon=Routes.icon_login, styles=Settings.style_btn_user)

        self.btnUser.setSize(28, 28)
        self.btnMicAD.setSize(28, 28)
        self.btnAudAD.setSize(28, 28)
        self.btnActions = ButtonCustom("")


        layout.addRow(MultipleLayoutWidgetCustom(elements=[self.btnRecord, self.btnStop, self.btnUser]))
        layout.addRow(MultipleLayoutWidgetCustom(elements=[self.btnMicAD, self.btnAudAD]))
        self.formGroupBox.setLayout(layout)  

    def updateButtonUser(self):
        if(os.path.isfile('credentials.json')):
            self.btnUser = self.infoButton.updateButton(path_icon=Routes.icon_logout)
        else:
            self.btnUser = self.infoButton.updateButton(path_icon=Routes.icon_login)
     

    def updateButtonMic(self, accionmicro):
        if(accionmicro == False):
            self.btnMicAD = self.infoButton.updateButton(path_icon=Routes.icon_microfono_d)
        else:
            self.btnMicAD = self.infoButton.updateButton(path_icon=Routes.icon_microfono_a)    
        

    def updateButtonAud(self, accionaudio):
        if(accionaudio == False):
            self.btnAudAD = self.infoButton.updateButton(path_icon=Routes.icon_audio_d)
        else:
            self.btnAudAD = self.infoButton.updateButton(path_icon=Routes.icon_audio_a)    

    def updateInfoBox(self, info=None, styles=None):
        self.infoGroupBox.updateBox(info=info, styles=styles)

    def cleanInfoBox(self):
        self.infoGroupBox.cleanBox()
    
    def updateTable(self, headers=None, data=None):
        self.tableWidget.updateInfoTable(headers=headers, data=data)
    
    def showMessageInfo(self, text):
        msgBox = MessageCustom()
        msgBox.showMessage(text)

    

