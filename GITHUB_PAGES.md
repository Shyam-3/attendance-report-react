# Publishing Your Attendance App on GitHub

## 🎯 Publishing Options

Since your app has **both backend and frontend**, here are your options:

---

## Option 1: GitHub Pages (Frontend Only - Limited) ⚠️

GitHub Pages can **only host static websites** (HTML, CSS, JavaScript). It **cannot run Python/Flask backend**.

### What you CAN do:
- ✅ Host the React frontend on GitHub Pages
- ✅ Show the UI and design
- ❌ **Backend won't work** (no file uploads, no database, no API calls)

### Steps to publish frontend only:

1. **Build the React app**:
```bash
cd frontend
npm run build
```
This creates a `dist` folder with static files.

2. **Install GitHub Pages deployment tool**:
```bash
npm install --save-dev gh-pages
```

3. **Add to `frontend/package.json`**:
```json
{
  "scripts": {
    "deploy": "gh-pages -d dist"
  },
  "homepage": "https://shyam-3.github.io/attendance-report-react"
}
```

4. **Deploy**:
```bash
npm run deploy
```

5. **Enable GitHub Pages**:
- Go to: https://github.com/Shyam-3/attendance-report-react/settings/pages
- Source: Select `gh-pages` branch
- Your site will be at: `https://shyam-3.github.io/attendance-report-react`

### ⚠️ Limitations:
- No file uploads
- No database
- No backend features
- Only static UI demonstration

---

## Option 2: Full Stack Deployment (Recommended) ✅

Deploy **both frontend and backend** on free hosting platforms.

### 🔥 Recommended Setup:

#### **Frontend**: Vercel (Free)
- Best for React apps
- Automatic deployments from GitHub
- Fast CDN
- Free SSL certificate

#### **Backend**: Render (Free)
- Supports Python/Flask
- Free tier available
- PostgreSQL database included
- Auto-deploy from GitHub

---

## 🚀 Full Deployment Guide (Frontend + Backend)

### Step 1: Deploy Backend to Render

1. **Create account**: https://render.com (sign in with GitHub)

2. **Create Web Service**:
   - Connect your GitHub repository
   - Select "Web Service"
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

3. **Add environment variables**:
   - `FRONTEND_URL`: `https://your-app.vercel.app`
   - `DATABASE_URL`: (Render provides PostgreSQL for free)

4. **Update `requirements.txt`** (add gunicorn):
```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
pandas>=2.0.0
openpyxl>=3.1.2
xlsxwriter>=3.2.0
Werkzeug>=2.3.7
SQLAlchemy>=2.0.16
reportlab>=4.0.0
Flask-Cors>=4.0.0
gunicorn>=21.2.0
psycopg2-binary>=2.9.9
```

5. **Update `backend/config.py`** for production database:
```python
import os

class Config:
    # Use PostgreSQL in production, SQLite in development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///attendance.db'
    
    # Fix for Render PostgreSQL URL
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://127.0.0.1:5173')
```

6. **Your backend will be at**: `https://your-app.onrender.com`

### Step 2: Deploy Frontend to Vercel

1. **Create account**: https://vercel.com (sign in with GitHub)

2. **Import project**:
   - Click "Add New" → "Project"
   - Select your repository
   - Framework: **Vite**
   - Root Directory: **frontend**

3. **Configure build settings**:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Add environment variable**:
   - Key: `VITE_API_BASE_URL`
   - Value: `https://your-app.onrender.com` (your Render backend URL)

5. **Deploy**: Click "Deploy"

6. **Your frontend will be at**: `https://your-app.vercel.app`

### Step 3: Update CORS

After deployment, update your backend's `app.py` to allow your Vercel domain:

```python
# In app.py
CORS(app, resources={
    r"/api/*": {"origins": ["https://your-app.vercel.app", "http://127.0.0.1:5173"]},
    r"/export/*": {"origins": ["https://your-app.vercel.app", "http://127.0.0.1:5173"]},
    r"/upload": {"origins": ["https://your-app.vercel.app", "http://127.0.0.1:5173"]},
    r"/delete_record/*": {"origins": ["https://your-app.vercel.app", "http://127.0.0.1:5173"]},
    r"/clear_all_data": {"origins": ["https://your-app.vercel.app", "http://127.0.0.1:5173"]}
})
```

---

## 🆓 Other Free Hosting Options

### Backend Options:
| Platform | Free Tier | Database | Python Support |
|----------|-----------|----------|----------------|
| **Render** | ✅ Yes | PostgreSQL | ✅ Yes |
| **Railway** | ✅ Limited | PostgreSQL | ✅ Yes |
| **PythonAnywhere** | ✅ Yes | SQLite/MySQL | ✅ Yes |
| **Fly.io** | ✅ Limited | PostgreSQL | ✅ Yes |
| **Heroku** | ❌ Paid only | PostgreSQL | ✅ Yes |

### Frontend Options:
| Platform | Free Tier | Auto Deploy | CDN |
|----------|-----------|-------------|-----|
| **Vercel** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Netlify** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Cloudflare Pages** | ✅ Yes | ✅ Yes | ✅ Yes |
| **GitHub Pages** | ✅ Yes | ✅ Yes | ❌ No |

---

## 📦 Files to Update Before Deployment

### 1. Create `gunicorn` configuration (optional)

**File**: `gunicorn.conf.py`
```python
bind = "0.0.0.0:5000"
workers = 2
timeout = 120
```

### 2. Create `Procfile` for some platforms

**File**: `Procfile`
```
web: gunicorn app:app
```

### 3. Update `.gitignore` (already done)

Make sure these are in `.gitignore`:
```
instance/
*.db
*.sqlite
node_modules/
dist/
.env
```

---

## 🔒 Security Checklist Before Publishing

### ✅ Do This:
- [ ] Remove any test data from database
- [ ] Change `SECRET_KEY` to a secure random string
- [ ] Set `DEBUG = False` in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS only
- [ ] Restrict CORS to your actual domain
- [ ] Use PostgreSQL instead of SQLite for production

### ❌ Never Commit:
- [ ] `.env` files with secrets
- [ ] Database files with real student data
- [ ] API keys or passwords
- [ ] `instance/` folder

---

## 🎬 Quick Start: Deploy Now (Recommended Path)

### For Full Functionality:

1. **Sign up for Render**: https://render.com
2. **Sign up for Vercel**: https://vercel.com
3. **Follow Step 1 above** (Deploy Backend to Render)
4. **Follow Step 2 above** (Deploy Frontend to Vercel)
5. **Test your live app**!

### For Demo Only (No Backend):

1. **Build frontend**:
```bash
cd frontend
npm run build
```

2. **Install gh-pages**:
```bash
npm install gh-pages --save-dev
```

3. **Update `frontend/package.json`**:
```json
{
  "homepage": "https://shyam-3.github.io/attendance-report-react",
  "scripts": {
    "deploy": "gh-pages -d dist"
  }
}
```

4. **Deploy**:
```bash
npm run deploy
```

5. **Enable in GitHub**:
   - Settings → Pages → Source: `gh-pages` branch

---

## 🌐 Your Published URLs

After deployment, you'll have:

- **Frontend**: `https://your-app.vercel.app` or `https://shyam-3.github.io/attendance-report-react`
- **Backend API**: `https://your-app.onrender.com`
- **Repository**: `https://github.com/Shyam-3/attendance-report-react`

---

## 💡 Recommendation

**For a portfolio project or real use:**
- ✅ Use **Vercel** (frontend) + **Render** (backend)
- ✅ Get full functionality with database
- ✅ Professional setup
- ✅ Free tier is sufficient
- ✅ Auto-deploys from GitHub

**For just showing code:**
- ✅ Keep it on GitHub as repository
- ✅ Good README.md is enough
- ✅ Screenshots + demo GIFs help

**For demo UI only:**
- ✅ Use GitHub Pages
- ⚠️ Mention "Backend not hosted" in README

---

## 📞 Need Help?

**Documentation**:
- Vercel: https://vercel.com/docs
- Render: https://render.com/docs
- GitHub Pages: https://pages.github.com

**Your current setup works perfectly for local development!** 
Deployment is optional and depends on your needs.
