import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_cors import CORS

from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, error_page
from datetime import datetime

# Configure application
app = Flask(__name__)

# Allow requests from specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///aim.db")

# Initialize database tables
def init_db():
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

     # Skills to insert, including new skills
    skills_to_insert = ["aim", "reaction time", "new_skill_1", "new_skill_2"]
    
    # Get existing skills from the database
    existing_skills = db.execute("SELECT name FROM skills")

    # Filter out existing skills from skills_to_insert
    new_skills = [skill for skill in skills_to_insert if skill not in (row['name'] for row in existing_skills)]

    # Insert new skills
    for skill_name in new_skills:
        db.execute("INSERT INTO skills (name) VALUES (?)", skill_name)

    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(skill_id) REFERENCES skills(id)
        );
    """)

init_db()

@app.route("/login", methods=["POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    username = request.json.get("username")
    password = request.json.get("password")

    def errorJson(dataType):
        error_data = {"code": "403", "message": f"Must provide {dataType}"}
        return jsonify(error_data), 403

    # Ensure username was submitted
    if not username:
        return errorJson("username")

    # Ensure password was submitted
    elif not password:
        return errorJson("password")

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        error_data = {"code": "403", "message": "Invalid username and/or password"}
        return jsonify(error_data), 403

    # In case username exists, remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Return success message
    return jsonify({"message": "Logged in successfully"})

# API:
@app.route("/get_scores")
@login_required
def get_transactions():
    # scores = db.execute(
    #     )
    return NULL

@app.route("/")
@login_required
def index():
    """Show my scores in dashboard"""
    return jsonify({"message": "Dashboard soon..."})


@app.route("/register", methods=["GET", "POST"])
def register():
    return NULL


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# if __name__ == "__main__":
#     app.run(host='localhost', port=4000)
