# Plateforme XP - Complete Project Structure

This document contains the complete file structure and code for the Plateforme XP MVP.

## Project Structure

```
plateforme-xp/
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.ts
├── postcss.config.js
├── .eslintrc.json
├── .prettierrc
├── .env.local.example
├── README.md
├── public/
│   └── badges/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   ├── register/route.ts
│   │   │   │   ├── login/route.ts
│   │   │   │   └── me/route.ts
│   │   │   ├── xp/
│   │   │   │   ├── route.ts
│   │   │   │   └── add/route.ts
│   │   │   ├── badges/
│   │   │   │   ├── route.ts
│   │   │   │   └── award/route.ts
│   │   │   ├── events/
│   │   │   │   ├── route.ts
│   │   │   │   └── [id]/route.ts
│   │   │   ├── peers/
│   │   │   │   ├── route.ts
│   │   │   │   └── request/route.ts
│   │   │   └── resources/
│   │   │       └── route.ts
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── profile/
│   │   │   └── page.tsx
│   │   ├── calendar/
│   │   │   └── page.tsx
│   │   └── tutoring/
│   │       └── page.tsx
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── gamification/
│   │   │   ├── XPBar.tsx
│   │   │   ├── LevelDisplay.tsx
│   │   │   ├── BadgeGallery.tsx
│   │   │   └── ProgressRing.tsx
│   │   ├── calendar/
│   │   │   ├── EventCalendar.tsx
│   │   │   ├── EventCard.tsx
│   │   │   └── EventModal.tsx
│   │   ├── tutoring/
│   │   │   ├── TutorCard.tsx
│   │   │   ├── ChatBox.tsx
│   │   │   ├── ResourceList.tsx
│   │   │   └── SessionRequest.tsx
│   │   └── auth/
│   │       ├── LoginForm.tsx
│   │       └── RegisterForm.tsx
│   ├── lib/
│   │   ├── mongodb.ts
│   │   ├── auth.ts
│   │   ├── socket.ts
│   │   └── constants.ts
│   ├── models/
│   │   ├── User.ts
│   │   ├── Event.ts
│   │   ├── Badge.ts
│   │   ├── Resource.ts
│   │   └── TutoringSession.ts
│   ├── types/
│   │   ├── index.ts
│   │   ├── user.ts
│   │   ├── event.ts
│   │   └── tutoring.ts
│   └── utils/
│       ├── xp.ts
│       ├── badges.ts
│       └── validation.ts
└── server/
    └── socket.ts
```

## Installation Instructions

1. Create a new directory and save all files according to the structure above
2. Run `npm install` in the root directory
3. Copy `.env.local.example` to `.env.local` and fill in your values
4. Run `npm run dev` to start the development server

## File Contents Follow Below

Each file is documented with its purpose and implementation details.
