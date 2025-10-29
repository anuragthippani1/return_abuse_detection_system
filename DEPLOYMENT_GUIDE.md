# 🚀 Deployment Guide - Amazon Return Abuse Detection System

This guide will help you deploy both the **Frontend** and **Backend** of your application.

---

## 📦 **Part 1: Deploy Frontend (React App)**

### Option A: Deploy to Netlify (Recommended)

#### Step 1: Login to Netlify
1. Go to: https://app.netlify.com
2. Sign up or login with GitHub

#### Step 2: Deploy from GitHub
1. Click **"Add new site"** → **"Import an existing project"**
2. Choose **"Deploy with GitHub"**
3. Select your repository: `anuragthippani1/return_abuse_detection_system`
4. Configure build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm install --legacy-peer-deps && npm run build`
   - **Publish directory**: `frontend/build`
   - Click **"Deploy site"**

#### Step 3: Wait for Deployment
- Netlify will build and deploy automatically
- You'll get a URL like: `https://your-app-name.netlify.app`

---

### Option B: Deploy to Vercel (Alternative)

#### Step 1: Login to Vercel
1. Go to: https://vercel.com
2. Sign up or login with GitHub

#### Step 2: Import Project
1. Click **"Add New"** → **"Project"**
2. Import `anuragthippani1/return_abuse_detection_system`
3. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install --legacy-peer-deps && npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install --legacy-peer-deps`

#### Step 3: Deploy
- Click **"Deploy"**
- You'll get a URL like: `https://your-app-name.vercel.app`

---

## 🔧 **Part 2: Deploy Backend (Flask API)**

### Option A: Deploy to Render (Recommended)

#### Step 1: Login to Render
1. Go to: https://render.com
2. Sign up or login with GitHub

#### Step 2: Create New Web Service
1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository: `anuragthippani1/return_abuse_detection_system`
3. Configure:
   - **Name**: `return-abuse-api`
   - **Region**: Select closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`

#### Step 3: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:
```
PORT=5001
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=returns_db
MONGODB_COLLECTION=return_cases
```

#### Step 4: Deploy
- Click **"Create Web Service"**
- Render will deploy your backend
- You'll get a URL like: `https://return-abuse-api.onrender.com`

---

### Option B: Deploy to Railway (Alternative)

#### Step 1: Login to Railway
1. Go to: https://railway.app
2. Sign up or login with GitHub

#### Step 2: Deploy from GitHub
1. Click **"New Project"** → **"Deploy from GitHub repo"**
2. Select `anuragthippani1/return_abuse_detection_system`
3. Railway will auto-detect Flask
4. Add environment variables in the **Variables** tab:
   ```
   PORT=5001
   MONGODB_URI=your_mongodb_atlas_connection_string
   MONGODB_DB_NAME=returns_db
   MONGODB_COLLECTION=return_cases
   ```

#### Step 3: Configure
- Root directory: `backend`
- Start command: `python run.py`

---

### Option C: Deploy to Heroku

#### Step 1: Install Heroku CLI
```bash
brew tap heroku/brew && brew install heroku
```

#### Step 2: Login and Create App
```bash
heroku login
heroku create return-abuse-backend
```

#### Step 3: Deploy
```bash
cd backend
git subtree push --prefix backend heroku main
```

#### Step 4: Set Environment Variables
```bash
heroku config:set MONGODB_URI=your_mongodb_connection_string
heroku config:set MONGODB_DB_NAME=returns_db
heroku config:set MONGODB_COLLECTION=return_cases
```

---

## 🗄️ **Part 3: Setup MongoDB Atlas (Free Cloud Database)**

If you haven't already set up MongoDB Atlas:

#### Step 1: Create MongoDB Atlas Account
1. Go to: https://www.mongodb.com/cloud/atlas/register
2. Sign up for free

#### Step 2: Create Cluster
1. Click **"Build a Database"** → **"Free (M0)"**
2. Choose your cloud provider and region
3. Click **"Create Cluster"**

#### Step 3: Create Database User
1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Set username and password (save these!)
4. Give **"Read and write to any database"** permission

#### Step 4: Whitelist IP Address
1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for testing)
4. Click **"Confirm"**

#### Step 5: Get Connection String
1. Go back to **Database** → **"Connect"**
2. Choose **"Connect your application"**
3. Copy the connection string:
   ```
   mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Use this as your `MONGODB_URI` environment variable

---

## 🔗 **Part 4: Connect Frontend to Backend**

After deploying both:

1. Update `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.onrender.com/api';
   ```

2. Commit and push:
   ```bash
   git add frontend/src/services/api.js
   git commit -m "Update API URL to production backend"
   git push
   ```

3. Netlify/Vercel will auto-redeploy with the new backend URL

---

## ✅ **Quick Deployment Checklist**

- [ ] Frontend deployed to Netlify or Vercel
- [ ] Backend deployed to Render, Railway, or Heroku
- [ ] MongoDB Atlas cluster created and configured
- [ ] Environment variables set on backend deployment
- [ ] Frontend API URL updated to point to backend
- [ ] Test the deployed app!

---

## 🧪 **Testing Your Deployment**

1. Visit your frontend URL
2. Navigate to the Dashboard
3. You should see sample data loading
4. Test filters and interactions
5. Check browser console for any errors

---

## 🆘 **Troubleshooting**

### Frontend shows blank page
- Check browser console for errors
- Verify build completed successfully
- Check Network tab for failed API calls

### Backend API not responding
- Check backend logs on Render/Railway/Heroku
- Verify environment variables are set
- Test API directly: `https://your-backend-url.onrender.com/health`

### Database connection issues
- Verify MongoDB Atlas IP whitelist includes `0.0.0.0/0`
- Check database user has correct permissions
- Verify connection string is correct

---

## 📧 **Need Help?**

If you encounter issues:
1. Check deployment logs
2. Review this guide
3. Check the README.md for additional info

---

**Made with ♥ by Anurag Thippani**

