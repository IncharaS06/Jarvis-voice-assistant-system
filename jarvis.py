import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture audio and convert it to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return None

# Function to fetch product information from Flipkart
def fetch_flipkart_data(query):
    url = "https://www.flipkart.com/search"
    params = {'q': query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Parse and extract relevant information
        # This is a very basic extraction; you might need to adjust selectors
        items = soup.find_all('div', class_='_1AtVbE')
        if items:
            for item in items[:5]:  # Limit to 5 results
                title = item.find('a', class_='IRpwTa')
                price = item.find('div', class_='_30jeq3')
                if title and price:
                    print(f"Product: {title.text}, Price: {price.text}")
                    speak(f"Found {title.text} for {price.text}")
        else:
            speak("No results found.")
    else:
        speak("Sorry, I was unable to fetch data from Flipkart.")

def main():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            if 'search' in command.lower():
                # Example command: "search for iPhone"
                query = command.lower().replace('search', '').strip()
                if query:
                    speak(f"Searching for {query} on Flipkart.")
                    fetch_flipkart_data(query)
                else:
                    speak("I didn't catch what you want to search for.")
            elif 'exit' in command.lower():
                speak("Goodbye!")
                break
            else:
                speak("I am not sure how to help with that.")

if _name_ == "_main_":
    main()
