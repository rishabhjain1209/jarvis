import streamlit as st
import pyttsx3
import speech_recognition as sr
import time
import requests
import wikipedia
import webbrowser
from bs4 import BeautifulSoup
import pyjokes
import random
from googletrans import Translator
import json
from streamlit_lottie import st_lottie


st.set_page_config(page_title="Jarvis", page_icon="🤖",initial_sidebar_state="collapsed")


def listen_and_process():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.7)
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        engine.runAndWait()
        user_input = user_input.lower()
        st.write("You said:", user_input)
        engine.say("You said: " + user_input)
        engine.runAndWait()
        


        if "weather" in user_input:
            try:
                keywords = ["in", "for", "weather", "of"]
                words = user_input.split()
                city = ""
                for i, word in enumerate(words):
                    if word.lower() not in keywords:
                        city += word + " "

                city = city.strip()

                We_API = "5347a180a441d5577a5494b4f8258837"
                response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={We_API}')

                if response.status_code == 200:
                    data = response.json()
                    description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']

                    weather_info = f"The weather in {city} is {description}."
                    temperature_info = f"The temperature is {temperature}fahrenheit."
                    humidity_info = f"The humidity is {humidity}%."
                    wind_info = f"The wind speed is {wind_speed} m/s."
                    st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                    st.write(weather_info)
                    st.write(temperature_info)
                    st.write(humidity_info)
                    st.write(wind_info)
                    engine.say(weather_info)
                    engine.say(temperature_info)
                    engine.say(humidity_info)
                    engine.say(wind_info)
                    engine.runAndWait()
                else:
                    engine.say("Sorry, I couldn't fetch weather information for that city.")
                    engine.runAndWait()
            except Exception as e:
                engine.say(f"An error occurred: {str(e)}")
                engine.runAndWait()

        elif "timer" in user_input:
            words = user_input.split()
            duration = None
            for i, word in enumerate(words):
                if word.isdigit():
                    duration = int(word)
                    break
            if duration is not None and duration > 0:
                st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                st.write(f"Timer set for {duration} seconds.")
                engine.say(f"Timer set for {duration} seconds.")
                engine.runAndWait()
                time.sleep(duration) 
                engine.say("Timer EXPIREDD!")
                engine.runAndWait()
            else:
                engine.say("Please specify a valid duration for the timer.")
                engine.runAndWait()

        elif "news" in user_input:
            try:
                news_api = "d7abb948a26b4e9d853383cc5e1b9656"
                response = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={news_api}&country=in')

                if response.status_code == 200:
                    data = response.json()
                    articles = data['articles']
                    engine.say("Here are the top headlines for India:")
                    engine.runAndWait()

                    for i, article in enumerate(articles):
                        title = article['title']
                        engine.say(f"{i + 1}. {title}")
                        engine.runAndWait()
                        if st.button("Stop"):
                            engine.stop
                else:
                    engine.say("Sorry, I couldn't fetch news headlines for India at the moment.")
                    engine.runAndWait()
            except Exception as e:
                engine.say(f"An error occurred: {str(e)}")
                engine.runAndWait()

        elif "translate" in user_input:
            words = user_input.split()
            text_to_translate = ""
            target_language = "en"

            for i, word in enumerate(words):
                if word == "translate":
                    text_to_translate = " ".join(words[i + 1:])
                    if i + 2 < len(words) and len(words[i + 2]) == 2:
                        target_language = words[i + 2]
                    break

            if text_to_translate and text_to_translate.strip():
                try:
                    translator = Translator()
                    translation = translator.translate(text_to_translate, src='auto', dest=target_language)
                    st.markdown('''</br><h3>🤖 Response : </h3>''', unsafe_allow_html=True)
                    st.write(f"Translation to English: {translation.text}")
                    engine.say(f"Translation to English: {translation.text}")
                    engine.runAndWait()
                except Exception as e:
                    st.write(f"Translation error: {str(e)}")
                    engine.say(f"Translation error: {str(e)}")
                    engine.runAndWait()
            else:
                st.write("Please provide the text you want to translate and the target language.")
                engine.say("Please provide the text you want to translate and the target language.")
                engine.runAndWait()


        elif "wikipedia" in user_input:
            query = user_input.replace("wikipedia", "").strip()
            if query:
                try:
                    result = wikipedia.summary(query, sentences=4)  
                    st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                    #st.write("Wikipedia Summary:")
                    st.write(result)
                    engine.say(result)
                    engine.runAndWait()
                    # Display the Wikipedia summary in Streamlit
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    options = e.options[:5]  
                    engine.say(f"Multiple options found. Here are some suggestions: {', '.join(options)}")
                    engine.runAndWait()
                except wikipedia.exceptions.PageError:
                    engine.say("Sorry, I couldn't find any matching Wikipedia article.")
                    engine.runAndWait()
                except Exception as e:
                    engine.say(f"An error occurred while searching Wikipedia: {str(e)}")
                    engine.runAndWait()
            else:
                engine.say("Please specify a query for Wikipedia search.")
                engine.runAndWait()
                st.write("Please specify a query for Wikipedia search.")

        elif "google" in user_input:
            query = user_input.replace("google", "").strip()
            try:
                search_url = f"https://www.google.com/search?q={query}"
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
                webbrowser.get('chrome').open(search_url)
                webbrowser.open(search_url)
                st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                st.write(f"Opened {query}")
            except Exception as e:
                engine.say(f"An error occurred while performing a Google search: {str(e)}")
                engine.runAndWait()
                st.write(f"An error occurred while performing a Google search: {str(e)}")

        elif "joke" in user_input:
            try:
                joke = pyjokes.get_joke()
                st.write(joke)
                engine.say(joke)
                engine.runAndWait()
                #st.write("Here's a joke:")
                st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                
            except Exception as e:
                engine.say(f"An error occurred while fetching a joke: {str(e)}")
                engine.runAndWait()
                st.write(f"An error occurred while fetching a joke: {str(e)}")

        elif "riddle" in user_input:
            try:
                riddles = [
                    "What has keys but can't open locks?",
                    "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? (Answer: An Echo)",
                    "I'm tall when I'm young, and I'm short when I'm old. What am I? (Answer: A Candle)",
                    "I speak without a mouth and hear without ears. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "What comes once in a minute, twice in a moment, but never in a thousand years?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "What has keys but can't open locks?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "I can fly without wings, cry without eyes, and wherever I go, darkness follows me. What am I?",
                    "What has a heart that doesn't beat?",
                    "I'm found in the middle of America, but I'm not a state. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm a word of letters three, add two and fewer there will be. What am I?",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "I'm found in the middle of America, but I'm not a state. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm a word of letters three, add two and fewer there will be. What am I?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "I'm found in the middle of America, but I'm not a state. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm a word of letters three, add two and fewer there will be. What am I?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "I'm found in the middle of America, but I'm not a state. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm a word of letters three, add two and fewer there will be. What am I?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
                    "I'm found in the middle of America, but I'm not a state. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red. What am I?",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside. What am I?",
                    "I'm a word of letters three, add two and fewer there will be. What am I?",
                    "I'm tall when I'm young and short when I'm old. What am I?",
                    "The more you take, the more you leave behind. What am I?",
                    "I have cities but no houses, forests but no trees, and rivers but no water. What am I?",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me.",
                    "I'm found in the middle of America, but I'm not a state.",
                    "The more you take, the more you leave behind.",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside.",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red.",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside.",
                    "I'm a word of letters three, add two and fewer there will be.",
                    "I'm tall when I'm young and short when I'm old.",
                    "The more you take, the more you leave behind.",
                    "I have cities but no houses, forests but no trees, and rivers but no water.",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me.",
                    "I'm found in the middle of America, but I'm not a state.",
                    "The more you take, the more you leave behind.",
                    "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside.",
                    "I'm always hungry, I must always be fed. The finger I touch, will soon turn red.",
                    "I have keys but can't open locks. I have space but no room. You can enter, but you can't go inside.",
                    "I'm a word of letters three, add two and fewer there will be.",
                    "I'm tall when I'm young and short when I'm old.",
                    "The more you take, the more you leave behind.",
                    "I have cities but no houses, forests but no trees, and rivers but no water.",
                    "What has keys but can't open locks?",
                    "I'm not alive, but I can grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me."
                ]
                riddle = random.choice(riddles)
                st.markdown('''</br><h3>🤖 Response : </h3>''',unsafe_allow_html=True)
                st.write(riddle)
                engine.say("Here's a riddle:")
                engine.say(riddle)
                engine.runAndWait()
            except Exception as e:
                engine.say(f"An error occurred while fetching a riddle: {str(e)}")
                engine.runAndWait()
                st.write(f"An error occurred while fetching a riddle: {str(e)}")

        elif "horoscope" in user_input:
            def get_horoscope(query):
                try:
                    url = f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={query}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        horoscope = soup.find('div', class_='main-horoscope').p.get_text()
                        return horoscope
                    else:
                        return f"Unable to fetch the horoscope at the moment. Status Code: {response.status_code}"
                except Exception as e:
                    return f"An error occurred while fetching the horoscope: {str(e)}"
            zodiac_sign = user_input.split()[-1].lower()
            if zodiac_sign == "aries":
                query=1
            elif zodiac_sign == "taurus":
                query=2
            elif zodiac_sign == "gemini":
                query=3
            elif zodiac_sign == "cancer":
                query=4
            elif zodiac_sign == "leo":
                query=5
            elif zodiac_sign == "virgo":
                query=6
            elif zodiac_sign == "libra":
                query=7
            elif zodiac_sign == "scorpio":
                query=8
            elif zodiac_sign == "sagittarius":
                query=9
            elif zodiac_sign == "capricorn":
                query=10
            elif zodiac_sign == "aquarius":
                query=11
            elif zodiac_sign == "pisces":
                query=12
            else:
                st.write("Invalid zodiac sign. Please enter a valid zodiac sign.")
                engine.say("Invalid zodiac sign. Please enter a valid zodiac sign.")
            try:
                horoscope = get_horoscope(query)
                st.write(f"Horoscope for '{zodiac_sign}':")
                st.write(horoscope)
                engine.say(f"Horoscope for '{zodiac_sign}':")
                engine.say(horoscope)
                engine.runAndWait()
            except Exception as e:
                print(f"An error occurred while fetching the horoscope: {str(e)}")
            

        elif "trivia" in user_input:
                def get_random_trivia_question():
                    try:
                        url = "https://opentdb.com/api.php"
                        params = {
                            "amount": 1,        
                            "type": "multiple",  
                        }

                        response = requests.get(url, params=params)
                        if response.status_code == 200:
                            data = json.loads(response.text)
                            if data["results"]:
                                question_data = data["results"][0]
                                question = question_data["question"]
                                correct_answer = question_data["correct_answer"]
                                incorrect_answers = question_data["incorrect_answers"]
                                return question, correct_answer, incorrect_answers
                            else:
                                return None, None, None
                        else:
                            return None, None, None
                    except Exception as e:
                        print("An error occurred while fetching trivia question:", str(e))
                        return None, None, None
                try:
                    question, correct_answer, incorrect_answers = get_random_trivia_question()

                    if question and correct_answer and incorrect_answers:
                        st.write(question)
                        engine.say(question)
                        engine.runAndWait()
                        options = [correct_answer] + incorrect_answers
                        random_options = sorted(options, key=lambda x: random.random())

                        st.write("Options:")
                        for i, option in enumerate(random_options, start=1):
                            st.write(f"Option {i}: {option}")

                        for i, option in enumerate(random_options, start=1):
                            engine.say(f"Option {i}. {option}")
                            engine.runAndWait()
                        time.sleep(5)
                        engine.say(f"the correct answer is{correct_answer}")
                        engine.runAndWait()

                    else:
                        engine.say("Sorry, unable to fetch a trivia question.")
                        engine.runAndWait()
                        st.write("Sorry, unable to fetch a trivia question.")
                except Exception as e:
                    engine.say(f"An error occurred while fetching a trivia question: {str(e)}")
                    engine.runAndWait()
                    st.write(f"An error occurred while fetching a trivia question: {str(e)}")

        elif "fitness" in user_input or "exercise" in user_input:
            exercises = [
                "Push-ups",
                "Sit-ups",
                "Jumping jacks",
                "Planks",
                "Squats",
                "Lunges",
                "Yoga stretches",
                "Burpees",
                "Mountain climbers",
                "Bicycle crunches",
                "Dumbbell curls",
                "Leg raises",
                "Jump rope",
            ]
            def provide_fitness_info():
                response = """Sure, here's some fitness information for you :
                """
                response += "Exercise of the day: " + random.choice(exercises) + "\n"
                return response
            fit = provide_fitness_info()
            st.write(fit)
            engine.say(fit)
            engine.runAndWait()

        elif "nutrition" in user_input or "health" in user_input:
            nutrition_tips = [
                "Drink plenty of water throughout the day to stay hydrated.",
                "Include a variety of fruits and vegetables in your diet for balanced nutrition.",
                "Limit the consumption of sugary and processed foods.",
                "Aim for a balanced mix of carbohydrates, proteins, and healthy fats in your meals.",
                "Consider portion control to avoid overeating.",
                "Try to incorporate lean proteins like chicken, fish, and tofu into your diet.",
                "Don't skip breakfast; it's an essential meal to kickstart your day.",
                "Choose whole grains over refined grains for better fiber and nutrients.",
            ]

            def provide_nutrition_tip():
                response = "Here's a nutrition tip for you:\n"
                response += random.choice(nutrition_tips) + "\n"
                return response
            hth = provide_nutrition_tip()
            st.write(hth)
            engine.say(hth)
            engine.runAndWait()

        elif "emergency" in user_input:
            emergency_numbers = {
                "police": "100",  # India police emergency number
                "fire": "101",    # India fire emergency number
                "medical": "102",  # India medical emergency number
                "ambulance": "102",  # India ambulance emergency number
                "poison control": "108",  # India poison control number
                "roadside assistance": "103",  # India roadside assistance number
                "coast guard": "104",  # India coast guard emergency number
                "disaster management": "108",  # India disaster management number
                "women's helpline": "1091",  # India women's helpline number
                "child helpline": "1098",  # India child helpline number
                "elderly helpline": "14567",  # India elderly helpline number
                "mental health helpline": "1551",  # India mental health helpline number
                "forest fire control": "1926",  # India forest fire control number
                "railway police": "182",  # India railway police emergency number
                "animal rescue": "1962",  # India animal rescue number
                "electricity emergency": "1912",  # India electricity emergency number
                "gas leak emergency": "1906",  # India gas leak emergency number
                "plumbing emergency": "1916",  # India plumbing emergency number
                "disaster helpline": "1078",  # India disaster helpline number
                "mountain rescue": "1950",  # India mountain rescue number
                "helicopter rescue": "1943",  # India helicopter rescue number
            }

            # Split user_input into words and check each word
            words_in_input = user_input.split()
            found_emergency_type = None
            
            for word in words_in_input:
                if word in emergency_numbers:
                    found_emergency_type = word
                    break

            if found_emergency_type:
                engine.say(f"Call {emergency_numbers[found_emergency_type]} for {found_emergency_type} assistance.")
                engine.runAndWait()
            else:
                engine.say("Sorry, we don't have the contact number for that emergency type.")
                engine.runAndWait()

        else:
            response = "I couldn't recognize that command."
            engine.say(response)

    except sr.UnknownValueError:
        engine.say("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        engine.say(f"Could not request results; {e}")

def main():
    st.markdown(
            """
            <style>
            .centered {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                margin: 0;
                padding: 0; 
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
    """
    <div style="text-align: center;">
        <h1>JARVIS</h1>
        <p>Your friendly AI assistant!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

    def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

    lottie_robot = load_lottieurl("https://lottie.host/c82f90fa-8990-4fb6-a4bb-f71374cdd8c7/BG9Ahjn5IG.json")
    st_lottie(lottie_robot, height=300, key="student", quality="high")

    if st.button("Please Speak"):
        listen_and_process()



if __name__ == '__main__':
    main()
