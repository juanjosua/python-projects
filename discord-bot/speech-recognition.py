import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak Anything : ')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        if 'hey jarvis' in text.lower():
            print('hey, how are you doing?')
        else:
            print('You said : {}'.format(text))
    except:
        print('Sorry could not recognize your voice')
