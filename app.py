from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "feedback.db"

# Create table if not exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        if name and message:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO feedback (name, message) VALUES (?, ?)", (name, message))
            return redirect("/")

    with sqlite3.connect(DB_PATH) as conn:
        feedbacks = conn.execute("SELECT name, message FROM feedback ORDER BY id DESC").fetchall()

    return render_template("index.html", feedbacks=feedbacks)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
