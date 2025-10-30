# 🔧 TROUBLESHOOTING GUIDE - PLATEFORME XP WEB VERSION

## 🚨 COMMON ISSUES & SOLUTIONS

### ❌ Issue 1: Port Already in Use (WinError 10048)

**Error Message:**
```
OSError: [WinError 10048] Une seule utilisation de chaque adresse de socket...
```

**Solution A - Use START_WEB.bat (Automatic):**
```bash
# Double-click this file:
START_WEB.bat

# It automatically:
# - Kills existing processes on ports 5000 & 3000
# - Starts backend
# - Starts frontend
# - Opens browser
```

**Solution B - Manual Cleanup:**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /F /PID <PID_NUMBER>

# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /F /PID <PID_NUMBER>

# Then start normally
cd backend
python run.py

# In another terminal:
cd frontend
npm start
```

**Solution C - Change Ports:**
Edit `backend/run.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Changed from 5000
```

Edit `frontend/package.json`:
```json
"start": "set PORT=3001 && react-scripts start"  # Changed from 3000
```

---

### ❌ Issue 2: Backend Won't Start

**Error: Module not found**

**Solution:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Error: Database file missing**

**Solution:**
```bash
cd backend
# Database will be created automatically on first run
python run.py
```

**Error: Import errors**

**Solution:**
```bash
cd backend
# Reinstall all dependencies
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

---

### ❌ Issue 3: Frontend Won't Start

**Error: npm not found**

**Solution:**
- Install Node.js from https://nodejs.org/
- Restart terminal
- Try again

**Error: Module not found**

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

**Error: Port 3000 already in use**

**Solution:**
```bash
# Kill existing process
netstat -ano | findstr :3000
taskkill /F /PID <PID>

# Or change port in package.json:
"start": "set PORT=3001 && react-scripts start"
```

---

### ❌ Issue 4: Can't Login

**Symptom:** Invalid credentials or no response

**Solution A - Check Backend:**
```bash
# Test if backend is running
curl http://localhost:5000/health

# Should return: {"status": "healthy"}
```

**Solution B - Clear Browser Data:**
```
1. Open DevTools (F12)
2. Go to Application tab
3. Clear all localStorage
4. Refresh page
```

**Solution C - Create New Account:**
```
1. Click "Créer un compte" on login page
2. Fill form with:
   - Nom: Your Name
   - Email: youremail@test.com
   - Password: yourpassword
   - Promo: B2 (or any)
3. Login with new credentials
```

**Default Test Account:**
```
Email:    test
Password: test123
```

---

### ❌ Issue 5: CORS Errors

**Error in browser console:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
Backend already has CORS enabled. Check:

1. Backend is running on port 5000
2. Frontend is running on port 3000
3. Clear browser cache
4. Restart both servers

If issue persists, edit `backend/app/__init__.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

### ❌ Issue 6: Database Issues

**Error: Database locked or corrupted**

**Solution A - Reset Database:**
```bash
cd backend
rm plateforme_xp.db
python run.py
# Database will be recreated with empty tables
```

**Solution B - Import Sample Data:**
```bash
cd backend
rm plateforme_xp.db
python migrate_json_to_db.py
# Imports data from plateforme_data.json
```

---

### ❌ Issue 7: Chat Not Working

**Symptom:** Messages don't appear or don't send

**Solution:**

1. Check backend is running
2. Messages refresh every 5 seconds (auto-refresh)
3. Check browser console for errors (F12)
4. Try logging out and back in

**Manual Test:**
```bash
# Test chat API directly
curl -X POST http://localhost:5000/api/chat/messages \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

---

### ❌ Issue 8: Projects Not Updating

**Symptom:** Changes don't save or XP not updating

**Solution:**

1. Check browser console for errors
2. Verify backend is running
3. Clear localStorage and login again
4. Check database file exists: `backend/plateforme_xp.db`

---

### ❌ Issue 9: Leaderboard Empty

**Symptom:** No students shown in ranking

**Solution:**

1. Create some users first
2. Complete projects to gain XP
3. Leaderboard shows users with XP > 0
4. Data is cached for 60 seconds

**Force refresh:**
```
Wait 1 minute or restart backend
```

---

### ❌ Issue 10: White Screen / Nothing Shows

**Solution:**

1. Check browser console (F12)
2. Verify both servers are running:
   - Backend: http://localhost:5000/health
   - Frontend: http://localhost:3000
3. Check network tab for failed requests
4. Clear browser cache
5. Try incognito mode

---

## 🔍 DEBUGGING CHECKLIST

### Backend Health Check:
```bash
curl http://localhost:5000/health
# Expected: {"status": "healthy", "message": "Plateforme XP API is running"}
```

### Frontend Health Check:
```
Open: http://localhost:3000
# Expected: Login page loads
```

### Check Logs:
- **Backend**: Look at terminal where `python run.py` is running
- **Frontend**: Look at terminal where `npm start` is running
- **Browser**: Press F12, check Console and Network tabs

---

## 🛠️ COMPLETE RESET (Last Resort)

If nothing works, complete reset:

```bash
# 1. Stop all processes
netstat -ano | findstr :5000
taskkill /F /PID <PID>
netstat -ano | findstr :3000
taskkill /F /PID <PID>

# 2. Clean backend
cd backend
rm plateforme_xp.db
pip install -r requirements.txt

# 3. Clean frontend
cd ../frontend
rm -rf node_modules package-lock.json
npm install

# 4. Start fresh
cd ..
START_WEB.bat
```

---

## 📞 GETTING HELP

### Check These First:
1. ✅ Node.js installed? `node --version`
2. ✅ Python installed? `python --version`
3. ✅ Backend running? http://localhost:5000/health
4. ✅ Frontend running? http://localhost:3000
5. ✅ Browser console errors? (F12)

### Common Error Patterns:

**Network Errors (ERR_CONNECTION_REFUSED):**
- Backend not running
- Wrong port number
- Solution: Start backend with `python run.py`

**401 Unauthorized:**
- Token expired or missing
- Solution: Logout and login again

**500 Internal Server Error:**
- Backend crash or database issue
- Solution: Check backend terminal for errors

**404 Not Found:**
- Wrong API endpoint
- Solution: Check URL in browser console

---

## 🎯 VERIFICATION STEPS

After starting, verify everything works:

1. ✅ **Login Page Loads**
   - Go to http://localhost:3000
   - See login form

2. ✅ **Can Login**
   - Use: test / test123
   - Redirects to dashboard

3. ✅ **Dashboard Shows Data**
   - See your profile
   - See XP and level
   - See project stats

4. ✅ **Projects Work**
   - Click "Projets" or sidebar
   - Can create new project
   - Can edit/delete projects

5. ✅ **Chat Works**
   - Go to Chat
   - Send a message
   - See message appear

6. ✅ **Other Features**
   - Leaderboard shows ranking
   - Profile can be edited
   - Badges show locked/unlocked
   - Calendar shows events

---

## 🔧 PERFORMANCE TIPS

### Slow Loading?

1. **Check Database Size:**
   ```bash
   cd backend
   dir plateforme_xp.db
   # If > 100MB, consider cleanup
   ```

2. **Clear Browser Cache:**
   - Chrome: Ctrl+Shift+Del
   - Select "Cached images and files"
   - Clear

3. **Disable Browser Extensions:**
   - Try incognito mode
   - Some extensions block requests

4. **Check RAM Usage:**
   - Close other apps
   - Restart browser

---

## 📚 USEFUL COMMANDS

### Windows:
```bash
# Check port usage
netstat -ano | findstr :5000
netstat -ano | findstr :3000

# Kill process by PID
taskkill /F /PID <PID>

# Check Python version
python --version

# Check Node version
node --version

# Check npm version
npm --version
```

### Testing:
```bash
# Test backend health
curl http://localhost:5000/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test\",\"password\":\"test123\"}"
```

---

## ✅ QUICK FIX SUMMARY

| Problem | Quick Fix |
|---------|-----------|
| Port in use | Run `START_WEB.bat` |
| Can't login | Use `test / test123` |
| Backend error | `pip install -r requirements.txt` |
| Frontend error | `npm install` |
| Database error | Delete `plateforme_xp.db` |
| CORS error | Restart both servers |
| White screen | Clear browser cache + F12 console |
| No data | Create account + add projects |

---

## 🎉 SUCCESS INDICATORS

You'll know everything works when:

✅ Backend terminal shows: "Running on http://0.0.0.0:5000"
✅ Frontend terminal shows: "Compiled successfully!"
✅ Browser opens to http://localhost:3000
✅ Login page loads with form
✅ Can login with test/test123
✅ Dashboard shows your profile & XP
✅ All navigation links work
✅ No red errors in browser console (F12)

---

**Still having issues? Check the backend terminal for specific error messages!**
