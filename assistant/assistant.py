import speech_recognition as sr
import ctypes
from ctypes import *
import pyttsx3
import sys

class Assistant:
    recognizer = None
    selected_device = None
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    def __init__(self):
        self.recognizer = sr.Recognizer()
        pass
    
    def startAssistant(self):
        if self.selected_device == None:
            self.selectMic()
            self.captureCommands()
        else:
            self.captureCommands()
        pass
    def captureCommands(self):
        with sr.Microphone(device_index=self.selected_device) as source:
            print('Say something...')
            self.speak('Say something...')
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                cmd=self.recognizer.recognize_google(audio)
                self.handleCommands(cmd)                
                
                self.captureCommands()
                # handle the exceptions
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                self.captureCommands()
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                self.captureCommands()
        pass
    def handleCommands(self, command):
        self.speak('Did you say '+command+'?')
        if command == 'lock my computer':
            ctypes.windll.user32.LockWorkStation()
        if command == 'close the app':
            sys.exit()
        pass
    def selectMic(self):
        mics = sr.Microphone.list_microphone_names()
        message = 'Seleccione un dispositivo a utilizar: \n\n'

        for i in range(len(mics)):
            if self.checkIsMicAvailable(mics[i]):
                message += str(i)+ ' - ' +mics[i]+'\n'
            
        op = int(input(message))

        self.selected_device = op

        


        pass
    def speak(self,audio):
        self.engine.say(audio)
        self.engine.runAndWait()
    def checkIsMicAvailable(self,mic):
        winmm = windll.LoadLibrary('winmm.dll')
        widn = winmm.waveInGetDevCapsA
        widn.restype = c_uint
        waveNum = winmm.waveInGetNumDevs 
        s = create_string_buffer(b'\000' * 32)
        
        class LPWAVEINCAPS(Structure):
            _fields_ = [
            ("wMid",c_ushort),
            ("wPid",c_ushort),
            ("vDriverVersion",c_uint),
            ("szPname", type(s)),
            ("dwFormats",c_uint),
            ("wChannels",c_ushort), 
            ("wReserved1",c_ushort),
            ]

        widn.argtypes = [
            c_uint,
            POINTER(LPWAVEINCAPS),
            c_uint
            ]
        structLP = LPWAVEINCAPS()

        

        for i in range(waveNum()):
            widn(c_uint(i),byref(structLP),sizeof(structLP))
            name = structLP.szPname.decode('latin-1')

            if name == mic:
                return True
        waveNum.restype = c_uint
        return False
        pass
    