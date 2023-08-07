import os
from io import BytesIO
import pygame
from gtts import gTTS

"""
requirements:
    pip install pygame gTTS
    
useful:
    import gtts.lang
    langs = gtts.lang.tts_langs()
"""

def play_sound(sound):
    pygame.mixer.music.load(sound, "mp3")
    pygame.mixer.music.play()
    
def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='pl')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp
    
pygame.init()
pygame.mixer.init()
if os.name == 'nt':
    # enable ansi colors
    os.system("")

while True:
    # user input
    try:
        text = input('\u001b[36mgo:\u001b[0m ')
    except KeyboardInterrupt:
        print()
        continue
        
    # remove white characters; stop audio if empty
    text = text.strip()
    if not text:
        pygame.mixer.music.stop()
        continue
        
    # generate and play sound
    sound = speak(text)
    play_sound(sound)
    