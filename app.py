from flask import Flask, render_template, request
from textblob import TextBlob
import sqlite3

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sentiments (id INTEGER PRIMARY KEY, text TEXT, sentiment TEXT)''')
    conn.commit()
    conn.close()

# Function to analyze sentiment

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.5:
        return "Very Positive 😊🔥🎉"
    elif polarity > 0:
        return "Positive 🙂👍"
    elif polarity < -0.5:
        return "Very Negative 😡💀👎"
    elif polarity < 0:
        return "Negative 😞😔"
    else:
        return "Neutral 😐"



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        sentiment = analyze_sentiment(text)

        # Save to Database
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO sentiments (text, sentiment) VALUES (?, ?)", (text, sentiment))
        conn.commit()
        conn.close()

        return render_template("result.html", text=text, sentiment=sentiment)

    return render_template("index.html")

@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM sentiments ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return render_template("history.html", data=data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
