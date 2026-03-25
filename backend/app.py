from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Enable CORS for all routes - allow requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}})

def get_db():
    return sqlite3.connect("database.db")

# -------- AUTH -------- #

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    
    # Prevent signup with username "admin"
    if data["username"].lower() == "admin":
        return jsonify({"error": "Username 'admin' is reserved and cannot be created"}), 400
    
    conn = get_db()
    c = conn.cursor()

    try:
        hashed_password = generate_password_hash(data["password"])
        c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                  (data["name"], data["username"], hashed_password))
        conn.commit()
        return jsonify({"message": "User created"})
    except:
        return jsonify({"error": "Username exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?",
              (data["username"],))
    user = c.fetchone()

    if user and check_password_hash(user[3], data["password"]):
        return jsonify({
            "id": user[0],
            "name": user[1],
            "username": user[2]
        })
    return jsonify({"error": "Invalid credentials"}), 401


# -------- SUBJECTS -------- #

@app.route("/subjects", methods=["GET"])
def subjects():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM subjects")
    data = c.fetchall()

    return jsonify([
        {"id": s[0], "name": s[1], "icon": s[2], "category": s[3]}
        for s in data
    ])


# -------- QUESTIONS -------- #

@app.route("/questions/<int:subject_id>", methods=["GET"])
def questions(subject_id):
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM questions WHERE subject_id=?", (subject_id,))
    data = c.fetchall()

    return jsonify([
        {
            "id": q[0],
            "text": q[2],
            "options": [q[3], q[4], q[5], q[6]],
            "correct": q[7]
        } for q in data
    ])


# -------- SUBMIT RESULT -------- #

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO results (user_id, subject_id, score, total, time_taken, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["user_id"],
        data["subject_id"],
        data["score"],
        data["total"],
        data["time_taken"],
        data["date"]
    ))

    conn.commit()
    return jsonify({"message": "Saved"})


# -------- ADMIN PANEL -------- #

@app.route("/add-question", methods=["POST"])
def add_question():
    data = request.json
    
    # Verify admin access
    admin_username = data.get("admin_username")
    if not admin_username or admin_username != "admin":
        return jsonify({"error": "Access Denied! Only admins can add questions."}), 403
    
    conn = get_db()
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO questions (subject_id, text, option1, option2, option3, option4, correct_option, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["subject_id"],
            data["text"],
            data["option1"],
            data["option2"],
            data["option3"],
            data["option4"],
            data["correct_option"],
            data["difficulty"]
        ))
        conn.commit()
        return jsonify({"message": "Question added successfully", "success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/add-subject", methods=["POST"])
def add_subject():
    data = request.json
    
    # Verify admin access
    admin_username = data.get("admin_username")
    if not admin_username or admin_username != "admin":
        return jsonify({"error": "Access Denied! Only admins can add subjects."}), 403
    
    conn = get_db()
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO subjects (name, icon, category)
            VALUES (?, ?, ?)
        """, (
            data["name"],
            data["icon"],
            data["category"]
        ))
        conn.commit()
        last_id = c.lastrowid
        return jsonify({
            "message": "Subject added successfully",
            "success": True,
            "id": last_id,
            "name": data["name"],
            "icon": data["icon"],
            "category": data["category"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)