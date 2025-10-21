# PLATEFORME XP - DASHBOARD, CALENDAR & TUTORING COMPONENTS (PART 4)
# ====================================================================

## FILE: src/components/layout/Header.tsx
## =======================================

```typescript
'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { IUser } from '@/types';
import LevelDisplay from '@/components/gamification/LevelDisplay';

export default function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<IUser | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setUser(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch user:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/');
  };

  const navItems = [
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/profile', label: 'Profile' },
    { href: '/calendar', label: 'Calendar' },
    { href: '/tutoring', label: 'Tutoring' },
  ];

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/dashboard" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-primary-600">Plateforme XP</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`font-medium transition-colors ${
                  pathname === item.href
                    ? 'text-primary-600'
                    : 'text-gray-600 hover:text-primary-600'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="flex items-center space-x-3">
                <LevelDisplay level={user.level} size="sm" />
                <div className="hidden md:block text-right">
                  <p className="font-semibold text-gray-800">{user.name}</p>
                  <p className="text-xs text-gray-500">{user.xp} XP</p>
                </div>
              </div>
            )}

            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Logout
            </button>

            {/* Mobile menu button */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="md:hidden text-gray-600 hover:text-primary-600"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                {menuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {menuOpen && (
          <nav className="md:hidden py-4 border-t">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMenuOpen(false)}
                className={`block py-2 font-medium ${
                  pathname === item.href ? 'text-primary-600' : 'text-gray-600'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
```

## FILE: src/app/dashboard/page.tsx
## =================================

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import XPBar from '@/components/gamification/XPBar';
import BadgeGallery from '@/components/gamification/BadgeGallery';
import { IUser, IEvent } from '@/types';
import { format } from 'date-fns';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<IUser | null>(null);
  const [upcomingEvents, setUpcomingEvents] = useState<IEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }
    fetchDashboardData();
  }, [router]);

  const fetchDashboardData = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const [userRes, eventsRes] = await Promise.all([
        fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch('/api/events', {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

      const userData = await userRes.json();
      const eventsData = await eventsRes.json();

      if (userData.success) {
        setUser(userData.data);
      }

      if (eventsData.success) {
        const upcoming = eventsData.data
          .filter((event: IEvent) => new Date(event.start) > new Date())
          .slice(0, 5);
        setUpcomingEvents(upcoming);
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Welcome back, {user.name}! 👋
        </h1>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* XP Progress */}
            <XPBar xp={user.xp} level={user.level} />

            {/* Upcoming Events */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-800">
                  Upcoming Events
                </h2>
                <button
                  onClick={() => router.push('/calendar')}
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  View All
                </button>
              </div>

              {upcomingEvents.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  No upcoming events
                </p>
              ) : (
                <div className="space-y-3">
                  {upcomingEvents.map((event) => (
                    <div
                      key={event._id}
                      className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                      onClick={() => router.push('/calendar')}
                    >
                      <div className="flex-shrink-0 w-16 h-16 bg-primary-100 rounded-lg flex flex-col items-center justify-center">
                        <span className="text-xs text-primary-600 font-semibold">
                          {format(new Date(event.start), 'MMM')}
                        </span>
                        <span className="text-xl font-bold text-primary-700">
                          {format(new Date(event.start), 'd')}
                        </span>
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-800">
                          {event.title}
                        </h3>
                        <p className="text-sm text-gray-600">
                          {format(new Date(event.start), 'h:mm a')} -{' '}
                          {event.type}
                        </p>
                      </div>
                      <div className="text-right">
                        <span className="inline-block bg-primary-100 text-primary-700 text-xs font-semibold px-2 py-1 rounded">
                          +{event.xpReward} XP
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Badges */}
            <BadgeGallery badges={user.badges} />
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Quick Stats */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Quick Stats
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Total XP</span>
                  <span className="font-bold text-primary-600">{user.xp}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Level</span>
                  <span className="font-bold text-secondary-600">
                    {user.level}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Badges</span>
                  <span className="font-bold text-yellow-600">
                    {user.badges.length}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Rating</span>
                  <span className="font-bold text-green-600">
                    {user.rating.toFixed(1)} ⭐
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">
                Quick Actions
              </h3>
              <div className="space-y-2">
                <button
                  onClick={() => router.push('/calendar')}
                  className="w-full bg-primary-50 hover:bg-primary-100 text-primary-700 font-medium py-3 px-4 rounded-lg transition-colors text-left"
                >
                  📅 View Calendar
                </button>
                <button
                  onClick={() => router.push('/tutoring')}
                  className="w-full bg-secondary-50 hover:bg-secondary-100 text-secondary-700 font-medium py-3 px-4 rounded-lg transition-colors text-left"
                >
                  👥 Find a Tutor
                </button>
                <button
                  onClick={() => router.push('/profile')}
                  className="w-full bg-green-50 hover:bg-green-100 text-green-700 font-medium py-3 px-4 rounded-lg transition-colors text-left"
                >
                  👤 Edit Profile
                </button>
              </div>
            </div>

            {/* Subjects */}
            {user.subjects && user.subjects.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Your Subjects
                </h3>
                <div className="flex flex-wrap gap-2">
                  {user.subjects.map((subject) => (
                    <span
                      key={subject}
                      className="bg-primary-100 text-primary-700 text-xs font-medium px-3 py-1 rounded-full"
                    >
                      {subject}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
```

## FILE: src/components/calendar/EventCalendar.tsx
## ================================================

```typescript
'use client';

import { useEffect, useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { IEvent } from '@/types';

interface EventCalendarProps {
  events: IEvent[];
  onEventClick: (event: IEvent) => void;
  onDateSelect?: (start: Date, end: Date) => void;
}

export default function EventCalendar({
  events,
  onEventClick,
  onDateSelect,
}: EventCalendarProps) {
  const calendarRef = useRef<FullCalendar>(null);

  const getEventColor = (type: string) => {
    const colors: Record<string, string> = {
      lecture: '#3b82f6',
      workshop: '#10b981',
      study_session: '#8b5cf6',
      exam: '#ef4444',
      social: '#f59e0b',
    };
    return colors[type] || '#6b7280';
  };

  const calendarEvents = events.map((event) => ({
    id: event._id,
    title: event.title,
    start: event.start,
    end: event.end,
    backgroundColor: getEventColor(event.type),
    borderColor: getEventColor(event.type),
    extendedProps: event,
  }));

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <FullCalendar
        ref={calendarRef}
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
        events={calendarEvents}
        editable={false}
        selectable={true}
        selectMirror={true}
        dayMaxEvents={true}
        weekends={true}
        eventClick={(info) => {
          onEventClick(info.event.extendedProps as IEvent);
        }}
        select={(info) => {
          if (onDateSelect) {
            onDateSelect(info.start, info.end);
          }
        }}
        height="auto"
        eventTimeFormat={{
          hour: '2-digit',
          minute: '2-digit',
          meridiem: 'short',
        }}
      />
    </div>
  );
}
```

## FILE: src/app/calendar/page.tsx
## ================================

```typescript
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import EventCalendar from '@/components/calendar/EventCalendar';
import { IEvent } from '@/types';
import { format } from 'date-fns';

export default function CalendarPage() {
  const router = useRouter();
  const [events, setEvents] = useState<IEvent[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<IEvent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }
    fetchEvents();
  }, [router]);

  const fetchEvents = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch('/api/events', {
        headers: { Authorization: `Bearer ${token}` },
      });

      const data = await response.json();
      if (data.success) {
        setEvents(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEventClick = (event: IEvent) => {
    setSelectedEvent(event);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading calendar...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Event Calendar 📅
          </h1>
          <p className="text-gray-600">
            View and manage your learning events
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <EventCalendar events={events} onEventClick={handleEventClick} />
          </div>

          <div>
            {selectedEvent ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-4">
                  Event Details
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Title
                    </label>
                    <p className="text-gray-900 font-semibold">
                      {selectedEvent.title}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Type
                    </label>
                    <p className="text-gray-900 capitalize">
                      {selectedEvent.type.replace('_', ' ')}
                    </p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      Date & Time
                    </label>
                    <p className="text-gray-900">
                      {format(new Date(selectedEvent.start), 'PPP')}
                    </p>
                    <p className="text-gray-700 text-sm">
                      {format(new Date(selectedEvent.start), 'p')} -{' '}
                      {format(new Date(selectedEvent.end), 'p')}
                    </p>
                  </div>
                  {selectedEvent.location && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">
                        Location
                      </label>
                      <p className="text-gray-900">{selectedEvent.location}</p>
                    </div>
                  )}
                  {selectedEvent.description && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">
                        Description
                      </label>
                      <p className="text-gray-900">{selectedEvent.description}</p>
                    </div>
                  )}
                  <div>
                    <label className="text-sm font-medium text-gray-600">
                      XP Reward
                    </label>
                    <p className="text-primary-600 font-bold">
                      +{selectedEvent.xpReward} XP
                    </p>
                  </div>
                  {selectedEvent.maxAttendees && (
                    <div>
                      <label className="text-sm font-medium text-gray-600">
                        Attendees
                      </label>
                      <p className="text-gray-900">
                        {selectedEvent.attendees.length} / {selectedEvent.maxAttendees}
                      </p>
                    </div>
                  )}
                </div>
                <button
                  onClick={() => setSelectedEvent(null)}
                  className="w-full mt-6 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors"
                >
                  Close
                </button>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  Event Legend
                </h3>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded bg-blue-500"></div>
                    <span className="text-sm text-gray-700">Lecture</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded bg-green-500"></div>
                    <span className="text-sm text-gray-700">Workshop</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded bg-purple-500"></div>
                    <span className="text-sm text-gray-700">Study Session</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded bg-red-500"></div>
                    <span className="text-sm text-gray-700">Exam</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 rounded bg-yellow-500"></div>
                    <span className="text-sm text-gray-700">Social</span>
                  </div>
                </div>
                <p className="mt-4 text-sm text-gray-600">
                  Click on an event to view details
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
```

---

# Continue to Part 5 for Tutoring and Profile pages...
