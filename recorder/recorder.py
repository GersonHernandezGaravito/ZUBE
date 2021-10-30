# -*- Coding: utf-8 -*-
# Utiles
from .utils import file_exists, random_name, write_file, remove_file
from .models import Audio
from .services import AudioService
from .plugins.audio_help import AudioHelp
from config import Settings, Routes 
import cv2
import tkinter as tk
import numpy as np
import pyautogui
from tkinter.filedialog import asksaveasfilename
import time
import sys
import threading
from os import remove
import webbrowser, os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Record():
    """ Clase de grabación de audio. """
    accionaudio = False
    accionmicro = False
    tipo = 0
    
    def __init__(self, interface):
        self.routes = Routes()
        self.interface = interface
        self.audio_h = AudioHelp()
        self.listAudios()
        self.filename = None
        self.filenamevideo = None
        self.STATUS = 1
        self.SCREEN_SIZE = pyautogui.size()
        
    def uploadRecording(self, pathVid, filename):
        gauth = GoogleAuth()  
        drive = GoogleDrive(gauth) 

        upload_file_list = [pathVid]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'title': filename + '.mp4'})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload() # Upload the file.
            self.interface.updateButtonUser()

    def verifyLogin(self):
        if(os.path.isfile('credentials.json')):
            remove('credentials.json')
            self.interface.updateButtonUser()
        else:
            gauth = GoogleAuth() 
            gauth.LocalWebserverAuth() 
            
            self.interface.updateButtonUser()

      
    def accionAudio(self):
        self.accionaudio = not self.accionaudio
        self.interface.updateButtonAud(self.accionaudio)
        self.tipoGrab()

    def accionMicro(self):
        self.accionmicro = not self.accionmicro
        self.interface.updateButtonMic(self.accionmicro)
        self.tipoGrab()
        

    def tipoGrab(self):
        """ Método de grabación de audio. """
        self.audio_h.type_recording(accionmicro= self.accionmicro, accionaudio=self.accionaudio)
        #print(self.accionmicro, "---", self.accionaudio)


    def saveAudio(self, filename):
        """ Método para guardar registro de audios. """
        try:
            # Guardar registros
            self.interface.showMessageInfo("Video Guardado.")
            #print(self.filenamevideo)
            audio = Audio(filename, self.filenamevideo)
            audio_service = AudioService(self.routes.table_name)
            audio_service.create_audio(audio)
            # Refrescar vista
            self.listAudios()
            

        except Exception as e:
            self.interface.showMessageInfo("Error al guardar los archivos.")
            return e


    def listAudios(self):
        """ Método para listar grabaciones. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        for audio in audios:
            audio = audio.update(
                dict(
                    methods=[
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_delete),
                            action=self.deleteAudio
                        ),
                        dict(
                            button=self.interface.btnActions.__class__(param=audio['uid'], path_icon=self.routes.icon_play),
                            action=self.playAudio
                        )
                    ]
                )
            )

        self.interface.updateTable(
            headers=Audio.schema() + ["Acciones"],
            data=audios, 
        )

    def getAudio(self, uid):
        """ Método para obtener un audio por UID. """
        audio_service = AudioService(self.routes.table_name)
        audios = audio_service.list_audios()
        audio = [audio for audio in audios if audio['uid'] == uid]
        if audio == []:
            return None
        return audio[0]


    def recordAudio(self, callback):
        """ Método de grabación de audio. """
        try:
            
            self.filename = random_name("record")
            self.filenamevideo = self.filename
            url_path = self.routes.base_audio_url + self.filename + ".wav"
            url_path2 = self.routes.base_audio_url + self.filename + ".avi"
            url_path3 = self.routes.base_audio_url + self.filename + ".mp4"
            self.interface.updateInfoBox("Grabando ...")
            
            #threadvideo = threading.Thread(target=self.demonioVideo, args=(url_path2))
            #threadvideo.daemon=True
            #threadaudio = threading.Thread(target=self.demonioAudio, args =(url_path, callback))
            #threadaudio.daemon=True
            #print("bp1")
            #threadaudio.start()  
            #threadvideo.start()
            #print("bp2")
            
            #print("bp3")    
            self.audio_h.start_recording(url_path=url_path, url_path2=url_path2, url_path3=url_path3, callback_refresh=callback, callback_final=self.finalAudio)
            self.borrarArchivosTemp(url_path, url_path2)
            self.saveAudio(url_path3)
            self.uploadRecording(url_path3, self.filenamevideo)
            self.interface.updateInfoBox("Video Guardado ...")
        except Exception as e:
            print(e)
            self.interface.showMessageInfo("Error de grabación.")

    def borrarArchivosTemp(self, path1, path2):
        remove(path1)
        remove(path2)

    def demonioVideo(self, file_name):
        print("bp4")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        
        out = cv2.VideoWriter(file_name, fourcc, 20.0, (self.SCREEN_SIZE))
        self.STATUS = 1
        odd=1
        while True:
            odd+=1
            # make a screenshot
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if(odd==10):
                cv2.imshow("Recording...", frame)
                odd=1
            # if the user clicks q, it exits
            if cv2.waitKey(1) == ord("q"):
                cv2.destroyAllWindows()
                break
            # write the frame
            out.write(frame)
        out.release()
        
        
    def demonioAudio(self, url_path, callback):
        print("bp5")
        self.audio_h.start_recording(url_path=url_path, callback_refresh=callback, callback_final=self.finalAudio)

    def stopAudio(self):
        """ Método de grabación de audio. """
        try:
            self.interface.updateInfoBox("Guardando Video ...")
            self.STATUS = 0
            self.audio_h.stop_recording()
        except:
            self.interface.showMessageInfo("Error de grabación.")
        

    def finalAudio(self):
        """ Método de finalización de grabación. """
        try:
            if self.filename is not None:
                text = self.audio_h.__class__().read_audio(
                    url_path=self.routes.base_audio_url + self.filename + ".wav",
                    language=Settings.language    
                )
                #self.interface.updateInfoBox("Has dicho: \n{}".format(text))
                #self.saveAudio(filename=self.filename, text=text)
        except:
            self.interface.showMessageInfo("Error de grabación.")
        finally:
            self.filename = None



    def deleteAudio(self, uid):
        """ Método para eliminar audio. """
        audio_service = AudioService(self.routes.table_name)
        audio = self.getAudio(uid)
        if audio:
            audio_service.delete_audio(audio["uid"])
            remove_file(audio["path"])
            remove_file(self.routes.base_text_audio_url + audio["path"] + ".txt")
            self.listAudios()
            self.interface.showMessageInfo("Audio eliminado del sistema.") 
        else:
            self.interface.showMessageInfo("El uid no existe en el sistema.") 


    def playAudio(self, uid):
        """ Método para reproducir audio. """
        try:
            audio = self.getAudio(uid)
            
            if audio:
                audio_url = audio["path"] 
                if file_exists(audio_url):

                    webbrowser.open(os.path.realpath(audio_url))
                else:
                    self.interface.showMessageInfo("Audio no encontrado.")
            else:
                self.interface.showMessageInfo("Audio no seleccionado.")

        except Exception as e:
            self.interface.showMessageInfo("No se puede reproducir el Audio.")
            print(e)