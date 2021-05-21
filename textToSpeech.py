from gtts import gTTS
import pygame 

pygame.mixer.init()
# pygame.init()

# text = 'Hi Jash. This is the conversion code woman speaking.'

def tts(text):
    language = 'en'
    audioObj = gTTS(text=text,lang=language,slow=False)
    audioObj.save('trialAudio.mp3')
    # playsound('trialAudio.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("trialAudio.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    # pygame.mixer.music.load("trialAudio.mp3")
    # pygame.mixer.music.play()
    # time.sleep(3)
    # pygame.mixer.music.stop()
# tts(text)