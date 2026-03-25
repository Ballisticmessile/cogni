# 🚀 Cogni Quiz Platform - Deployment Guide

## **Option 1: Deploy to Render (Recommended - Easiest & FREE)**

### **Prerequisites:**
- GitHub account (already have ✅)
- Render account (free)

### **Step-by-Step Instructions:**

#### **Step 1: Create Render Account**
1. Go to https://render.com
2. Click "Sign up"
3. Choose "Continue with GitHub"
4. Authorize Render to access your GitHub

#### **Step 2: Create Backend Service**
1. Click on your dashboard (after login)
2. Click "New" → "Web Service"
3. Connect your GitHub account if not already done
4. Select repository: `cogni`
5. Click "Connect"

#### **Step 3: Configure Backend Deployment**
Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `cogni-backend` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Root Directory** | `backend` |

#### **Step 4: Deploy**
1. Click "Create Web Service"
2. Wait 2-3 minutes for deployment to complete
3. Once deployed, you'll get a URL like: `https://cogni-backend-xxxx.onrender.com`
4. ✅ **Backend is now LIVE!**

---

## **Option 2: Deploy Frontend to Netlify (Also FREE)**

### **Step-by-Step Instructions:**

#### **Step 1: Prepare Frontend**
1. Ensure `frontend/` folder has:
   - `index.html`
   - `app.js`
   - `style.css`

#### **Step 2: Deploy to Netlify**
1. Go to https://netlify.com
2. Click "Sign up" → "Continue with GitHub"
3. Authorize Netlify
4. Click "Add new site" → "Deploy manually"
5. Drag & drop your `frontend/` folder
6. Netlify will assign a URL like: `cogni-xxxxx.netlify.app`
7. ✅ **Frontend is now LIVE!**

---

## **Option 3: Deploy Everything to Railway (Single Dashboard)**

### **Step-by-Step:**
1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose `cogni` repository
5. Railway auto-detects and deploys!
6. Gets a free public URL automatically

---

## **After Deployment - Important!**

### **Update Frontend API URL** (if using separate frontend/backend)

If you deployed frontend to Netlify and backend to Render:

**In `frontend/app.js` line 12-14:**
```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://127.0.0.1:5000'
  : 'https://cogni-backend-xxxx.onrender.com';  // ← Change this URL
```

Replace `cogni-backend-xxxx.onrender.com` with your actual Render backend URL.

---

## **Test Your Live Website**

1. Open your frontend URL
2. Try to **login** with: 
   - Username: `admin`
   - Password: `admin123`
3. Try to **signup** with a new username
4. Start a quiz and verify it works!

---

## **Troubleshooting**

### **Backend showing 502 Bad Gateway?**
- Wait 2-3 more minutes for full startup
- Check Render dashboard logs for errors
- Ensure `requirements.txt` is in `backend/` folder

### **Frontend can't connect to backend?**
- Verify the API_URL is correct in `app.js`
- Check that CORS is enabled (it is ✅)
- Open browser DevTools (F12) → Network tab to see requests

### **Database errors on production?**
- Render creates `database.db` automatically on first run
- If issues persist, redeploy the service

---

## **Free Tier Limitations**

| Service | Free Tier |
|---------|-----------|
| Render | 750 hours/month (enough!) |
| Netlify | Unlimited deploys |
| Railway | $5 free credits/month |

---

## **Custom Domain (Optional)**

1. Buy domain from GoDaddy, Namecheap, or similar ($1-5/year)
2. In Render/Netlify: Settings → Domains → Add custom domain
3. Update DNS records at your domain registrar
4. Done! 🎉

---

## **Need Help?**

**Error messages?** Check logs:
- Render: Dashboard → Your service → Logs tab
- Netlify: Site settings → Deploys → View logs

**Still stuck?** Ask me for help with specific error messages!

---

**You're ready to go live! 🚀**
