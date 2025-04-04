from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    intent = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    query = req.get("queryResult", {}).get("queryText", "")

    if intent == "AIResponse":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )
        answer = response.choices[0].message.content
        return jsonify({"fulfillmentText": answer})

    return jsonify({"fulfillmentText": "Intentul nu este recunoscut de webhook."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
