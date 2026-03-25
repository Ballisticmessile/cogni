import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT UNIQUE,
    password TEXT
)""")

c.execute("""CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    icon TEXT,
    category TEXT
)""")

c.execute("""CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    text TEXT,
    option_a TEXT,
    option_b TEXT,
    option_c TEXT,
    option_d TEXT,
    correct INTEGER,
    difficulty TEXT
)""")

c.execute("""CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    subject_id INTEGER,
    score INTEGER,
    total INTEGER,
    time_taken INTEGER,
    date TEXT
)""")

# Create Admin Account - CHANGE THIS PASSWORD BEFORE DEPLOYMENT!
admin_password = "admin123"  # Change this to a strong password
hashed_password = generate_password_hash(admin_password)
c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
          ("Administrator", "admin", hashed_password))

# Insert Sample Subjects
subjects = [
    ("Mathematics", "📐", "Science"),
    ("Physics", "⚛️", "Science"),
    ("Chemistry", "🧪", "Science"),
    ("Biology", "🔬", "Science"),
    ("History", "📚", "Humanities"),
    ("Geography", "🌍", "Humanities"),
    ("English Literature", "📖", "Languages"),
    ("Spanish", "🗣️", "Languages"),
    ("Computer Science", "💻", "Technology"),
    ("Web Development", "🌐", "Technology"),
    ("Python Programming", "🐍", "Technology"),
    ("JavaScript", "⚙️", "Technology"),
    ("Economics", "💹", "Business"),
    ("Business Management", "📊", "Business"),
    ("Psychology", "🧠", "Social Science"),
    ("Sociology", "👥", "Social Science"),
    ("Philosophy", "💭", "Humanities"),
    ("General Knowledge", "🎓", "General"),
    ("Current Affairs", "📰", "General"),
    ("Art & Design", "🎨", "Creative"),
]

for subject in subjects:
    c.execute("INSERT INTO subjects (name, icon, category) VALUES (?, ?, ?)", subject)

# Insert Sample Questions
questions = [
    # Mathematics (Subject ID 1)
    (1, "What is the value of π (pi) approximately?", "2.14", "3.14", "4.14", "5.14", 1, "Easy"),
    (1, "What is 15 × 12?", "170", "180", "190", "200", 1, "Easy"),
    (1, "Solve: 2x + 5 = 13", "2", "3", "4", "5", 2, "Medium"),
    (1, "What is the square root of 144?", "11", "12", "13", "14", 1, "Easy"),
    (1, "What is 25% of 200?", "40", "50", "60", "70", 1, "Easy"),
    
    # Physics (Subject ID 2)
    (2, "What is the SI unit of force?", "kg", "m/s", "Newton", "Watt", 2, "Easy"),
    (2, "What is the speed of light in vacuum?", "3 × 10^8 m/s", "3 × 10^5 m/s", "3 × 10^10 m/s", "3 × 10^6 m/s", 0, "Medium"),
    (2, "Newton's first law of motion states:", "Action = Reaction", "F = ma", "An object in motion stays in motion", "Energy is conserved", 2, "Easy"),
    (2, "What does 'g' represent on Earth?", "9.8 m/s^2", "10 m/s^2", "9.8 N", "10 kg", 0, "Medium"),
    (2, "Which energy form is possessed by a moving object?", "Potential Energy", "Kinetic Energy", "Thermal Energy", "Nuclear Energy", 1, "Easy"),
    
    # Chemistry (Subject ID 3)
    (3, "What is the chemical symbol for Gold?", "Go", "Gd", "Au", "Ag", 2, "Easy"),
    (3, "What is the pH of pure water at 25°C?", "6", "7", "8", "9", 1, "Easy"),
    (3, "Which gas do plants absorb from the atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", 2, "Easy"),
    (3, "What is the atomic number of Carbon?", "4", "6", "8", "12", 1, "Easy"),
    (3, "H2O is the chemical formula for:", "Hydrogen Peroxide", "Heavy Water", "Water", "Ozone", 2, "Easy"),
    
    # Biology (Subject ID 4)
    (4, "How many chromosomes does a human have?", "23", "46", "48", "50", 1, "Easy"),
    (4, "What is the powerhouse of the cell?", "Ribosome", "Nucleus", "Mitochondria", "Golgi Apparatus", 2, "Easy"),
    (4, "Which organ pumps blood in the human body?", "Lungs", "Brain", "Heart", "Liver", 2, "Easy"),
    (4, "What is the study of plants called?", "Zoology", "Botany", "Ecology", "Genetics", 1, "Easy"),
    (4, "How many bones does an adult human skeleton have?", "186", "206", "226", "246", 1, "Medium"),
    
    # General Knowledge (Subject ID 18)
    (18, "What is the capital of France?", "London", "Berlin", "Paris", "Rome", 2, "Easy"),
    (18, "How many continents are there?", "6", "7", "8", "9", 1, "Easy"),
    (18, "Who wrote Romeo and Juliet?", "Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain", 1, "Easy"),
    (18, "What is the largest planet in our solar system?", "Saturn", "Jupiter", "Neptune", "Mars", 1, "Easy"),
    (18, "In which year did World War II end?", "1943", "1944", "1945", "1946", 2, "Easy"),
]

for question in questions:
    c.execute("""INSERT INTO questions 
    (subject_id, text, option_a, option_b, option_c, option_d, correct, difficulty) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", question)

conn.commit()
conn.close()

print("DB Created 🚀")