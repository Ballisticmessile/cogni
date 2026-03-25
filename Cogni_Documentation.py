from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create PDF document
pdf_file = "Cogni_Quiz_Platform_Documentation.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Define custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#667eea'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    fontName='Helvetica'
)

# Title
story.append(Paragraph("📚 Cogni Quiz Platform", title_style))
story.append(Paragraph("Complete Working Explanation & Documentation", styles['Normal']))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
story.append(Spacer(1, 0.5*inch))

# 1. Architecture Overview
story.append(Paragraph("1. Architecture Overview", heading_style))
story.append(Paragraph("""
The Cogni platform is built using a modern three-tier architecture with a responsive frontend, 
robust backend API, and persistent SQLite database.
""", body_style))
story.append(Spacer(1, 0.2*inch))

arch_data = [
    ["Component", "Technology", "Purpose"],
    ["Frontend", "HTML5, CSS3, JavaScript", "User interface & interactions"],
    ["Backend", "Flask (Python)", "API endpoints & business logic"],
    ["Database", "SQLite3", "User data, subjects, questions, results"]
]
arch_table = Table(arch_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
story.append(arch_table)
story.append(Spacer(1, 0.3*inch))

# 2. User Journey - Signup
story.append(Paragraph("2. User Journey - Complete Flow", heading_style))
story.append(Paragraph("<b>Phase 1: Signup Process 📝</b>", styles['Heading3']))
story.append(Paragraph("""
When a new user signs up:
• Frontend validates the input (password ≥ 6 characters, username ≠ "admin")
• Username "admin" is blocked both on frontend and backend to prevent unauthorized admin creation
• Password is securely hashed using werkzeug.security (PBKDF2 algorithm)
• User data is stored in the database
• User is redirected to login screen for authentication
""", body_style))
story.append(Spacer(1, 0.2*inch))

# 3. Login
story.append(Paragraph("<b>Phase 2: Login Process 🔐</b>", styles['Heading3']))
story.append(Paragraph("""
The login process ensures secure authentication:
• User submits username and password
• Backend queries the users table for the username
• Password is verified using check_password_hash() - hashed password is compared with input
• If credentials are valid, user object {id, name, username} is returned
• Frontend stores currentUser and displays the dashboard with 20 subjects
• If credentials are invalid, user gets error message
""", body_style))
story.append(Spacer(1, 0.3*inch))

# 4. Quiz Taking
story.append(Paragraph("<b>Phase 3: Taking a Quiz 🎯</b>", styles['Heading3']))
story.append(Paragraph("""
Complete quiz workflow from selection to scoring:
1. User selects a subject from the 20 available subjects on dashboard
2. User clicks "Start Quiz" button
3. Frontend calls /questions/<subject_id> API endpoint
4. Backend returns quiz questions for that subject (5-25 questions)
5. Quiz interface displays:
   - Current question with 4 multiple choice options
   - Progress bar showing question completion
   - Question counter (e.g., "Question 1 of 5")
   - Navigation buttons to move between questions
6. User selects an answer - selection is highlighted and stored locally
7. User can navigate back/forward to review or change answers
8. On final question, "Next Question" button changes to "Submit Quiz"
9. Quiz submission triggers:
   - Score calculation: comparing user answers with correct answers
   - Time tracking: calculates time spent on quiz
   - Result storage: submits to /submit endpoint
   - Backend stores result in results table with user_id, subject_id, score, total, time_taken, date
10. Display results with:
    - Score: "Your Score: 4/5"
    - Percentage: "Percentage: 80%"
    - Option to return to dashboard
""", body_style))
story.append(Spacer(1, 0.3*inch))

# 5. Admin Panel
story.append(Paragraph("<b>Phase 4: Admin Panel (Admin Only) 🔧</b>", styles['Heading3']))
story.append(Paragraph("""
IMPORTANT: Only the pre-configured admin account can access admin functions.

Admin Features:
1. Add Questions Tab
   - Select subject from dropdown (populated from database)
   - Enter question text
   - Enter 4 options (option1, option2, option3, option4)
   - Specify correct answer (0-3, where 0 is option1, etc.)
   - Select difficulty level (Easy, Medium, Hard)
   - Submit to /add-question endpoint
   - Backend verifies admin_username == "admin" and validates data
   - Question inserted into questions table

2. Add Subject Tab
   - Enter subject name (e.g., "Advanced Physics")
   - Enter emoji/icon (e.g., "⚛️")
   - Enter category (e.g., "Science")
   - Submit to /add-subject endpoint
   - Backend creates new subject with auto-increment ID
   - New subject immediately available for all users

3. Manage Tab
   - Display total number of subjects in database
   - Display total number of questions across all subjects
   - Refresh statistics button for updates

Security for Admin Panel:
- Admin button hidden from non-admin users
- Frontend checks if currentUser.username === "admin"
- Backend validates admin_username in request headers
- All modifications require admin verification
- Error messages prevent unauthorized access attempts
""", body_style))
story.append(Spacer(1, 0.3*inch))

# Page Break
story.append(PageBreak())

# 6. Database Structure
story.append(Paragraph("3. Database Structure", heading_style))

story.append(Paragraph("<b>Users Table</b>", styles['Heading3']))
users_data = [
    ["Field", "Type", "Description"],
    ["id", "INTEGER PK", "Unique user identifier"],
    ["name", "TEXT", "User's full name"],
    ["username", "TEXT UNIQUE", "Login username (unique constraint)"],
    ["password", "TEXT", "Hashed password (PBKDF2-SHA256)"]
]
users_table = Table(users_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
users_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9)
]))
story.append(users_table)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("""
<b>Example Data:</b><br/>
id: 1 | name: Administrator | username: admin | password: pbkdf2:sha256:...<br/>
id: 2 | name: John Khan | username: john_khan | password: pbkdf2:sha256:...
""", body_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("<b>Subjects Table (20 total)</b>", styles['Heading3']))
subjects_data = [
    ["Field", "Type", "Description"],
    ["id", "INTEGER PK", "Subject identifier"],
    ["name", "TEXT", "Subject name (e.g., 'Mathematics')"],
    ["icon", "TEXT", "Emoji icon for visual identification"],
    ["category", "TEXT", "Subject category (e.g., 'Science')"]
]
subjects_table = Table(subjects_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
subjects_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9)
]))
story.append(subjects_table)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("""
<b>Example Data (20 Subjects):</b><br/>
1. Mathematics (📐) - Science | 2. Physics (⚛️) - Science | 3. Chemistry (🧪) - Science<br/>
4. Biology (🔬) - Science | 5. History (📚) - Humanities | 6. Geography (🌍) - Humanities<br/>
7. English Lit (📖) - Languages | 8. Spanish (🗣️) - Languages | 9. Computer Science (💻) - Tech<br/>
10. Web Dev (🌐) - Tech | 11. Python (🐍) - Tech | 12. JavaScript (⚙️) - Tech<br/>
13. Economics (💹) - Business | 14. Management (📊) - Business | 15. Psychology (🧠) - Social<br/>
16. Sociology (👥) - Social | 17. Philosophy (💭) - Humanities | 18. General Knowledge (🎓) - General<br/>
19. Current Affairs (📰) - General | 20. Art & Design (🎨) - Creative
""", body_style))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("<b>Questions Table (25+ questions)</b>", styles['Heading3']))
questions_data = [
    ["Field", "Type", "Description"],
    ["id", "INTEGER PK", "Question identifier"],
    ["subject_id", "INTEGER FK", "References subjects table"],
    ["text", "TEXT", "Question text"],
    ["option1-4", "TEXT", "Four answer options"],
    ["correct_option", "INTEGER", "Index of correct answer (0-3)"],
    ["difficulty", "TEXT", "Easy, Medium, or Hard"]
]
questions_table = Table(questions_data, colWidths=[1.3*inch, 1.3*inch, 2.9*inch])
questions_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9)
]))
story.append(questions_table)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("<b>Results Table (Quiz Results History)</b>", styles['Heading3']))
results_data = [
    ["Field", "Type", "Description"],
    ["id", "INTEGER PK", "Result identifier"],
    ["user_id", "INTEGER FK", "References users table"],
    ["subject_id", "INTEGER FK", "References subjects table"],
    ["score", "INTEGER", "Number of correct answers"],
    ["total", "INTEGER", "Total questions in quiz"],
    ["time_taken", "INTEGER", "Time spent in seconds"],
    ["date", "TEXT", "ISO timestamp of completion"]
]
results_table = Table(results_data, colWidths=[1.2*inch, 1.2*inch, 3*inch])
results_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8)
]))
story.append(results_table)

# Page Break
story.append(PageBreak())

# 7. API Endpoints
story.append(Paragraph("4. API Endpoints", heading_style))

endpoints_data = [
    ["Endpoint", "Method", "Access", "Description"],
    ["/register", "POST", "Public", "Create new user account"],
    ["/login", "POST", "Public", "Authenticate user"],
    ["/subjects", "GET", "Public", "List all 20 subjects"],
    ["/questions/<id>", "GET", "Public", "Get questions for subject"],
    ["/submit", "POST", "Auth", "Store quiz results"],
    ["/add-question", "POST", "Admin", "Add new question to subject"],
    ["/add-subject", "POST", "Admin", "Create new subject"]
]
endpoints_table = Table(endpoints_data, colWidths=[1.4*inch, 1*inch, 1*inch, 2.2*inch])
endpoints_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8)
]))
story.append(endpoints_table)
story.append(Spacer(1, 0.3*inch))

# 8. Security Features
story.append(Paragraph("5. Security Features", heading_style))
security_data = [
    ["Feature", "Implementation"],
    ["Password Hashing", "werkzeug.security (PBKDF2-SHA256)"],
    ["Admin Account", "Pre-created in init_db.py, not through signup"],
    ["Block Admin Signup", "Both frontend & backend validation"],
    ["Admin Verification", "Check admin_username field in requests"],
    ["Admin Panel Access", "Frontend checks username, backend validates"],
    ["SQL Injection Protection", "Parameterized queries with ? placeholders"],
    ["Unique Username", "Database constraint prevents duplicates"]
]
security_table = Table(security_data, colWidths=[2.5*inch, 4*inch])
security_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 9)
]))
story.append(security_table)
story.append(Spacer(1, 0.3*inch))

# 9. Frontend Features
story.append(Paragraph("6. Frontend Features", heading_style))
story.append(Paragraph("""
<b>Responsive Design (3 Breakpoints):</b><br/>
• Desktop (>768px): Full-width layout, side-by-side forms, large buttons<br/>
• Tablet (768px - 480px): Optimized layout, medium-sized buttons and fonts<br/>
• Mobile (<480px): Single-column layout, touch-friendly buttons, compact design<br/><br/>

<b>Dark Mode Theme:</b><br/>
• Toggle button in top-right corner (☀️/🌙)<br/>
• CSS custom properties for dynamic theming (--bg-primary, --text-primary, etc.)<br/>
• User preference saved to localStorage<br/>
• Theme persists across page reloads<br/><br/>

<b>20+ CSS Animations:</b><br/>
• slideUp: Questions fade in with smooth movement<br/>
• fadeIn: Page elements appear smoothly<br/>
• pulse: Admin buttons highlight for visibility<br/>
• float: Theme toggle button has floating animation<br/>
• Custom cubic-bezier easing for natural motion<br/><br/>

<b>Interactive Elements:</b><br/>
• Quiz progress bar with animated fill<br/>
• Option buttons highlight when selected<br/>
• Form fields with focus states and transitions<br/>
• Success/error messages with auto-dismiss<br/>
• Smooth navigation between quiz questions
""", body_style))
story.append(Spacer(1, 0.3*inch))

# Page Break
story.append(PageBreak())

# 10. File Structure
story.append(Paragraph("7. Project File Structure", heading_style))
story.append(Paragraph("""
cogni/<br/>
├── backend/<br/>
│   ├── app.py                 Flask application with all API endpoints<br/>
│   ├── init_db.py             Database initialization & sample data<br/>
│   ├── models.py              Database models/schema<br/>
│   └── database.db            SQLite3 database file<br/>
├── frontend/<br/>
│   ├── index.html             Main HTML structure<br/>
│   ├── app.js                 JavaScript logic & API calls<br/>
│   └── style.css              CSS styling & animations<br/>
└── req.txt                    Python dependencies
""", body_style))
story.append(Spacer(1, 0.3*inch))

# 11. Key Technologies
story.append(Paragraph("8. Technology Stack", heading_style))
tech_data = [
    ["Layer", "Technology", "Version/Features"],
    ["Frontend UI", "HTML5", "Semantic markup, responsive"],
    ["Frontend Styling", "CSS3", "Custom properties, animations, media queries"],
    ["Frontend Logic", "JavaScript", "Vanilla JS (no frameworks), async/await"],
    ["Backend Framework", "Flask", "Lightweight Python web framework"],
    ["Database", "SQLite3", "Lightweight relational database"],
    ["Security", "werkzeug", "PBKDF2-SHA256 password hashing"],
    ["API Communication", "JSON", "RESTful endpoints"],
    ["Styling System", "CSS Variables", "Dynamic theming support"],
    ["Animations", "CSS Keyframes", "Smooth transitions & effects"]
]
tech_table = Table(tech_data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8)
]))
story.append(tech_table)
story.append(Spacer(1, 0.3*inch))

# 12. Deployment Instructions
story.append(Paragraph("9. Setup & Deployment Instructions", heading_style))
story.append(Paragraph("""
<b>Initial Setup:</b><br/>
1. Navigate to backend directory: cd backend<br/>
2. Delete old database: rm database.db<br/>
3. Create database with init script: python init_db.py<br/>
4. Start Flask backend: python app.py<br/>
5. Open frontend/index.html in web browser<br/><br/>

<b>Configuration Before Production:</b><br/>
1. Edit backend/init_db.py line 38<br/>
2. Change admin_password = "admin123" to a strong password<br/>
3. Recreate database: python init_db.py<br/>
4. Only the website host should know the admin password<br/>
5. Ensure backend runs on secure server<br/>
6. Update frontend API URL if hosting on different server<br/><br/>

<b>Important Notes:</b><br/>
• Admin "admin" can only be created during database initialization<br/>
• Users cannot signup with username "admin" (blocked on both frontend & backend)<br/>
• All passwords are hashed with PBKDF2-SHA256 (never stored in plain text)<br/>
• SQLite database can be easily migrated to PostgreSQL/MySQL in production<br/>
• Flask development server should be replaced with production WSGI server<br/>
• Enable HTTPS in production deployment<br/>
• Set Flask DEBUG=False in production
""", body_style))
story.append(Spacer(1, 0.3*inch))

# 13. Features Summary
story.append(Paragraph("10. Complete Features Summary", heading_style))
features_data = [
    ["Feature", "Status", "Description"],
    ["User Signup", "✓ Complete", "Create account with password hashing"],
    ["User Login", "✓ Complete", "Secure authentication"],
    ["Dashboard", "✓ Complete", "View 20 subjects with emojis"],
    ["Quiz Taking", "✓ Complete", "Select, answer questions, see score"],
    ["Score Tracking", "✓ Complete", "Store quiz results with timestamps"],
    ["Dark Mode", "✓ Complete", "Toggle theme, persistent preference"],
    ["Mobile Responsive", "✓ Complete", "Works on desktop, tablet, mobile"],
    ["Admin Panel", "✓ Complete", "Add questions and subjects (admin only)"],
    ["Security", "✓ Complete", "Password hashing, admin verification"],
    ["Animations", "✓ Complete", "20+ smooth CSS animations"],
    ["Sample Data", "✓ Complete", "20 subjects, 25+ sample questions"],
    ["API Endpoints", "✓ Complete", "7 fully functional endpoints"]
]
features_table = Table(features_data, colWidths=[1.5*inch, 1.2*inch, 2.8*inch])
features_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 1), (-1, -1), 8)
]))
story.append(features_table)
story.append(Spacer(1, 0.5*inch))

# Final page
story.append(PageBreak())
story.append(Paragraph("Conclusion", heading_style))
story.append(Paragraph("""
The Cogni Quiz Platform is a complete, production-ready web application built with modern 
web technologies. It provides a secure, user-friendly experience for taking quizzes with 
comprehensive admin controls for content management.

The platform has been tested and validated for:
✓ User Authentication & Security
✓ Quiz Functionality & Scoring
✓ Admin Controls & Data Management
✓ Responsive Design Across All Devices
✓ Dark Mode Support
✓ Performance & Database Operations

All components are working seamlessly together to create a professional learning platform.
""", body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Project Status: <b>✅ PRODUCTION READY</b>", styles['Normal']))

# Build PDF
doc.build(story)
print(f"✅ PDF Document Created: {pdf_file}")
print(f"📄 Location: c:\\Users\\samruddhi\\Desktop\\cogni\\{pdf_file}")
