from flask import Flask, request, jsonify, send_from_directory
import os
import whisper
from io import BytesIO
from flask_cors import CORS
from voice_service import PyttsVoice
from chat import spark_completion

app = Flask(__name__, static_folder="static")
CORS(app)  # 允许跨域

model = whisper.load_model("base")
voice_service = PyttsVoice()


@app.route("/process_audio", methods=["POST"])
def process_audio():
    audio_file = request.files["audio"]
    audio_path = os.path.join("uploads", "input_audio.wav")
    audio_file.save(audio_path)

    result = model.transcribe(audio_path)
    user_text = result["text"]

    messages = [{"role": "user", "content": user_text}]
    llm_response = spark_completion(messages)
    reply_text = llm_response.generations[0][0].text

    wav_file_path = voice_service.textToVoice(reply_text)

    if wav_file_path:
        with open(wav_file_path, "rb") as f:
            audio_data = f.read()
        return jsonify(
            {
                "transcript": user_text,
                "reply": reply_text,
                "audio": audio_data.hex(),  # 转换音频数据为十六进制字符串
            }
        )
    else:
        return jsonify({"error": "Error generating voice response"}), 500


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(host="0.0.0.0", port=6123, debug=True)
