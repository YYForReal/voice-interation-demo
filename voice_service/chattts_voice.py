import os
import time
import torch
import ChatTTS
import numpy as np
from scipy.io.wavfile import write as wav_write
from .voice import Voice
import torchaudio
import soundfile


class ChatTTSVoice(Voice):
    def __init__(self):
        self.chat = ChatTTS.Chat()
        self.chat.load_models(compile=False)

    def textToVoice(self, text):
        try:
            wavFileName = (
                "reply-"
                + str(int(time.time()))
                + "-"
                + str(hash(text) & 0x7FFFFFFF)
                + ".wav"
            )
            wavFile = os.path.join("tmp", wavFileName)
            os.makedirs(os.path.dirname(wavFile), exist_ok=True)

            # ChatTTS 的 infer 方法
            wavs = self.chat.infer([text])
            wav_data = wavs[0]
            print(f"wav_data: {wav_data}")
            print("ready to write in wav file", wavFile)

            soundfile.write(wavFile, wavs[0][0], 24000)
            # torchaudio.save(wavFile, torch.from_numpy(wav_data), 24000)

            # # 将音频数据限制在 float32 的范围内并转换为 int16 格式
            # wav_data_clipped = np.clip(wav_data, -1.0, 1.0)
            # wav_data_int16 = np.int16(wav_data_clipped * 32767)

            # # 使用 scipy.io.wavfile 写入 WAV 文件
            # wav_write(wavFile, 24000, wav_data_int16)

            return wavFile
        except Exception as e:
            print(f"Error in textToVoice: {e}")
            return None

    def voiceToText(self, voice_file):
        raise NotImplementedError("voiceToText is not implemented for ChatTTSVoice")


def main():
    text = "你好，这是一个测试文本。"
    chat_tts_voice = ChatTTSVoice()
    wav_file = chat_tts_voice.textToVoice(text)

    if wav_file and os.path.exists(wav_file):
        print(f"语音文件已生成: {wav_file}")
    else:
        print("语音文件生成失败")


if __name__ == "__main__":
    main()
