# 🚀 Deployment Guide

## Quick Deploy (Recommended for Beginners)

### Option 1: Render.com (FREE & EASY) ⭐

Perfect for full-stack apps, completely free tier.

#### Step 1: Set Up MongoDB Atlas (Free Database)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up and create a free cluster
3. Click "Connect" → "Connect your application"
4. Copy the connection string (looks like: `mongodb+srv://username:password@cluster0.mongodb.net/`)
5. Replace `<password>` with your password
6. Save this for later!

#### Step 2: Deploy Backend on Render

1. **Push your code to GitHub first!**

   ```bash
   cd /Users/anuragthippani/Documents/programs/Amazon
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin https://github.com/YOUR_USERNAME/return-abuse-detection.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `return-detection-backend`
     - **Root Directory**: `backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python run.py`
3. **Add Environment Variables:**

   - Click "Environment" tab
   - Add:
     ```
     MONGODB_URI = your_mongodb_atlas_connection_string
     MONGODB_DB_NAME = returns_db
     MONGODB_COLLECTION = return_cases
     ```

4. Click "Create Web Service"
5. Wait for deployment (5-10 minutes)
6. Copy your backend URL: `https://return-detection-backend.onrender.com`

#### Step 3: Deploy Frontend on Netlify

1. **Update frontend API URL:**

   ```bash
   cd /Users/anuragthippani/Documents/programs/Amazon/frontend/src/components
   ```

   Update `Dashboard.js`:

   ```javascript
   // Change this line:
   const API_BASE_URL = "http://localhost:5001/api";

   // To this (use your Render backend URL):
   const API_BASE_URL = "https://return-detection-backend.onrender.com/api";
   ```

2. **Commit changes:**

   ```bash
   git add .
   git commit -m "Update API URL for production"
   git push
   ```

3. **Deploy to Netlify:**

   - Go to https://netlify.com and sign up
   - Click "Add new site" → "Import an existing project"
   - Connect GitHub
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `frontend/build`
   - Click "Deploy"

4. Your site is live! 🎉
   - Frontend: `https://your-site-name.netlify.app`
   - Backend: `https://return-detection-backend.onrender.com`

---

## Option 2: Vercel (Frontend) + Render (Backend)

### Backend (Same as Option 1)

### Frontend on Vercel

```bash
cd /Users/anuragthippani/Documents/programs/Amazon/frontend

# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

Follow prompts and deploy!

---

## Option 3: Railway.app (Full-Stack in One Place)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect both backend and frontend
6. Add MongoDB service from Railway's marketplace (or use Atlas)
7. Deploy!

**Deployment URL**: `https://your-app.railway.app`

---

## Option 4: Heroku (Classic Approach)

### Prerequisites

```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Deploy Backend

```bash
cd /Users/anuragthippani/Documents/programs/Amazon/backend

# Login
heroku login

# Create app
heroku create return-detection-backend

# Add MongoDB (free tier)
heroku addons:create mongolab:sandbox

# Deploy
git init
git add .
git commit -m "Deploy to Heroku"
heroku git:remote -a return-detection-backend
git push heroku main

# Get your backend URL
heroku open
```

### Deploy Frontend

```bash
cd /Users/anuragthippani/Documents/programs/Amazon/frontend

# Update API URL in Dashboard.js to your Heroku backend URL

# Create Heroku app
heroku create return-detection-frontend

# Add buildpack
heroku buildpacks:set mars/create-react-app

# Deploy
git init
git add .
git commit -m "Deploy frontend"
heroku git:remote -a return-detection-frontend
git push heroku main
```

---

## Option 5: Docker Deployment

### Build and Run Locally with Docker

```bash
cd /Users/anuragthippani/Documents/programs/Amazon

# Build and run
docker-compose up --build

# Access:
# Frontend: http://localhost:80
# Backend: http://localhost:5001
```

### Deploy Docker to Cloud

**DigitalOcean App Platform:**

1. Push to GitHub
2. Go to https://cloud.digitalocean.com/apps
3. Create new app from GitHub
4. DigitalOcean auto-detects Dockerfile
5. Deploy!

**Google Cloud Run:**

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT-ID/return-detection

# Deploy
gcloud run deploy --image gcr.io/PROJECT-ID/return-detection
```

---

## Environment Variables

Create `.env` files for production:

### Backend `.env`

```env
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net/returns_db
MONGODB_DB_NAME=returns_db
MONGODB_COLLECTION=return_cases
FLASK_ENV=production
```

### Frontend `.env`

```env
REACT_APP_API_URL=https://your-backend-url.com/api
```

---

## 📊 Comparison of Deployment Options

| Platform             | Backend | Frontend | Database  | Free Tier  | Difficulty  |
| -------------------- | ------- | -------- | --------- | ---------- | ----------- |
| **Render**           | ✅      | ✅       | Use Atlas | ✅ Yes     | ⭐ Easy     |
| **Netlify + Render** | ✅      | ✅       | Use Atlas | ✅ Yes     | ⭐ Easy     |
| **Railway**          | ✅      | ✅       | ✅        | ✅ Yes     | ⭐ Easy     |
| **Vercel + Render**  | ✅      | ✅       | Use Atlas | ✅ Yes     | ⭐⭐ Medium |
| **Heroku**           | ✅      | ✅       | ✅        | ⚠️ Limited | ⭐⭐ Medium |
| **AWS**              | ✅      | ✅       | ✅        | ✅ Yes     | ⭐⭐⭐ Hard |
| **Docker**           | ✅      | ✅       | ✅        | Depends    | ⭐⭐⭐ Hard |

**Recommendation**: Use **Render + Netlify** for easiest free deployment! ⭐

---

## 🔧 Post-Deployment Checklist

- [ ] Backend is live and accessible
- [ ] Frontend is live and accessible
- [ ] Database connection works
- [ ] API calls from frontend to backend work
- [ ] CORS is properly configured
- [ ] Environment variables are set
- [ ] HTTPS is enabled
- [ ] Custom domain configured (optional)
- [ ] Add to your resume/portfolio!

---

## 🐛 Troubleshooting

### Issue: CORS errors

**Solution**: Add your frontend URL to CORS in `backend/app/__init__.py`:

```python
CORS(app, origins=["https://your-frontend-url.netlify.app"])
```

### Issue: API calls failing

**Solution**: Check that API_BASE_URL in frontend points to correct backend URL

### Issue: Database connection failed

**Solution**: Verify MongoDB Atlas connection string and whitelist IP (0.0.0.0/0 for all)

### Issue: Build failing

**Solution**: Check logs, ensure all dependencies in requirements.txt and package.json

---

## 📱 Mobile App (Bonus)

Want a mobile app? Use React Native with Expo:

```bash
npx create-expo-app return-detection-mobile
# Reuse your API calls from frontend
expo start
```

---

## 🎉 You're Live!

Share your deployed app:

- Add link to LinkedIn
- Add to your resume
- Share on Twitter/X
- Add to portfolio website

**Example URLs:**

- Frontend: https://return-detection.netlify.app
- Backend API: https://return-detection-backend.onrender.com/api
- GitHub: https://github.com/yourusername/return-abuse-detection

---

Need help? Check platform documentation:

- Render: https://render.com/docs
- Netlify: https://docs.netlify.com
- Vercel: https://vercel.com/docs
- Railway: https://docs.railway.app
