import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from flask_cors import CORS

from werkzeug.security import check_password_hash, generate_password_hash

from helpers import errorJson, has_required_chars
from datetime import datetime

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


# Configure application
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"
jwt = JWTManager(app)


# Allow requests from specific origins
CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

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
            code TEXT NOT NULL,
            name TEXT NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            score REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(skill_id) REFERENCES skills(id)
        );
    """)

init_db()


@app.route("/login", methods=["POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")

        # Ensure username was submitted
        if not username:
            return errorJson("Must provide username")

        # Ensure password was submitted
        elif not password:
            return errorJson("Must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            error_data = {"code": "403", "message": "Invalid username and/or password"}
            return jsonify(error_data), 403

        # Generate JWT token
        access_token = create_access_token(identity=rows[0]["id"])
        # print(f"token backend login for {username}: {access_token}")

        return jsonify({"access_token": access_token, "message": "Logged in successfully"})
        


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
        confirmation = request.json.get("password-confirmation")

        print(f"credentials sent from frontend: {username}, {password}, {confirmation}")
        
        rows = db.execute("SELECT * FROM users WHERE username=?", username)
        print(f"rowsss: {rows}")

        # Backend Validation
        if username == "":
            return errorJson("Username cannot be blank")
        
        elif len(rows) > 0:
            return errorJson("Username already exists, try another one")

        if password == "":
            return errorJson("Password cannot be blank")
        
        if len(password) < 6:
            return errorJson("Password must be at least 6 characters long")

        if not has_required_chars(password):
            return errorJson("Password must contain at least one uppercase letter, one digit, and one symbol")
        
        if password != confirmation:
            return errorJson("Passwords do not match")

        hashed_password = generate_password_hash(password, method="scrypt")

        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hashed_password)

        rows_new = db.execute("SELECT * FROM users WHERE username=?", username)

        # Generate JWT token
        access_token = create_access_token(identity=rows_new[0]["id"])
        # print(f"token backend register for {username}: {access_token}")

        return jsonify({"access_token": access_token, "message": "Registered successfully"})

# Initialize the set for revoked tokens
revoked_tokens = set()

@app.route("/logout")
@jwt_required()
def logout():
    """Log user out"""
    current_user_id = get_jwt_identity()

    # Revoke the JWT token for the current user
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)  # You need to define 'revoked_tokens' as a set or a storage mechanism

    # Redirect user to login form
    return jsonify({"message": "Logged out successfully"})

@app.route("/")
@jwt_required()
def index():
    current_user_id = get_jwt_identity()

    """Show my scores in dashboard"""

    users = db.execute("SELECT * FROM users WHERE id=?", current_user_id)

    user_name = users[0]["username"]

    skills = db.execute("SELECT * FROM skills")

    scores = db.execute("SELECT * FROM scores WHERE user_id=?", current_user_id)

    user_dash_data = db.execute("""
        SELECT 
            u.username AS user_name,
            s.name AS skill_name,
            s.id AS skill_id,
            MIN(sc.score) AS best_score,
            AVG(sc.score) AS avg_score,
            MAX(CASE WHEN sc.timestamp = (SELECT MAX(timestamp) FROM scores WHERE user_id = ? AND skill_id = s.id) THEN sc.score ELSE NULL END) AS last_score
        FROM
            skills s
        LEFT JOIN
            scores sc ON s.id = sc.skill_id
        JOIN
            users u ON sc.user_id = u.id
        WHERE
            sc.user_id = ?
        GROUP BY
            u.username, s.name, s.id
        ORDER BY
            s.name;
        """, current_user_id, current_user_id)

    # print(f"general scores: {scores}")
    # print(f"user_name for {user_name}: {user_name}")
    # print(f"user_scores for {user_name}: {user_dash_data}")
    # print(f"skills_data: {skills}")
    return jsonify({"user_name": user_name, "user_dash_data": user_dash_data, "skills_data": skills})


# API:
@app.route("/games", methods=["POST"]) # This could be /games to save all kind of game
@jwt_required()  
def games():
    if request.method == "POST":
        try:
            current_user_id = get_jwt_identity()

            # Update:
            skill_code = request.json.get("skill_code")
            score = request.json.get("score")

            # Get skill_id:
            skills = db.execute("SELECT * FROM skills WHERE code=?", skill_code)
            skill_id = skills[0]["id"]

            # Inserting score
            db.execute("INSERT INTO scores (user_id, skill_id, score) VALUES (?,?,?)", current_user_id, skill_id, score)

            return jsonify({"code": 200, "message": "Your score was successfully saved"})

        except Exception as e:

            return jsonify({"code": 400, "message": "An error occurred. Please try again later."})     
        