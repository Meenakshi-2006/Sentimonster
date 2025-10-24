from flask import Flask, render_template, request, jsonify, session
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Setup
nltk.download('vader_lexicon')
app = Flask(__name__)
app.secret_key = 'sentimonster_secret_key'

# Sentiment analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "🌞  I'm glad you're feeling positive."
    elif score <= -0.05:
        return "🌧️ That sounds a bit down."
    else:
        return "🌤️ That seems neutral."

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input", "")
    response = analyze_sentiment(user_input)

    chat_history = session.get('chat_history', [])
    chat_history.append({'sender': 'user', 'text': user_input})
    chat_history.append({'sender': 'bot', 'text': response})
    session['chat_history'] = chat_history

    return jsonify({'bot': response, 'chat_history': chat_history})


if __name__ == "__main__":
    app.run(debug=True)
