from gtts import gTTS
import os
import webbrowser
import datetime
import wikipedia
from tkinter import *
from PIL import ImageTk, Image
import pyaudio
from pvporcupine import create as pv_create
from pvporcupine import PorcupineRuntimeError
from requests import get
import speech_recognition as sr

class VirtualAssistant:
    def __init__(self):
        self.wake_word_detector = self.initialize_porcupine()
        self.init_gui()

    def initialize_porcupine(self):
        access_key = "rlt+uh4CzuP2xM95neZZAQZv7tdlZG22KG0XcYpC7oQn/B53WjvtRw=="
        wake_word_model_path = "/Users/adi/Desktop/VIRTUAL ASSITANT/Dynam_en_mac_v3_0_0.ppn"
        try:
            handle = pv_create(keyword_paths={"Dynam": wake_word_model_path},library_path='libpv_porcupine.dylib',access_key=access_key)
            return handle
        except PorcupineRuntimeError as e:
            print(f"Failed to initialize Porcupine: {str(e)}")
            return None

    def init_gui(self):
        self.root = Tk()
        self.root.title('DYNUM')
        self.root.geometry('1280x720')
        img = ImageTk.PhotoImage(Image.open('DYNUM.webp'))
        panel = Label(self.root, image=img)
        panel.pack(side='right', fill='both', expand='no')

        self.compText = StringVar()
        self.userText = StringVar()

        self.userText.set('Your Virtual Assistant')
        userFrame = LabelFrame(self.root, text='DYNUM', font=('Railways', 24, 'bold'))
        userFrame.pack(fill='both', expand='Yes')

        top = Message(userFrame, textvariable=self.userText, bg='black', fg='white')
        top.config(font=("Century Gothic", 15, 'bold'))
        top.pack(side='top', fill='both', expand='yes')

        btn = Button(self.root, text="SPEAK", font=('railways', 10, 'bold'),bg='red', fg='black', command=self.clicked)
        btn.pack(fill='x', expand='no')
        btn2 = Button(self.root, text='Close', font=('railways', 10, 'bold'),bg='yellow', fg='black', command=self.root.destroy)
        btn2.pack(fill='x', expand='no')
        self.speak('How can I assist you?')
        self.root.mainloop()

    def speak(self, text):
        output=gTTS(text=text, lang='en', slow=False)
        output.save("dynum.mp3")
        os.system("afplay dynum.mp3")
        os.remove("dynum.mp3")

    def listen(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 3

        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Listening for wake word...")
        frames = []

        try:
            while True:
                data = stream.read(CHUNK)
                pcm = list(data)
                result = self.wake_word_detector.process(pcm)
                if result:
                    print("Wake word detected!")
                    self.speak("How can I assist you?")
                    self.process_command()
                    break
        except KeyboardInterrupt:
            pass

        print("Stopped listening for wake word.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

    def process_command(self):
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with mic as mic:
            print("Listening...")
            rec.adjust_for_ambient_noise(mic)
            rec.energy_threshold = 400
            audio = rec.listen(mic, timeout=5)
        try:
            print("Recognizing...")
            command = rec.recognize_google(audio)
            print('You said: {}'.format(command))
            self.process_command(command)
        except sr.UnknownValueError:
            print('Could not understand the audio')
        except sr.RequestError:
            print('Could not request results; check your internet connection')

    def process_command(self, command):
        if 'hello' in command:
            self.speak("Hello sir")
        elif 'goodbye' in command:
            self.speak("Goodbye")
            exit()
        elif 'open safari' in command or 'open web browser' in command:
            self.open_website("https://www.apple.com/safari/")
        elif 'ip address' in command:
            ip = get('https://api.ipify.org').text
            self.speak(f"Your IP address is {ip}")
        elif 'search the web for' in command:
            search_query = command.replace("search the web for", "")
            self.open_website(f"https://www.google.com/search?q={search_query}")
            print(f"Searching the web for: {search_query}")
        elif 'wikipedia' in command:
            self.search_wikipedia(command)
        elif 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        elif 'shutdown' in command:
            self.shutdown_or_restart_mac("shutdown")
        elif 'restart' in command:
            self.shutdown_or_restart_mac("restart")

    def open_website(self, website_url):
        webbrowser.open(website_url)
        self.speak(f"Opening {website_url.split('//')[1]}.")

    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def get_date(self):
        current_date = datetime.date.today().strftime("%B %d, %Y")
        self.speak(f"Today's date is {current_date}")

    def shutdown_or_restart_mac(self, action):
        os.system(f"osascript -e 'tell app \"System Events\" to {action}'")
        self.speak(f"{action.capitalize()}ing...")

    def search_wikipedia(self, command):
        keyword = "wikipedia"
        if keyword in command:
            self.speak("Searching Wikipedia...")
            search_wik = command.split(keyword, 1)[-1].strip()
            try:
                print(search_wik)
                result = wikipedia.summary(search_wik, sentences=2)
                print(result)
                self.speak(result)
            except wikipedia.DisambiguationError:
                self.speak("Multiple results found. Can you be more specific?")
            except wikipedia.PageError:
                self.speak(f"Sorry, I couldn't find information on '{search_wik}'.")
            except Exception as e:
                self.speak(f"An error occurred while searching Wikipedia. {e}")

    def clicked(self):
        print("Working...")
        self.listen()

if __name__== '__main__':
    assistant = VirtualAssistant()