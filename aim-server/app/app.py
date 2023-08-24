import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

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


if __name__ == "__main__":
    init_db()

