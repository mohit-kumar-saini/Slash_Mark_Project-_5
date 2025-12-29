import speech_recognition as sr
import pyttsx3
import datetime
import time

engine = pyttsx3.init()
engine.setProperty('rate', 160)

def respond(text):
   
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=4,
                phrase_time_limit=4
            )
        except sr.WaitTimeoutError:
            return None

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print("User said:", command)
        return command.lower()

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        respond("Speech recognition service is unavailable.")
        return None


def process_command(command):
    print(f"process_command received: {command}")
    if "hello" in command or "hi" in command:
        print("Matched: greeting")
        respond("Hello! How can I assist you?")

    elif "name" in command:
        print("Matched: name")
        respond("I am a voice assistant developed during an internship.")

    elif "time" in command:
        print("Matched: time")
        current_time = datetime.datetime.now().strftime("%H:%M")
        respond(f"The current time is {current_time}")

    elif "exit" in command or "stop" in command or "quit" in command:
        print("Matched: exit")
        respond("Thank you. Have a nice day.")
        return False

    else:
        print("No matching command found")
        respond("Sorry, I did not understand the command. You can say 'hello', 'time', 'name', or 'exit'.")

    return True


def main():
    respond("Voice assistant started. Please say a command.")

    silent_attempts = 0
    MAX_SILENT_ATTEMPTS = 5

    while True:
        command = take_command()

        if command is None:
            silent_attempts += 1
            time.sleep(1)
            if silent_attempts >= MAX_SILENT_ATTEMPTS:
                respond("No input detected. Assistant is stopping.")
                break
            continue

        silent_attempts = 0

        print(f"Processing command: {command}")
        result = process_command(command)
        print(f"process_command returned: {result}")
        if not result:
            break


if __name__ == "__main__":
    main()
