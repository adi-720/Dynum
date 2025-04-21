from gtts import gTTS
import os
import speech_recognition as sr
import webbrowser
import requests
from requests import get
import datetime
import wikipedia
from tkinter import *
from PIL import ImageTk, Image

class VirtualAssistant:
    def __init__(self):
        self.init_gui()

    def init_gui(self):
        self.root = Tk()
        self.root.title('DYNUM')
        self.root.geometry('1280x720')
        img = ImageTk.PhotoImage(Image.open('DYNUM.webp'))
        panel = Label(self.root, image=img)
        panel.pack(side='right', fill='both', expand='no')

        self.compText = StringVar()
        self.userText = StringVar()

        self.userText.set('Hey I am Dynum')
        userFrame = LabelFrame(self.root, text='DYNUM', font=('Railways', 40, 'bold'))
        userFrame.pack(fill='both', expand='Yes')

        top = Message(userFrame, textvariable=self.userText, bg='black', fg='white')
        top.config(font=("Century Gothic", 55, 'bold'))
        top.pack(side='top', fill='both', expand='yes')

        btn = Button(self.root, text="SPEAK", font=('railways', 20, 'bold'),bg='red', fg='black', command=self.clicked)
        btn.pack(fill='x', expand='no')
        btn2 = Button(self.root, text='Close', font=('railways', 20, 'bold'),bg='yellow', fg='black', command=self.root.destroy)
        btn2.pack(fill='x', expand='no')
        self.speak('How can I assist you?')
        self.root.mainloop()

    def speak(self, text):
        if isinstance(text, list):
            text = ' '.join(text)
        output=gTTS(text=text, lang='en', slow=False)
        output.save("dynum.mp3")
        os.system("afplay dynum.mp3")
        os.remove("dynum.mp3")

    def listen(self):
        rec = sr.Recognizer()
        mic = sr.Microphone()
        with mic as mic:
            print("Listening...")
            rec.adjust_for_ambient_noise(mic)
            rec.energy_threshold = 100
            audio = rec.listen(mic, timeout=5)
        try:
            print("Recognizing...")
            command = rec.recognize_google(audio)
            print('You said: {}'.format(command))
            self.process_command(command)
        except sr.UnknownValueError:
            self.userText.set('Could not understand the audio')
            print('Could not understand the audio')
        except sr.RequestError:
            self.userText.set('Could not request results; check your internet connection')
            print('Could not request results; check your internet connection')

    def process_command(self, command):
        if 'hello' in command:
            self.speak("Hello sir")
        elif 'goodbye' in command:
            self.speak("Goodbye")
            exit()
        elif 'open safari' in command:
            self.open_website("https://www.google.com/")
        elif 'ip address' in command:
            ip = get('https://api.ipify.org').text
            self.speak(f"Your IP address is {ip}")
        elif 'search the web for' in command:
            search_query = command.replace("search the web for", "")
            self.open_website(f"https://www.google.com/search?q={search_query}")
            print(f"Searching the web for: {search_query}")
        elif 'wikipedia' in command:
            self.search_wikipedia(command)
        elif 'news' in command:
            self.speak(f"I'm reading out the latest news headlines, sir")
            self.speak(self.get_latest_news())
        elif 'time' in command:
            self.get_time()
        elif 'date' in command:
            self.get_date()
        elif 'shutdown' in command:
            self.shutdown_or_restart_mac("shutdown")
        elif 'restart' in command:
            self.shutdown_or_restart_mac("restart")

    def get_latest_news(self):
        NEWS_API_KEY = ("f3551ee1058b45f6a4eaefd833b715de")
        news_headlines = []
        res = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
        articles = res["articles"]
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:5]

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