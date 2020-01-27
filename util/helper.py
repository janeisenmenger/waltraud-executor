from gtts import gTTS
import playsound
import os
import json

def load_config(filepath="config.json"):
    """ A function that loads the general configuration for the subscribers from the given file

    :type filepath: string
    :param filepath: The path to the configurationf ile

    :rtype: dict
    """
    with open(filepath) as config_file:
        return json.load(config_file)

def play_audio_string(string, language="en"):
    """ A function that relies on the Google Text to Speech service in order to
    produce an mp3 file with the given text. The mp3 file is then played.


    :type string: string
    :param string: The string we want to turn into speech

    :type language: string
    :param language: The language we want to use for the text

    :rtype: void
    """
    tts = gTTS(string, lang=language)
    tts.save('play_sound.mp3')
    
    playsound.playsound('play_sound.mp3', True)
    os.remove('play_sound.mp3')