from flask import Flask, request, jsonify
from env.waste_env import WasteEnv

app = Flask(__name__)

env = WasteEnv()

@app.route("/reset", methods=["POST"])
def reset():
    state = env.reset()
    return jsonify(state)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)