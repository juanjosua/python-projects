from pocketsphinx import LiveSpeech
import speech_recognition as sr
import pyttsx3
import requests
import bs4
import pandas as pd


def greetings(hero=None, sentence=None):

    # init function to get an engine instance for the speech synthesis
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    # say method on the engine that passing input text to be spoken
    if hero is None and sentence is None:
        engine.say('Please tell me a hero, sir.')
    elif sentence:
        engine.say(sentence)
    else:
        engine.say('The best item for {} is {}.'.format(hero, sentence))

    # run and wait method, it processes the voice commands.
    engine.runAndWait()


def find_item(hero):
    url = 'https://www.dotabuff.com/heroes/{}/items'.format(hero)

    result = requests.get(url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})
    soup = bs4.BeautifulSoup(result.text, "html.parser")

    table = soup.find_all('table', {'class': 'sortable'})

    # turn the soup into a dataframe
    df = pd.read_html(str(table))[0]

    # rename the columns
    df.columns = ['null', 'item_name', 'match_played', 'win_rate']

    # drop the first column
    df.drop('null', axis='columns', inplace=True)

    # remove % fron the win_rate and change the type to float
    df['win_rate'] = df['win_rate'].str.replace('%', '')
    df['win_rate'] = df['win_rate'].astype(float)

    # data cleaning
    mp_median = df['match_played'].median()
    wr_median = df['win_rate'].median()
    df_new = df.loc[df['match_played'] > mp_median]

    # get the top 10 items based on best match_played and best win_rate
    n = 50
    mp_lrgst = df['match_played'].nlargest(n)
    wr_lrgst = df['win_rate'].nlargest(n)

    top_10 = df.query('match_played in @mp_lrgst & win_rate in @wr_lrgst')
    return(', '.join(top_10["item_name"].values))


def audio_query():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Speak Anything : ')
        greetings()
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)

            hero = text.strip().replace(' ', '-').lower()
            print('You said : {}'.format(hero))

            items = find_item(hero)
            print(items)
            greetings(hero, items)

        except:
            # print('Sorry could not recognize your voice')
            greetings(sentence='Sorry could not recognize your voice sir!')
        
        finally:
            print('========================================')


speech = LiveSpeech(lm=False, keyphrase='friday')
for phrase in speech:
    audio_query()
