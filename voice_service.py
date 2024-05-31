import os
import sys
import time
import pyttsx3
from pydub import AudioSegment

# Set the path to ffmpeg if it's not found
if sys.platform == "win32":
    AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
else:
    AudioSegment.converter = "/usr/bin/ffmpeg"

class Voice:
    def voiceToText(self, voice_file):
        """
        Convert voice file to text.
        """
        raise NotImplementedError

    def textToVoice(self, text):
        """
        Convert text to voice file.
        """
        raise NotImplementedError


class PyttsVoice(Voice):
    engine = pyttsx3.init()

    def __init__(self):
        self.engine.setProperty("rate", 125)
        self.engine.setProperty("volume", 1.0)
        if sys.platform == "win32":
            for voice in self.engine.getProperty("voices"):
                if "Chinese" in voice.name:
                    self.engine.setProperty("voice", voice.id)
        else:
            self.engine.setProperty("voice", "zh")
            self.engine.startLoop(useDriverLoop=False)

    def textToVoice(self, text):
        try:
            wavFileName = "reply-" + str(int(time.time())) + "-" + str(hash(text) & 0x7FFFFFFF) + ".wav"
            wavFile = os.path.join('tmp', wavFileName)
            os.makedirs(os.path.dirname(wavFile), exist_ok=True)

            self.engine.save_to_file(text, wavFile)

            if sys.platform == "win32":
                self.engine.runAndWait()
            else:
                self.engine.iterate()
                while self.engine.isBusy() or wavFileName not in os.listdir('tmp'):
                    time.sleep(0.1)

            return wavFile
        except Exception as e:
            print(f"Error in textToVoice: {e}")
            return None

    def voiceToText(self, voice_file):
        raise NotImplementedError("voiceToText is not implemented for PyttsVoice")
