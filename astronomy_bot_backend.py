from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os
app = Flask(__name__, static_folder="static")
CORS(app)


client = Groq(api_key="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")

conversation_history = []

ASTRONOMY_SYSTEM = """
You are an enthusiastic Astronomy Expert Bot! 🌌✨

You love space, stars, planets, galaxies, black holes, moons, comets, rockets and cosmic mysteries.

Rules:
- Be exciting and friendly
- Explain simply
- Use emojis naturally
- Make astronomy fun
- Give accurate answers

"""

@app.route("/")
def home():
    return send_from_directory("static", "astronomy_bot_ui.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "running"})

@app.route("/api/clear", methods=["POST"])
def clear_chat():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "cleared"})

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Empty message"}), 400

        response = client.chat.completions.create(
            model="groq/compound",
            messages=[
                {"role": "system", "content": ASTRONOMY_SYSTEM},
                {"role": "user", "content": message}
            ],
            max_tokens=500
        )

        reply = response.choices[0].message.content

        return jsonify({"response": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, port=5000)
