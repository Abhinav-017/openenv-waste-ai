import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from env.waste_env import WasteEnv

app = Flask(__name__)
env = WasteEnv()

@app.route("/")
def home():
    return "OpenEnv Waste AI is running"

@app.route("/reset", methods=["POST"])
def reset():
    return jsonify(env.reset())

@app.route("/step", methods=["POST"])
def step():
    data = request.json
    action = data.get("action", 1)
    state, reward, done, _ = env.step(action)

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done
    })

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()