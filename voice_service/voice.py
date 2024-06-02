import os
import json


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


def get_voice_service():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            tts_service = config.get("TTS_SERVICE", "pytts")
            if tts_service == "chattts":
                from .chattts_voice import ChatTTSVoice

                return ChatTTSVoice()
            else:
                from .pytts_voice import PyttsVoice

                return PyttsVoice()
    except FileNotFoundError:
        raise Exception("配置文件 config.json 未找到，请确保文件存在并正确配置。")
