# ✅ PLATEFORME XP - INSTALLATION CHECKLIST

## Quick Installation Guide

Follow this checklist to set up your Plateforme XP project step by step.

---

## 📋 Pre-Installation Checklist

- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm or yarn installed (`npm --version`)
- [ ] MongoDB installed OR MongoDB Atlas account created
- [ ] VS Code installed (recommended)
- [ ] Git installed (optional, for version control)

---

## 🔧 Step-by-Step Installation

### Step 1: Create Project Structure (5 min)

```bash
# Create main project directory
mkdir plateforme-xp
cd plateforme-xp

# Create source directories
mkdir -p src/app/api/auth/register
mkdir -p src/app/api/auth/login
mkdir -p src/app/api/auth/me
mkdir -p src/app/api/xp/add
mkdir -p src/app/api/badges
mkdir -p src/app/api/events/[id]
mkdir -p src/app/api/peers/request
mkdir -p src/app/api/resources
mkdir -p src/app/dashboard
mkdir -p src/app/profile
mkdir -p src/app/calendar
mkdir -p src/app/tutoring
mkdir -p src/components/auth
mkdir -p src/components/gamification
mkdir -p src/components/calendar
mkdir -p src/components/tutoring
mkdir -p src/components/layout
mkdir -p src/lib
mkdir -p src/models
mkdir -p src/types
mkdir -p src/utils
mkdir public
```

- [ ] Directories created

### Step 2: Copy Configuration Files (10 min)

Copy these files from the documentation to your project root:

- [ ] `package.json`
- [ ] `tsconfig.json`
- [ ] `next.config.js`
- [ ] `tailwind.config.ts`
- [ ] `postcss.config.js`
- [ ] `.eslintrc.json`
- [ ] `.prettierrc`
- [ ] `.env.local.example`
- [ ] `.gitignore`

### Step 3: Copy Source Code - Part 1 (15 min)

From **PLATEFORME_XP_CODE_PART1.md**, copy:

- [ ] `src/types/index.ts`
- [ ] `src/lib/constants.ts`
- [ ] `src/lib/mongodb.ts`
- [ ] `src/lib/auth.ts`
- [ ] `src/utils/xp.ts`
- [ ] `src/utils/badges.ts`
- [ ] `src/models/User.ts`
- [ ] `src/models/Event.ts`
- [ ] `src/models/TutoringSession.ts`
- [ ] `src/models/Resource.ts`

### Step 4: Copy Source Code - Part 2 (15 min)

From **PLATEFORME_XP_CODE_PART2.md**, copy:

- [ ] `src/app/api/auth/register/route.ts`
- [ ] `src/app/api/auth/login/route.ts`
- [ ] `src/app/api/auth/me/route.ts`
- [ ] `src/app/api/xp/route.ts`
- [ ] `src/app/api/xp/add/route.ts`
- [ ] `src/app/api/badges/route.ts`
- [ ] `src/app/api/events/route.ts`
- [ ] `src/app/api/events/[id]/route.ts`
- [ ] `src/app/api/peers/route.ts`
- [ ] `src/app/api/peers/request/route.ts`
- [ ] `src/app/api/resources/route.ts`

### Step 5: Copy Source Code - Part 3 (15 min)

From **PLATEFORME_XP_CODE_PART3.md**, copy:

- [ ] `src/app/globals.css`
- [ ] `src/app/layout.tsx`
- [ ] `src/app/page.tsx`
- [ ] `src/components/auth/LoginForm.tsx`
- [ ] `src/components/auth/RegisterForm.tsx`
- [ ] `src/components/gamification/XPBar.tsx`
- [ ] `src/components/gamification/BadgeGallery.tsx`
- [ ] `src/components/gamification/LevelDisplay.tsx`

### Step 6: Copy Source Code - Part 4 (15 min)

From **PLATEFORME_XP_CODE_PART4.md**, copy:

- [ ] `src/components/layout/Header.tsx`
- [ ] `src/app/dashboard/page.tsx`
- [ ] `src/components/calendar/EventCalendar.tsx`
- [ ] `src/app/calendar/page.tsx`

### Step 7: Copy Source Code - Part 5 (15 min)

From **PLATEFORME_XP_CODE_PART5.md**, copy:

- [ ] `src/components/tutoring/TutorCard.tsx`
- [ ] `src/components/tutoring/ChatBox.tsx`
- [ ] `src/app/tutoring/page.tsx`
- [ ] `src/app/profile/page.tsx`

### Step 8: Install Dependencies (5 min)

```bash
npm install
```

**Expected packages** (check package.json):
- next, react, react-dom
- mongoose
- bcryptjs, jsonwebtoken
- socket.io, socket.io-client
- @fullcalendar/* packages
- date-fns, lucide-react, framer-motion
- TypeScript and type definitions
- Tailwind CSS, PostCSS, Autoprefixer
- ESLint, Prettier

- [ ] Dependencies installed successfully
- [ ] No error messages

### Step 9: Configure Environment (5 min)

1. Copy environment template:
```bash
cp .env.local.example .env.local
```

2. Edit `.env.local` with your values:

```env
# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017/plateforme-xp
# OR for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/plateforme-xp

# JWT Secret (IMPORTANT: Use a strong random string!)
JWT_SECRET=your-super-secret-jwt-key-minimum-32-characters-long
JWT_EXPIRES_IN=7d

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Important**: 
- [ ] MongoDB URI configured
- [ ] JWT_SECRET set (minimum 32 characters)
- [ ] APP_URL correct

### Step 10: Start MongoDB (if local)

**For local MongoDB**:
```bash
# Windows
net start MongoDB

# macOS/Linux
brew services start mongodb-community
# OR
sudo systemctl start mongod
```

**For MongoDB Atlas**:
- [ ] Cluster created
- [ ] Database user created
- [ ] IP whitelist configured
- [ ] Connection string copied to .env.local

- [ ] MongoDB running and accessible

### Step 11: Run Development Server (2 min)

```bash
npm run dev
```

Expected output:
```
▲ Next.js 14.x.x
- Local:        http://localhost:3000
- Ready in X.Xs
```

- [ ] Server started without errors
- [ ] No compilation errors
- [ ] MongoDB connection successful

### Step 12: Test in Browser (5 min)

1. Open browser: http://localhost:3000

2. Test registration:
   - [ ] Registration form loads
   - [ ] Can create new account
   - [ ] Redirects to dashboard after signup

3. Test login:
   - [ ] Can login with created account
   - [ ] Token stored in localStorage
   - [ ] Dashboard displays correctly

4. Test features:
   - [ ] Dashboard shows XP bar and badges
   - [ ] Calendar page loads
   - [ ] Tutoring page displays tutors
   - [ ] Profile page shows user info

---

## 🔍 Verification Checklist

### Files Created
- [ ] All 45+ source files created
- [ ] All configuration files in place
- [ ] .env.local configured
- [ ] node_modules directory exists

### Build & Run
- [ ] No TypeScript errors
- [ ] No ESLint errors
- [ ] Development server runs
- [ ] No console errors in browser

### Database
- [ ] MongoDB connected
- [ ] User collection created on registration
- [ ] Data persists between restarts

### Features Working
- [ ] User registration works
- [ ] User login works
- [ ] XP system calculates correctly
- [ ] Badges awarded on registration
- [ ] Dashboard displays all sections
- [ ] Calendar renders
- [ ] Tutoring page shows UI
- [ ] Profile page editable

---

## 🎯 Post-Installation Tasks

### Immediate
- [ ] Create test user accounts
- [ ] Add sample events to calendar
- [ ] Test XP addition via API
- [ ] Verify badge awards

### Optional
- [ ] Set up Git repository
- [ ] Create initial commit
- [ ] Configure IDE extensions
- [ ] Set up debugging

### Customization
- [ ] Modify color scheme in tailwind.config.ts
- [ ] Update app name and branding
- [ ] Add custom badges
- [ ] Configure XP rewards

---

## 🐛 Troubleshooting

### Common Issues

**npm install fails**
```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```
- [ ] Fixed

**MongoDB connection error**
- Check MongoDB is running
- Verify connection string in .env.local
- Check network connectivity
- Whitelist IP in MongoDB Atlas
- [ ] Fixed

**Port 3000 already in use**
```bash
# Use different port
PORT=3001 npm run dev
```
- [ ] Fixed

**TypeScript errors**
- Ensure all files copied correctly
- Check tsconfig.json is present
- Run: `npx tsc --noEmit` to see all errors
- [ ] Fixed

**Module not found errors**
- Verify file paths match exactly
- Check import statements
- Ensure all files created in correct directories
- [ ] Fixed

---

## 📞 Need Help?

1. **Check documentation**:
   - SETUP_GUIDE.md (troubleshooting section)
   - QUICK_REFERENCE.md (API reference)
   - DOCUMENTATION_INDEX.md (find right doc)

2. **Verify setup**:
   - All files copied correctly
   - Environment variables set
   - MongoDB accessible
   - Dependencies installed

3. **Test incrementally**:
   - Start with one feature
   - Test each API endpoint
   - Check browser console
   - Review server logs

---

## ✅ Installation Complete!

When all items are checked:

✨ **Your Plateforme XP MVP is ready to use!**

Next steps:
1. Explore all features
2. Customize to your needs
3. Add sample data
4. Deploy to production (see SETUP_GUIDE.md)

---

## 📊 Installation Time Estimates

- **Manual Setup**: 1.5 - 2 hours
- **With Copy/Paste**: 30 - 45 minutes
- **Experienced Developer**: 15 - 30 minutes

---

**Installation Date**: _____________

**Installed By**: _____________

**MongoDB Type**: ☐ Local  ☐ MongoDB Atlas

**Status**: ☐ Complete  ☐ In Progress  ☐ Issues

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________

---

**Ready to start building? Let's go! 🚀**
