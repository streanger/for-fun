import os
import re
import time
import contextlib
from pathlib import Path
from io import BytesIO
from string import ascii_letters, digits
from gtts import gTTS

with contextlib.redirect_stdout(None):
    import pygame
try:
    from unidecode import unidecode
except ImportError:
    def unidecode(x):
        return x

"""
requirements:
    pip install pygame gTTS Unidecode  # Unidecode is optional
    
useful:
    import gtts.lang
    langs = gtts.lang.tts_langs()
"""

ALLOWED_CHARACTERS = ascii_letters + digits + " "

def play_sound(sound):
    pygame.mixer.music.load(sound, "mp3")
    pygame.mixer.music.play()


def create_file_name(text):
    """Create file name from text"""
    now = time.strftime("%H%M%S")
    unidecoded_text = "".join(
        [c for c in unidecode(text[:20]) if c in ALLOWED_CHARACTERS]
    )
    unidecoded_text = "-".join(unidecoded_text.split())
    unidecoded_text = re.sub("\-\-+", "-", unidecoded_text)
    name = f"{now}-{unidecoded_text}.mp3"
    return name


def save_voice(text):
    tts = gTTS(text, lang="pl")
    name = create_file_name(text)
    tts.save(name)


def speak(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang="pl")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp


if __name__ == "__main__":
    # path & colors
    os.chdir(str(Path(__file__).parent))
    if os.name == "nt":
        # enable ansi colors
        os.system("")

    # pygame init
    pygame.init()
    pygame.mixer.init()

    # create voice in loop
    while True:
        # user input
        try:
            text = input("\u001b[36mgo:\u001b[0m ")
        except KeyboardInterrupt:
            print()
            continue

        # remove white characters; stop audio if empty
        text = text.strip()
        if not text:
            pygame.mixer.music.stop()
            continue

        # generate and play sound
        save_voice(text)
        sound = speak(text)
        play_sound(sound)
