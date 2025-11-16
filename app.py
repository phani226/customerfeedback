from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_DIR = "/app/database"
DB_PATH = f"{DB_DIR}/feedback.db"

os.makedirs(DB_DIR, exist_ok=True)

# Backup feedback
backup_feedback = [
    ("user1", "User1's first feedback"),
    ("user2", "User2's feedback"),
    ("user3", "User3 says hello"),
    ("user1", "User1's second feedback")
]

# Initialize DB
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        # Insert backup if empty
        count = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO feedback (username, message) VALUES (?, ?)",
                backup_feedback
            )
            conn.commit()

init_db()

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        uid = request.form.get("uid")
        password = request.form.get("password")

        if uid == "admin" and password == "admin":
            session["role"] = "admin"
            session["username"] = "admin"
            return redirect("/")

        elif uid in ["user1", "user2", "user3"] and password == "1234":
            session["role"] = "user"
            session["username"] = uid
            return redirect("/")

        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Main page
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    role = session["role"]

    # Determine view (list or submit)
    view = request.args.get("view", "submit" if role != "admin" else "list")

    # POST -> save feedback
    if request.method == "POST":
        message = request.form.get("message")
        if message:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("INSERT INTO feedback (username, message) VALUES (?, ?)",
                             (username, message))
                conn.commit()
        return redirect("/?view=submit")

    feedbacks = []
    if view == "list" and role == "admin":
        with sqlite3.connect(DB_PATH) as conn:
            feedbacks = conn.execute(
                "SELECT username, message FROM feedback ORDER BY id DESC"
            ).fetchall()

    return render_template(
        "index.html",
        feedbacks=feedbacks,
        role=role,
        username=username,
        view=view
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
