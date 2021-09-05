from pocketsphinx import LiveSpeech
import pyttsx3

# keyphrase to listen
speech = LiveSpeech(lm=False, keyphrase='hello')

# init function to get an engine instance for the speech synthesis
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


for phrase in speech:
    print(phrase.segments(detailed=True))

    # say method on the engine that passing input text to be spoken
    engine.say('Hello sir, how may I help you?')

    # run and wait method, it processes the voice commands.
    engine.runAndWait()
