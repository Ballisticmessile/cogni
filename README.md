# 📚 Cogni - Quiz Platform

A modern, full-stack quiz platform built with Python Flask, SQLite, and vanilla JavaScript. Features user authentication, comprehensive quiz system, admin controls, and a responsive design with dark mode support.

## ✨ Features

### User Features
- ✅ **User Authentication** - Secure signup and login with password hashing (PBKDF2-SHA256)
- ✅ **20+ Subjects** - Mathematics, Physics, Chemistry, Biology, History, Geography, and more
- ✅ **Quiz System** - Take interactive quizzes with score tracking
- ✅ **Dark Mode** - Toggle between light and dark themes (persistent preference)
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
- ✅ **Progress Tracking** - See quiz progress with interactive progress bar
- ✅ **Score History** - Results stored in database with timestamps

### Admin Features
- 🔧 **Admin Panel** - Secure admin-only interface
- ➕ **Add Questions** - Create new quiz questions with multiple choice options
- ➕ **Add Subjects** - Add new subjects with custom icons and categories
- 📊 **Manage Content** - View statistics and manage all data
- 🔐 **Admin Security** - Pre-configured admin account, username "admin" reserved

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Flask (Python) |
| **Database** | SQLite3 |
| **Security** | werkzeug (password hashing) |
| **API** | RESTful JSON |
| **Styling** | CSS Custom Properties, Media Queries, Keyframe Animations |

## 📁 Project Structure

```
cogni/
├── backend/
│   ├── app.py                 # Flask API application
│   ├── init_db.py             # Database initialization & sample data
│   ├── models.py              # Database models
│   └── database.db            # SQLite database
├── frontend/
│   ├── index.html             # Main HTML structure
│   ├── app.js                 # JavaScript logic
│   ├── style.css              # CSS styling & animations
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── req.txt                    # Python dependencies
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cogni.git
cd cogni
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install Python dependencies**
```bash
pip install -r req.txt
```

4. **Initialize the database**
```bash
cd backend
python init_db.py
```

This creates `database.db` with:
- 20 pre-configured subjects
- 25 sample questions
- Admin account (username: `admin`, password: `admin123`)

5. **Start the Flask backend**
```bash
python app.py
```

Backend runs on `http://127.0.0.1:5000`

6. **Open the frontend**
- Open `frontend/index.html` in your web browser
- Or use a simple HTTP server:
```bash
cd frontend
python -m http.server 8000
# Then visit http://localhost:8000
```

## 🔐 Security

### Authentication
- Passwords are hashed using PBKDF2-SHA256 algorithm
- Admin "admin" account is pre-created during initialization
- Username "admin" is reserved and cannot be created through signup

### Admin Access
- Only pre-configured admin user can access admin panel
- Both frontend and backend verify admin status
- Admin credentials validated on every admin action
- Error messages prevent unauthorized access

### Database Security
- Parameterized SQL queries prevent SQL injection
- UNIQUE constraint on usernames prevents duplicates
- Foreign keys maintain data integrity

## 📝 API Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/register` | POST | Public | Create new user account |
| `/login` | POST | Public | Authenticate user |
| `/subjects` | GET | Public | List all subjects |
| `/questions/<subject_id>` | GET | Public | Get questions for subject |
| `/submit` | POST | Authenticated | Store quiz results |
| `/add-question` | POST | Admin Only | Add new question |
| `/add-subject` | POST | Admin Only | Create new subject |

## 🎨 Frontend Features

### Responsive Design
- Desktop (>768px): Full-width layout with optimal spacing
- Tablet (768px - 480px): Optimized for medium screens
- Mobile (<480px): Compact single-column layout

### Dark Mode
- Toggle button in top-right corner
- CSS custom properties for dynamic theming
- User preference saved to localStorage
- Smooth transition between themes

### Animations
- 20+ CSS keyframe animations
- Smooth page transitions
- Question slide-up effects
- Progress bar animations
- Button hover effects

## 🧪 Testing

### Test Regular User Flow
1. Signup with username (not "admin")
2. Login with credentials
3. Select a subject
4. Take a quiz
5. View results

### Test Admin Flow
1. Login as admin (username: `admin`, password: `admin123`)
2. Click "Admin Panel" button
3. Add a new question to a subject
4. Add a new subject
5. View statistics

### Test Security
1. Try to signup with username "admin" → Should be blocked
2. Try to access admin panel as regular user → Should be blocked
3. Verify password is hashed in database

## 📋 Database Tables

### Users
```
id (INTEGER PK) | name (TEXT) | username (TEXT UNIQUE) | password (TEXT hashed)
```

### Subjects
```
id (INTEGER PK) | name (TEXT) | icon (TEXT) | category (TEXT)
```

### Questions
```
id (INTEGER PK) | subject_id (INTEGER FK) | text (TEXT) | option1-4 (TEXT) | 
correct_option (INTEGER) | difficulty (TEXT)
```

### Results
```
id (INTEGER PK) | user_id (INTEGER FK) | subject_id (INTEGER FK) | 
score (INTEGER) | total (INTEGER) | time_taken (INTEGER) | date (TEXT)
```

## 🚀 Deployment

### Before Production
1. **Change admin password**
   - Edit `backend/init_db.py` line 38
   - Change `admin_password = "admin123"` to a strong password
   - Recreate database: `python init_db.py`

2. **Update backend URL** (if hosting separately)
   - Edit `frontend/app.js`
   - Change `http://127.0.0.1:5000` to your production URL

3. **Enable HTTPS**
   - Use SSL/TLS certificates
   - Redirect HTTP to HTTPS

4. **Production Server Setup**
   - Replace Flask development server with production WSGI (Gunicorn, uWSGI)
   - Setup reverse proxy (Nginx, Apache)
   - Enable CORS for cross-origin requests

5. **Database Migration**
   - SQLite is suitable for small-medium deployments
   - For large scale, migrate to PostgreSQL/MySQL

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/app.py"]
```

## 📊 Sample Data

### 20 Pre-configured Subjects
- **Science**: Mathematics, Physics, Chemistry, Biology
- **Humanities**: History, Geography, English Literature, Philosophy
- **Languages**: Spanish
- **Technology**: Computer Science, Web Development, Python, JavaScript
- **Business**: Economics, Business Management
- **Social Science**: Psychology, Sociology
- **General**: General Knowledge, Current Affairs, Art & Design

### 25 Sample Questions
- 5 Mathematics questions
- 5 Physics questions
- 5 Chemistry questions
- 5 Biology questions
- 5 General Knowledge questions

## 🐛 Troubleshooting

### Backend not starting
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # macOS/Linux

# Kill the process and restart
# Or change port in app.py: app.run(debug=True, port=5001)
```

### Frontend not loading questions
- Ensure backend is running on `http://127.0.0.1:5000`
- Check browser console for API errors (F12 → Console)
- Verify database is initialized: `python init_db.py`

### Admin panel not showing
- Login as admin (username: `admin`)
- Check browser console for JavaScript errors
- Verify currentUser object has username === "admin"

### Password not working
- Ensure password is at least 6 characters
- Check if admin password was changed in init_db.py
- Recreate database if admin password was modified

## 📚 Documentation

Full technical documentation available in [Cogni_Documentation.pdf](./Cogni_Documentation.pdf)

Includes:
- Architecture overview
- Complete API documentation
- Database schema details
- Security implementation
- Frontend features
- Deployment instructions

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Improve documentation
- Add more subjects/questions

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a comprehensive quiz platform demonstration.

## 🎯 Future Enhancements

- [ ] User profile dashboard
- [ ] Quiz leaderboard/rankings
- [ ] Timed quizzes with countdown
- [ ] Difficulty-based filtering
- [ ] Answer review after submission
- [ ] User statistics and analytics
- [ ] Email notifications
- [ ] Quiz categories and tags
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time multiplayer quizzes

## ⭐ Status

**Production Ready** ✅

All features are implemented and tested. The platform is ready for deployment.

---

**Questions?** Open an issue or check the documentation for more details.
#   P R O J E C T  
 