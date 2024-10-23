from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/agent', methods=['POST'])
def interact_with_agent():
    # This is a stub for interacting with the agent.
    # Extract data from request
    data = request.json

    # Stub response until agent interaction is implemented
    response = {
        "message": "This is a stub for agent interaction."
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
