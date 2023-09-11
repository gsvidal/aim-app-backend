import os

from cs50 import SQL
from flask import Flask, request, jsonify
from flask_session import Session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

from helpers import errorJson, has_required_chars

# Configure application
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)


# Allow requests from specific origins
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173","https://www.gonzalovidal.dev"], "supports_credentials": True}})

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")

# Configure CS50 Library to use PostgreSQL database
# db = SQL("postgresql://gonza:gonza-aim@localhost:5432/aim")
db = SQL(f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}")

# Initialize database tables
def init_db():
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            code TEXT NOT NULL,
            name TEXT NOT NULL
        );
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            score REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(skill_id) REFERENCES skills(id)
        );
    """)

init_db()

def populate_skills():
    skills_data = [
        {"code": "reaction-time", "name": "Reaction Time"},
        {"code": "aim", "name": "Aim"}
        # Add more skills if needed
    ]

    for skill in skills_data:
        # Check if the skill already exists in the table
        existing_skill = db.execute("SELECT id FROM skills WHERE code = ?", skill["code"])
        
        if not existing_skill:
            # Skill doesn't exist, so insert it
            db.execute("INSERT INTO skills (code, name) VALUES (?, ?)", skill["code"], skill["name"])

# Check if skills are already populated
if not db.execute("SELECT * FROM skills"):
    populate_skills()


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

        hashed_password = generate_password_hash(password)

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

    return jsonify({"user_name": user_name, "user_dash_data": user_dash_data, "skills_data": skills})


@app.route("/positions")
@jwt_required()
def positions():
    current_user_id = get_jwt_identity()
    """Show all users scores in positions"""

    goal_reaction_time =  250
    goal_aim = 700
    
    # Getting average score for every user_id and skill_id
    users_data = db.execute("""
        SELECT
        u.username AS user_name,
        u.id AS user_id,
        ROUND(AVG(CASE WHEN sk.code = 'reaction-time' THEN s.score ELSE NULL END)::numeric, 1) AS reaction_time,
        ROUND(AVG(CASE WHEN sk.code = 'aim' THEN s.score ELSE NULL END)::numeric, 1) AS aim,
        ROUND(
            0.5 * ? / AVG(CASE WHEN sk.code = 'reaction-time' THEN s.score ELSE NULL END)::numeric
            + 0.5 * ? / AVG(CASE WHEN sk.code = 'aim' THEN s.score ELSE NULL END)::numeric
        ,3) AS total
        FROM users u
        JOIN scores s ON u.id = s.user_id
        JOIN skills sk ON s.skill_id = sk.id
        GROUP BY u.id, u.username
        ORDER BY total DESC;
            """, goal_reaction_time, goal_aim)

    return jsonify({"users_data": users_data})


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

            return jsonify({"code": 200, "message": "Your score was successfully saved!"})

        except Exception as e:

            return jsonify({"code": 400, "message": "An error occurred. Please try again later."})     
        