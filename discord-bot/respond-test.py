import speech_recognition as sr
import pyttsx3

# init recognizer engine
r = sr.Recognizer()

# init function to get an engine instance for the speech synthesis
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

with sr.Microphone() as source:
    print('Speak Anything : ')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if 'hey jarvis' in text.lower():
            # say method on the engine that passing input text to be spoken
            engine.say('Hello sir, how may I help you?')
            # run and wait method, it processes the voice commands.
            engine.runAndWait()
        else:
            print('You said : {}'.format(text))
            
    except:
        print('Sorry could not recognize your voice')

