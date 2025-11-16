from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
DB_PATH = os.path.join("database", "feedback.db")
os.makedirs("database", exist_ok=True)

# Sample backup feedback
backup_feedback = [
    ("user1", "User1's first feedback"),
    ("user2", "User2's feedback"),
    ("user3", "User3 says hello"),
    ("user1", "User1's second feedback")
]

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO feedback (username, message) VALUES (?, ?)",
                backup_feedback
            )
            conn.commit()

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        uid = request.form.get("uid")
        password = request.form.get("password")

        # Admin login
        if uid == "admin" and password == "admin":
            session["role"] = "admin"
            session["username"] = "admin"
            return redirect("/")

        # User login
        elif uid in ["user1", "user2", "user3"] and password == "1234":
            session["role"] = "user"
            session["username"] = uid
            return redirect("/")

        error = "Invalid credentials"

    return render_template("login.html", error=error)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Home
@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    if session["role"] == "admin":
        return redirect("/admin/feedback-list")
    return redirect("/submit-feedback")

# Submit Feedback Page
@app.route("/submit-feedback", methods=["GET", "POST"])
def submit_feedback():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    if request.method == "POST":
        message = request.form.get("message")
        if message:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO feedback (username, message) VALUES (?, ?)",
                    (username, message)
                )
                conn.commit()
        return redirect("/submit-feedback")

    return render_template("index.html",
                           role=session["role"],
                           username=username,
                           show_form=True,
                           show_list=False,
                           active_page="submit")

# Admin List Page
@app.route("/admin/feedback-list")
def admin_feedback_list():
    if "username" not in session:
        return redirect("/login")

    if session["role"] != "admin":
        return redirect("/submit-feedback")

    with sqlite3.connect(DB_PATH) as conn:
        feedbacks = conn.execute(
            "SELECT username, message FROM feedback ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html",
                           role="admin",
                           username="admin",
                           feedbacks=feedbacks,
                           show_form=False,
                           show_list=True,
                           active_page="list")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
