# PLATEFORME XP - FRONTEND COMPONENTS (PART 3)
# =============================================

## FILE: src/app/globals.css
## ==========================

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* FullCalendar Custom Styles */
.fc {
  font-family: inherit;
}

.fc-button {
  @apply bg-primary-600 hover:bg-primary-700 text-white border-none;
}

.fc-event {
  @apply cursor-pointer transition-transform hover:scale-105;
}
```

## FILE: src/app/layout.tsx
## =========================

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Plateforme XP - Gamified Learning Platform',
  description: 'A gamified learning platform with XP tracking, events, and peer tutoring',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

## FILE: src/app/page.tsx
## ======================

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import LoginForm from '@/components/auth/LoginForm';
import RegisterForm from '@/components/auth/RegisterForm';

export default function Home() {
  const [isLogin, setIsLogin] = useState(true);
  const router = useRouter();

  const handleAuthSuccess = (token: string) => {
    localStorage.setItem('token', token);
    router.push('/dashboard');
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-primary-50 via-secondary-50 to-primary-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Welcome to <span className="text-primary-600">Plateforme XP</span>
            </h1>
            <p className="text-xl text-gray-600 mb-2">
              Your Gamified Learning Journey Starts Here
            </p>
            <p className="text-gray-500">
              Track XP, earn badges, attend events, and connect with peers
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Features */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">Features</h2>
              <ul className="space-y-4">
                <li className="flex items-start">
                  <span className="text-3xl mr-3">🎮</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">Gamification</h3>
                    <p className="text-gray-600 text-sm">
                      Earn XP, level up, and collect achievement badges
                    </p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-3xl mr-3">📅</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">Event Calendar</h3>
                    <p className="text-gray-600 text-sm">
                      Stay organized with an interactive event calendar
                    </p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-3xl mr-3">👥</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">Peer Tutoring</h3>
                    <p className="text-gray-600 text-sm">
                      Connect with tutors and share resources
                    </p>
                  </div>
                </li>
                <li className="flex items-start">
                  <span className="text-3xl mr-3">💬</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">Real-time Chat</h3>
                    <p className="text-gray-600 text-sm">
                      Communicate instantly with your peers
                    </p>
                  </div>
                </li>
              </ul>
            </div>

            {/* Auth Forms */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="flex mb-6 border-b">
                <button
                  onClick={() => setIsLogin(true)}
                  className={`flex-1 py-2 text-center font-semibold transition-colors ${
                    isLogin
                      ? 'text-primary-600 border-b-2 border-primary-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => setIsLogin(false)}
                  className={`flex-1 py-2 text-center font-semibold transition-colors ${
                    !isLogin
                      ? 'text-primary-600 border-b-2 border-primary-600'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Register
                </button>
              </div>

              {isLogin ? (
                <LoginForm onSuccess={handleAuthSuccess} />
              ) : (
                <RegisterForm onSuccess={handleAuthSuccess} />
              )}
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-3xl font-bold text-primary-600">500+</div>
              <div className="text-gray-600">Active Students</div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-3xl font-bold text-secondary-600">100+</div>
              <div className="text-gray-600">Events Monthly</div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-3xl font-bold text-primary-600">1000+</div>
              <div className="text-gray-600">Study Sessions</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
```

## FILE: src/components/auth/LoginForm.tsx
## ========================================

```typescript
'use client';

import { useState } from 'react';

interface LoginFormProps {
  onSuccess: (token: string) => void;
}

export default function LoginForm({ onSuccess }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        onSuccess(data.data.token);
      } else {
        setError(data.error || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:bg-gray-400"
      >
        {loading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

## FILE: src/components/auth/RegisterForm.tsx
## ===========================================

```typescript
'use client';

import { useState } from 'react';
import { SUBJECTS } from '@/lib/constants';

interface RegisterFormProps {
  onSuccess: (token: string) => void;
}

export default function RegisterForm({ onSuccess }: RegisterFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    subjects: [] as string[],
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
          subjects: formData.subjects,
        }),
      });

      const data = await response.json();

      if (data.success) {
        onSuccess(data.data.token);
      } else {
        setError(data.error || 'Registration failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleSubject = (subject: string) => {
    setFormData((prev) => ({
      ...prev,
      subjects: prev.subjects.includes(subject)
        ? prev.subjects.filter((s) => s !== subject)
        : [...prev.subjects, subject],
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Full Name
        </label>
        <input
          type="text"
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <div>
        <label htmlFor="reg-email" className="block text-sm font-medium text-gray-700 mb-1">
          Email
        </label>
        <input
          type="email"
          id="reg-email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <div>
        <label htmlFor="reg-password" className="block text-sm font-medium text-gray-700 mb-1">
          Password
        </label>
        <input
          type="password"
          id="reg-password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <div>
        <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-1">
          Confirm Password
        </label>
        <input
          type="password"
          id="confirm-password"
          value={formData.confirmPassword}
          onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Subjects (Optional)
        </label>
        <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto p-2 border border-gray-300 rounded-lg">
          {SUBJECTS.map((subject) => (
            <label key={subject} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.subjects.includes(subject)}
                onChange={() => toggleSubject(subject)}
                className="rounded text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700">{subject}</span>
            </label>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:bg-gray-400"
      >
        {loading ? 'Creating Account...' : 'Register'}
      </button>
    </form>
  );
}
```

## FILE: src/components/gamification/XPBar.tsx
## ============================================

```typescript
'use client';

import { useEffect, useState } from 'react';
import { getXPToNextLevel, formatXP } from '@/utils/xp';

interface XPBarProps {
  xp: number;
  level: number;
}

export default function XPBar({ xp, level }: XPBarProps) {
  const [progress, setProgress] = useState(0);
  const xpInfo = getXPToNextLevel(xp);

  useEffect(() => {
    const timer = setTimeout(() => {
      setProgress(xpInfo.progressPercentage);
    }, 100);
    return () => clearTimeout(timer);
  }, [xpInfo.progressPercentage]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-2">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">Level {level}</h3>
          <p className="text-sm text-gray-600">{formatXP(xp)} XP</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Next Level</p>
          <p className="text-sm font-semibold text-primary-600">
            {formatXP(xpInfo.xpToNextLevel)} XP to go
          </p>
        </div>
      </div>

      <div className="relative w-full h-4 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="absolute top-0 left-0 h-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-1000 ease-out"
          style={{ width: `${progress}%` }}
        >
          <div className="absolute inset-0 bg-white opacity-20 animate-pulse"></div>
        </div>
      </div>

      <div className="flex justify-between mt-2 text-xs text-gray-500">
        <span>{formatXP(xpInfo.currentLevelXP)}</span>
        <span>{Math.round(progress)}%</span>
        <span>{formatXP(xpInfo.nextLevelXP)}</span>
      </div>
    </div>
  );
}
```

## FILE: src/components/gamification/BadgeGallery.tsx
## ==================================================

```typescript
'use client';

import { IBadge } from '@/types';
import { format } from 'date-fns';

interface BadgeGalleryProps {
  badges: IBadge[];
}

export default function BadgeGallery({ badges }: BadgeGalleryProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Badges ({badges.length})
      </h3>

      {badges.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <p>No badges earned yet</p>
          <p className="text-sm mt-2">
            Keep learning and completing activities to earn badges!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {badges.map((badge) => (
            <div
              key={badge._id}
              className="group relative bg-gradient-to-br from-primary-50 to-secondary-50 rounded-lg p-4 text-center hover:shadow-lg transition-all cursor-pointer"
            >
              <div className="text-4xl mb-2 transform group-hover:scale-110 transition-transform">
                {badge.icon}
              </div>
              <h4 className="font-semibold text-sm text-gray-800 mb-1">
                {badge.name}
              </h4>
              <p className="text-xs text-gray-600 mb-2">{badge.description}</p>
              <p className="text-xs text-gray-500">
                {format(new Date(badge.awardedAt), 'MMM d, yyyy')}
              </p>

              {/* Tooltip */}
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block">
                <div className="bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
                  {badge.description}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## FILE: src/components/gamification/LevelDisplay.tsx
## ==================================================

```typescript
'use client';

interface LevelDisplayProps {
  level: number;
  size?: 'sm' | 'md' | 'lg';
}

export default function LevelDisplay({ level, size = 'md' }: LevelDisplayProps) {
  const sizeClasses = {
    sm: 'w-12 h-12 text-lg',
    md: 'w-16 h-16 text-2xl',
    lg: 'w-24 h-24 text-4xl',
  };

  const getLevelColor = (lvl: number) => {
    if (lvl >= 50) return 'from-yellow-400 to-yellow-600';
    if (lvl >= 25) return 'from-purple-400 to-purple-600';
    if (lvl >= 10) return 'from-blue-400 to-blue-600';
    return 'from-green-400 to-green-600';
  };

  return (
    <div
      className={`${sizeClasses[size]} rounded-full bg-gradient-to-br ${getLevelColor(
        level
      )} flex items-center justify-center text-white font-bold shadow-lg`}
    >
      {level}
    </div>
  );
}
```

---

# Continue to Part 4 for more components...
