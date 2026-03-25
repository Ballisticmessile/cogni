# Environment Variables Setup Guide

## **Local Development (.env file)**

### **Step 1: Create `.env` file in backend folder**

```bash
# Navigate to backend
cd backend

# Create .env file (Windows PowerShell)
New-Item -Name ".env" -ItemType File

# Or create manually in VS Code
```

### **Step 2: Add Environment Variables**

Create `/backend/.env` with:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here_change_in_production

# Database
DATABASE_URL=sqlite:///database.db

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:5000

# Server
PORT=5000
HOST=127.0.0.1
```

### **Step 3: Install python-dotenv**

```bash
pip install python-dotenv
```

### **Step 4: Update `backend/app.py` to use .env**

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
```

---

## **Production Environment Variables**

### **For Render:**

1. Dashboard → Your Service → Environment
2. Add variables:

```
FLASK_ENV=production
SECRET_KEY=your_production_secret_key_here
DATABASE_URL=sqlite:///database.db
PORT=10000
```

### **For Railway:**

1. Dashboard → Project → Variables
2. Add the same variables

### **For Fly.io:**

In `fly.toml`:

```toml
[env]
FLASK_ENV = "production"
SECRET_KEY = "your_production_secret_key"
PORT = "8080"
```

---

## **Updated Backend Code**

Replace your `backend/app.py` top section with:

```python
from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, resources={r"/*": {"origins": CORS_ORIGINS}})

def get_db():
    return sqlite3.connect("database.db")

# ... rest of your code
```

---

## **For Frontend - API URL from Environment**

Update `frontend/app.js`:

```javascript
// Detect environment and set API URL
const API_URL = (() => {
  const hostname = window.location.hostname;
  
  // Development
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://127.0.0.1:5000';
  }
  
  // Production
  return `https://${hostname}`;
})();

console.log('Using API URL:', API_URL);
```

---

## **Common Environment Variables**

| Variable | Purpose | Example |
|----------|---------|---------|
| `FLASK_ENV` | Development or production | `production` |
| `SECRET_KEY` | Session/cookie encryption | `your-secret-key-here` |
| `PORT` | Server port | `5000` or `10000` |
| `DATABASE_URL` | Database connection | `sqlite:///database.db` |
| `CORS_ORIGINS` | Allowed frontend URLs | `https://example.com` |
| `DEBUG` | Enable error details | `False` (production) |

---

## **Security Tips**

✅ **DO:**
- Use strong SECRET_KEY in production
- Store sensitive variables in .env (never commit!)
- Use different keys for development vs production

❌ **DON'T:**
- Commit `.env` file to GitHub
- Use same SECRET_KEY everywhere
- Share environment variables publicly

---

## **Add to .gitignore**

Create `.gitignore` in root:

```
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
ENV/

# Database
database.db

# OS
.DS_Store
.idea/
.vscode/

# Database backups
*.db-journal
```

---

## **Test Environment Variables Locally**

Add this to `backend/app.py`:

```python
@app.route('/debug-config', methods=['GET'])
def debug_config():
    """For debugging only - remove in production!"""
    if FLASK_ENV != 'production':
        return jsonify({
            'FLASK_ENV': FLASK_ENV,
            'PORT': PORT,
            'HOST': HOST,
            'DEBUG': app.debug
        })
    return jsonify({'error': 'Not available in production'}), 403
```

Then visit: `http://localhost:5000/debug-config`

---

**Ready to use environment variables? Let me know if you need help!** 🚀
