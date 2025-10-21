# PLATEFORME XP - COMPLETE SETUP & DEPLOYMENT GUIDE
# ==================================================

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Detailed Setup Instructions](#detailed-setup-instructions)
3. [File Structure](#file-structure)
4. [Environment Configuration](#environment-configuration)
5. [Running the Application](#running-the-application)
6. [Testing Features](#testing-features)
7. [Deployment Guide](#deployment-guide)
8. [Troubleshooting](#troubleshooting)
9. [API Documentation](#api-documentation)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- MongoDB running (local or cloud)
- VS Code (recommended)

### Installation Steps

1. **Create project directory and extract files**
   - Use the provided code from PART 1-5 documents
   - Create each file in its respective location

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your settings
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Open browser**
   ```
   http://localhost:3000
   ```

---

## 📦 Detailed Setup Instructions

### Step 1: Create Project Structure

Create the following directory structure:

```
plateforme-xp/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── login/
│   │   │   │   │   └── route.ts
│   │   │   │   ├── register/
│   │   │   │   │   └── route.ts
│   │   │   │   └── me/
│   │   │   │       └── route.ts
│   │   │   ├── xp/
│   │   │   │   ├── route.ts
│   │   │   │   └── add/
│   │   │   │       └── route.ts
│   │   │   ├── badges/
│   │   │   │   └── route.ts
│   │   │   ├── events/
│   │   │   │   ├── route.ts
│   │   │   │   └── [id]/
│   │   │   │       └── route.ts
│   │   │   ├── peers/
│   │   │   │   ├── route.ts
│   │   │   │   └── request/
│   │   │   │       └── route.ts
│   │   │   └── resources/
│   │   │       └── route.ts
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── profile/
│   │   │   └── page.tsx
│   │   ├── calendar/
│   │   │   └── page.tsx
│   │   ├── tutoring/
│   │   │   └── page.tsx
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── gamification/
│   │   │   ├── XPBar.tsx
│   │   │   ├── LevelDisplay.tsx
│   │   │   └── BadgeGallery.tsx
│   │   ├── calendar/
│   │   │   └── EventCalendar.tsx
│   │   ├── tutoring/
│   │   │   ├── TutorCard.tsx
│   │   │   └── ChatBox.tsx
│   │   └── layout/
│   │       └── Header.tsx
│   ├── lib/
│   │   ├── mongodb.ts
│   │   ├── auth.ts
│   │   └── constants.ts
│   ├── models/
│   │   ├── User.ts
│   │   ├── Event.ts
│   │   ├── TutoringSession.ts
│   │   └── Resource.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       ├── xp.ts
│       └── badges.ts
├── public/
├── .env.local.example
├── .env.local (you create this)
├── .eslintrc.json
├── .prettierrc
├── .gitignore
├── next.config.js
├── package.json
├── postcss.config.js
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

### Step 2: Copy All Code Files

Use the code provided in the following documents:
- **PART 1**: Types, Models, Utils, Config files
- **PART 2**: API Routes for Auth, XP, Events, Peers, Resources
- **PART 3**: Frontend Components (Auth, Gamification)
- **PART 4**: Dashboard, Calendar, Header
- **PART 5**: Tutoring, Profile, Final configuration

### Step 3: Install Dependencies

Run in the project root:

```bash
npm install
```

This will install all dependencies listed in package.json:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Mongoose
- FullCalendar
- Socket.IO
- bcryptjs
- jsonwebtoken
- date-fns
- lucide-react
- framer-motion

### Step 4: Setup MongoDB

**Option A: Local MongoDB**
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath /path/to/data
```

**Option B: MongoDB Atlas (Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Whitelist your IP address
5. Create database user

### Step 5: Configure Environment Variables

Create `.env.local` file:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/plateforme-xp
# OR for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/plateforme-xp

# Authentication (IMPORTANT: Change this!)
JWT_SECRET=your-super-secret-jwt-key-min-32-characters-long-change-in-production
JWT_EXPIRES_IN=7d

# App Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

⚠️ **IMPORTANT**: 
- Change `JWT_SECRET` to a strong random string (min 32 characters)
- Never commit `.env.local` to version control

---

## 🏃 Running the Application

### Development Mode

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Production Build

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Code Quality

```bash
# Run linter
npm run lint

# Format code
npm run format
```

---

## 🧪 Testing Features

### 1. Registration & Authentication

1. Navigate to `http://localhost:3000`
2. Click "Register" tab
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Select subjects (optional)
4. Click "Register"
5. You should be redirected to dashboard

### 2. Dashboard

After login, you should see:
- XP Bar showing Level 1 and initial XP
- "First Steps" badge (awarded on registration)
- Quick stats sidebar
- Upcoming events (if any)
- Quick action buttons

### 3. XP System

Test XP gain:
```bash
# Use API to add XP (replace with actual token)
curl -X POST http://localhost:3000/api/xp/add \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "reason": "Test XP"}'
```

### 4. Calendar

1. Navigate to Calendar page
2. View events in month/week/day view
3. Click on events to see details
4. Events are color-coded by type

### 5. Tutoring System

1. Go to Tutoring page
2. Browse available tutors
3. Filter by subject
4. Click "Request Session" to send tutoring request
5. View shared resources in sidebar

### 6. Profile

1. Navigate to Profile page
2. View your stats, badges, and progress
3. Click "Edit" to update profile information
4. Toggle "Available for tutoring" status
5. Add/remove subjects

---

## 🌐 Deployment Guide

### Deploy to Vercel (Recommended)

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_REPO_URL
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - Configure environment variables
   - Deploy!

3. **Set Environment Variables in Vercel**
   - Go to Project Settings > Environment Variables
   - Add all variables from `.env.local`

### Deploy to Other Platforms

**Netlify:**
- Similar to Vercel
- Use `netlify.toml` for configuration

**Railway:**
- Excellent for full-stack apps
- Automatically detects Next.js
- Built-in MongoDB hosting option

**Docker:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

---

## 🔧 Troubleshooting

### Common Issues

**1. MongoDB Connection Error**
```
Error: connect ECONNREFUSED 127.0.0.1:27017
```
**Solution**: 
- Ensure MongoDB is running
- Check connection string in `.env.local`
- Verify network connectivity

**2. JWT Secret Error**
```
Error: JWT secret not configured
```
**Solution**: 
- Add `JWT_SECRET` to `.env.local`
- Ensure it's at least 32 characters

**3. Module Not Found Errors**
```
Module not found: Can't resolve '@/...'
```
**Solution**:
```bash
npm install
# Clear cache
rm -rf .next
npm run dev
```

**4. TypeScript Errors**
```
Type errors found
```
**Solution**:
```bash
npm run lint
# Fix type issues
```

**5. Build Errors**
```
Error: Build failed
```
**Solution**:
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Performance Issues

**Slow Page Load**
- Check MongoDB connection latency
- Use MongoDB indexes
- Enable Next.js caching

**High Memory Usage**
- Limit concurrent connections
- Implement pagination
- Use lazy loading for components

---

## 📚 API Documentation

### Authentication Endpoints

**POST /api/auth/register**
```json
Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "subjects": ["Mathematics", "Physics"]
}

Response:
{
  "success": true,
  "data": {
    "user": { ... },
    "token": "jwt_token_here"
  }
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "john@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "data": {
    "user": { ... },
    "token": "jwt_token_here"
  }
}
```

**GET /api/auth/me**
```
Headers: Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": { user_object }
}
```

### XP & Gamification

**GET /api/xp**
- Get user XP and level information
- Requires authentication

**POST /api/xp/add**
```json
Request:
{
  "amount": 100,
  "reason": "Completed assignment"
}
```

**GET /api/badges**
- Get user's earned badges
- Requires authentication

### Events

**GET /api/events**
- Query params: `start`, `end`, `type`
- Returns filtered events

**POST /api/events**
```json
Request:
{
  "title": "Math Workshop",
  "description": "Learn calculus",
  "start": "2024-01-15T10:00:00",
  "end": "2024-01-15T12:00:00",
  "type": "workshop",
  "location": "Room 101",
  "xpReward": 50
}
```

**GET /api/events/[id]**
- Get specific event details

**PUT /api/events/[id]**
- Update event (organizer only)

**DELETE /api/events/[id]**
- Delete event (organizer only)

### Peer Tutoring

**GET /api/peers**
- Query params: `subject`
- Get available tutors

**POST /api/peers/request**
```json
Request:
{
  "tutorId": "user_id",
  "subject": "Mathematics",
  "scheduledAt": "2024-01-15T14:00:00",
  "notes": "Need help with calculus"
}
```

### Resources

**GET /api/resources**
- Query params: `subject`, `type`
- Get shared resources

**POST /api/resources**
```json
Request:
{
  "title": "Calculus Notes",
  "description": "Complete notes on limits",
  "type": "document",
  "url": "https://...",
  "subject": "Mathematics",
  "sharedWith": ["user_id1", "user_id2"]
}
```

---

## 🎯 Feature Roadmap

### Phase 1 (MVP) - ✅ Complete
- User authentication
- XP and leveling system
- Badge awards
- Event calendar
- Peer tutoring requests
- Resource sharing
- Responsive design

### Phase 2 (Enhancements)
- [ ] Real-time chat with Socket.IO
- [ ] WebRTC video calls
- [ ] Push notifications
- [ ] Advanced search and filters
- [ ] User profiles with avatars
- [ ] Activity feed
- [ ] Leaderboards

### Phase 3 (Advanced)
- [ ] AI-powered tutor matching
- [ ] Learning path recommendations
- [ ] Analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with LMS
- [ ] Payment system
- [ ] Certification system

---

## 📞 Support

For issues and questions:
1. Check troubleshooting section
2. Review API documentation
3. Check MongoDB connection
4. Verify environment variables
5. Clear cache and rebuild

---

## 📄 License

MIT License - Free to use for educational purposes

---

**Built with ❤️ using Next.js 14, TypeScript, and Tailwind CSS**

Project created for educational purposes as an MVP demonstration.
