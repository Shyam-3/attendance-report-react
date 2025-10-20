# Vercel Deployment Troubleshooting

## ❌ Error: Cannot find module '../lib/api'

### Problem:
```
src/pages/Dashboard.tsx(2,131): error TS2307: Cannot find module '../lib/api'
src/pages/Upload.tsx(3,29): error TS2307: Cannot find module '../lib/api'
Error: Command "npm run build" exited with 2
```

### Root Cause:
Vercel is trying to build from the **root directory** instead of the **`frontend/`** directory where your React app is located.

---

## ✅ Solution: Configure Vercel Root Directory

### ⭐ REQUIRED: Set Root Directory in Vercel Dashboard

**Vercel requires the Root Directory to be set in the dashboard** - this cannot be configured via `vercel.json`.

1. **Go to your project settings in Vercel**:
   - https://vercel.com/[your-username]/[your-project]/settings

2. **Navigate to "General" settings**

3. **Find "Root Directory" section**:
   - Click "Edit"
   - Change from `.` (root) to `frontend`
   - Click "Save"

4. **Redeploy**:
   - Go to "Deployments"
   - Click "..." on the latest deployment
   - Click "Redeploy"

### Additional: vercel.json Configuration

A `vercel.json` file has been created in your root directory with optimized build settings:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite"
}
```

**These commands will run INSIDE the `frontend/` directory** after you set the Root Directory.

**Push this file to GitHub**:
```bash
git add vercel.json
git commit -m "Add Vercel configuration"
git push origin main
```

---

## 🎯 Correct Vercel Configuration

### Project Settings:
| Setting | Value |
|---------|-------|
| **Root Directory** | `frontend` |
| **Framework Preset** | Vite |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |
| **Install Command** | `npm install` |
| **Node.js Version** | 18.x or higher |

### Environment Variables:
| Key | Value | Description |
|-----|-------|-------------|
| `VITE_API_BASE_URL` | `https://your-backend.onrender.com` | Your backend URL |

---

## 🔍 How to Check Your Current Settings

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click "Settings"
4. Check "General" → "Root Directory"
5. Should be: `frontend` (not `.` or empty)

---

## 🚀 Step-by-Step Fix

### Step 1: Update Root Directory

1. **In Vercel Dashboard**:
   - Project → Settings → General
   - Root Directory: Change to `frontend`
   - Save

2. **Or delete and reimport**:
   - Delete the current project in Vercel
   - Click "Add New" → "Project"
   - Select your repository
   - **BEFORE clicking Deploy**:
     - Click "Edit" next to Root Directory
     - Set to `frontend`
     - Then click "Deploy"

### Step 2: Verify Build Settings

Make sure these are set:
- ✅ Framework Preset: **Vite**
- ✅ Build Command: `npm run build`
- ✅ Output Directory: `dist`
- ✅ Install Command: `npm install`

### Step 3: Add Environment Variable

- Key: `VITE_API_BASE_URL`
- Value: Your backend URL (e.g., `https://your-app.onrender.com`)

### Step 4: Redeploy

- Go to Deployments tab
- Click "Redeploy" on the latest deployment
- Or push a new commit to trigger deployment

---

## 📁 Your Project Structure

```
attendance-report-react/          ← Root of repository
├── vercel.json                   ← Vercel config (NEW)
├── app.py                        ← Backend
├── requirements.txt              ← Backend dependencies
├── backend/                      ← Backend code
└── frontend/                     ← YOUR REACT APP IS HERE!
    ├── package.json              ← Frontend dependencies
    ├── vite.config.ts            ← Vite config
    ├── index.html                ← Entry point
    └── src/
        ├── App.tsx
        ├── lib/
        │   └── api.ts            ← The file Vercel can't find!
        └── pages/
            ├── Dashboard.tsx
            └── Upload.tsx
```

**The issue**: Vercel was looking for `src/lib/api.ts` from the root, but it's actually at `frontend/src/lib/api.ts`

**The fix**: Tell Vercel to build from the `frontend/` directory!

---

## 🔄 Alternative: Separate Repository for Frontend

If you want to keep things simple, you could:

1. Create a new repository just for frontend
2. Copy the `frontend/` folder contents to new repo
3. Deploy that repository to Vercel (easier!)

But the current setup with `vercel.json` or root directory setting should work fine!

---

## ✅ After Fix, Your Build Should Show:

```
Running "install" command: `npm install`...
✓ Installed packages

Running "build" command: `npm run build`...
vite v7.1.7 building for production...
✓ 45 modules transformed.
dist/index.html                  0.46 kB
dist/assets/index-abc123.css     12.34 kB
dist/assets/index-xyz789.js      156.78 kB
✓ built in 3.45s

Build Completed
```

---

## 🆘 Still Having Issues?

### Check the logs:
1. Go to Vercel deployment
2. Click on the failed deployment
3. Read the full build log
4. Look for the actual error

### Common issues:
- **TypeScript errors**: Fix any TS errors in your code
- **Missing dependencies**: Check `frontend/package.json`
- **Environment variables**: Make sure `VITE_API_BASE_URL` is set

### Test locally first:
```bash
cd frontend
npm install
npm run build
```

If this works locally, it should work on Vercel!

---

## 📝 Summary

**The Error**: Vercel couldn't find `../lib/api` because it was building from the wrong directory

**The Fix**: Set Root Directory to `frontend` in Vercel settings OR use the `vercel.json` file

**Next Step**: Redeploy after changing settings!

Your deployment should work now! 🚀
