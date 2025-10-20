# Environment Variables Setup

## 🔑 Required Environment Variable

Your frontend needs to know where your backend API is located. This is configured using the `VITE_API_BASE_URL` environment variable.

---

## 📋 Quick Setup (Vercel)

### 1. Deploy Backend First

Your backend must be deployed and accessible. Options:

- **Render.com** (Free tier available)
  - URL format: `https://your-app-name.onrender.com`
  - See `GITHUB_PAGES.md` for detailed steps

- **Railway.app** (Free tier available)
  - URL format: `https://your-app-name.up.railway.app`

### 2. Set Environment Variable in Vercel

1. **Go to**: https://vercel.com/dashboard
2. Select your project
3. Click **Settings** → **Environment Variables**
4. Click **"Add New"**
5. Fill in:
   ```
   Name: VITE_API_BASE_URL
   Value: https://your-backend-url.com
   Environments: ☑ Production  ☑ Preview  ☐ Development
   ```
6. Click **Save**

### 3. Redeploy

After adding the variable:
- Go to **Deployments** tab
- Click **"Redeploy"** on the latest deployment

---

## 🧪 Testing

### Before Environment Variable:
```
❌ POST http://127.0.0.1:5000/upload net::ERR_CONNECTION_REFUSED
```

### After Environment Variable:
```
✅ POST https://your-backend.onrender.com/upload 200 OK
```

---

## 🔍 How It Works

In `frontend/src/lib/api.ts`:
```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:5000';
```

- **Local development**: Uses `http://127.0.0.1:5000` (your local Flask server)
- **Production**: Uses `VITE_API_BASE_URL` from Vercel environment variables

---

## 📝 Backend CORS Configuration

Your backend must allow requests from your Vercel frontend. In `backend/config.py`:

```python
CORS_ORIGINS = [
    'http://localhost:5173',           # Local dev
    'http://localhost:4173',           # Local preview
    'https://your-app.vercel.app',     # Production
    'https://*.vercel.app'             # Preview deployments
]
```

Update this with your actual Vercel URL after first deployment!

---

## 🚨 Common Errors

### Error: "Upload failed. Please check file format"
**Cause**: Backend URL not set or incorrect  
**Fix**: Set `VITE_API_BASE_URL` in Vercel environment variables

### Error: "CORS policy: No 'Access-Control-Allow-Origin'"
**Cause**: Backend CORS not configured for your frontend domain  
**Fix**: Update `CORS_ORIGINS` in `backend/config.py`

### Error: "503 Service Unavailable"
**Cause**: Backend is sleeping (free tier) or not deployed  
**Fix**: Wait for backend to wake up (~30 seconds on Render free tier)

---

## 📚 Related Documentation

- **Full Deployment Guide**: See `DEPLOYMENT.md`
- **Backend Deployment**: See `GITHUB_PAGES.md` (Backend section)
- **Troubleshooting**: See `VERCEL_TROUBLESHOOTING.md`
