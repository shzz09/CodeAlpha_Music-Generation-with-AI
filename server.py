
import os
import subprocess
import sys
from flask import Flask, jsonify, send_file
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return "MelodyAI Backend is Running!"


@app.route("/api/generate", methods=["POST"])
def generate_music():
    from flask import request

    try:
        data = request.get_json() or {}

        length = data.get("length", "Medium")
        creativity = float(data.get("creativity", 1.0))

        note_counts = {
            "Short": 100,
            "Medium": 300,
            "Long": 500,
            "Extended": 800
        }

        os.environ["MELODYAI_GENERATE_NOTES"] = str(
            note_counts.get(length, 300)
        )
        os.environ["MELODYAI_TEMPERATURE"] = str(creativity)

        subprocess.run(
            [sys.executable, "generate.py"],
            cwd=BASE_DIR,
            check=True
        )

        subprocess.run(
            [sys.executable, "convert_audio.py"],
            cwd=BASE_DIR,
            check=True
        )

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/audio")
def get_audio():
    path = os.path.join(BASE_DIR, "generated_music.wav")

    if not os.path.exists(path):
        return jsonify({"error": "Audio not found"}), 404

    return send_file(path, mimetype="audio/wav")


@app.route("/api/midi")
def get_midi():
    path = os.path.join(BASE_DIR, "generated_music.mid")

    if not os.path.exists(path):
        return jsonify({"error": "MIDI not found"}), 404

    return send_file(path, as_attachment=True,
                     download_name="MelodyAI_Generated.mid")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
