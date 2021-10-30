# -*- Coding: utf-8 -*-
import speech_recognition as sr
import pyaudio
import wave
import cv2
import tkinter as tk
import numpy as np
import pyautogui
from tkinter.filedialog import asksaveasfilename
import time
import sys
import moviepy.editor as mpe
import threading

class AudioHelp:
    """ Clase para grabar, reproducir y reconocer audio en texto. """

    def __init__(self, chunk=40960):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.P_AUD = pyaudio.PyAudio()
        self.FRAMES = []
        self.STATUS = 1
        self.TYPE = 0
        self.abierto = 1
        self.url = None
        self.STREAM = self.P_AUD.open(
            format=self.FORMAT, 
            channels=self.CHANNELS, 
            rate=self.RATE, 
            input=True, 
            frames_per_buffer=self.CHUNK
        )
        self.SCREEN_SIZE = pyautogui.size()


    def start_recording(self, url_path, url_path2, url_path3, callback_refresh, callback_final):
        """ 
            Método para comenzar grabación con pyaudio. 
            callback_refresh: Método para hacer el refresco de nuestra interfaz.
            callback_final: Método para indicar que la grabación ya se guardo y se puede hacer el siguiente paso.
        """
        
        self.STATUS = 1
        self.FRAMES = []
        print(self.STATUS)

        #fourcc = cv2.VideoWriter_fourcc(*"XVID")
        #out = cv2.VideoWriter(url_path2, fourcc, 1.0, (SCREEN_SIZE))
        count = 0
        #if(self.abierto == 1):
        self.url = url_path2
        threadvideo = threading.Thread(target=self.demonioVideo)
        threadvideo.daemon=True
        threadvideo.start()
        
        while self.STATUS == 1:
            if (self.TYPE == 1):
                stream = self.P_AUD.open(
                    format=self.FORMAT, 
                    channels=self.CHANNELS, 
                    rate=self.RATE, 
                    input=True, 
                    frames_per_buffer=self.CHUNK,
                    input_device_index=0
                )
            if (self.TYPE == 0):
                stream = self.P_AUD.open(
                    format=self.FORMAT, 
                    channels=self.CHANNELS, 
                    rate=self.RATE, 
                    input=True, 
                    frames_per_buffer=self.CHUNK,
                    input_device_index=1
                )
            if (self.TYPE == 2):
                stream = self.P_AUD.open(
                    format=self.FORMAT, 
                    channels=self.CHANNELS, 
                    rate=self.RATE, 
                    input=True, 
                    frames_per_buffer=self.CHUNK,
                    input_device_index=1
                )
            if (self.TYPE == 3):
                stream = self.P_AUD.open(
                    format=self.FORMAT, 
                    channels=self.CHANNELS, 
                    rate=self.RATE, 
                    input=True, 
                    frames_per_buffer=self.CHUNK,
                    input_device_index=2
                )
            count = count + 1
            print("grabando ...", count)
            data = stream.read(self.CHUNK)
            self.FRAMES.append(data)
            callback_refresh()
            #INICIO VIDEO    
            #img = pyautogui.screenshot()
            #frame = np.array(img)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #out.write(frame)
        stream.close()


        wf = wave.open(url_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.P_AUD.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.FRAMES))
        wf.close()

        self.P_AUD.terminate()
        callback_final()

        #self.combine_audio(url_path2, url_path, "prueba.mkv")

        my_clip = mpe.VideoFileClip(url_path2)
        audio_background = mpe.AudioFileClip(url_path)
        final_clip = my_clip.set_audio(audio_background)
        final_clip.write_videofile(url_path3,fps=25, codec="libx264")

    def demonioVideo(self):
        print("bp4")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")    
        out = cv2.VideoWriter(self.url, fourcc, 20.0, (self.SCREEN_SIZE))
        while self.STATUS == 1:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        out.release()

    def stop_recording(self):
        """ Método para cambiar el estado de grabación a False. """
        self.STATUS = 0

    def type_recording(self, accionmicro, accionaudio):
        #print(accionmicro, "---", accionaudio)
        if(accionaudio==False and accionmicro==False):
            
            self.TYPE=0
        if(accionaudio==True and accionmicro==True):
            self.TYPE=1
        if(accionaudio==False and accionmicro==True):
            self.TYPE=2
        if(accionaudio==True and accionmicro==False):
            self.TYPE=3
        print(accionaudio, " -- ",accionmicro)

    def play_audio(self, url_path):
        """ Método para reproducir audio en una ruta especifica. """
        rf = wave.open(url_path, "rb")

        stream = self.P_AUD.open(
            format=self.P_AUD.get_format_from_width(rf.getsampwidth()),  
            channels=rf.getnchannels(),  
            rate=rf.getframerate(),  
            output=True
        )

        data = rf.readframes(self.CHUNK)
        # Reproducir Audio
        while data:  
            stream.write(data)  
            data = rf.readframes(self.CHUNK)  
  
        stream.stop_stream()  
        stream.close()  
        self.P_AUD.terminate()
    

    def read_audio(self, url_path, language='es-ES'):
        """ Método para leer un audio y devolver el texto. """
        try:
            text = None
            url_path = f"{url_path}".format(url_path=url_path)
            r = sr.Recognizer()
            with sr.AudioFile(url_path) as source:
                audio = r.listen(source)
                text = str(r.recognize_google(audio, language=language))
            
            return text
        except Exception as e:
            return e

