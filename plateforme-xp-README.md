# Plateforme XP - MVP

A gamified learning platform with student profiles, event calendar, and peer-to-peer tutoring system.

## Features

- 🎮 **Gamified Student Profile**: XP tracking, leveling system, and achievement badges
- 📅 **Interactive Event Calendar**: View and manage events with responsive calendar interface
- 👥 **Peer-to-Peer Tutoring**: Connect with peers, share resources, and communicate in real-time
- 🔐 **Authentication**: Secure email/password authentication system
- 📱 **Responsive Design**: Mobile-first design using Tailwind CSS

## Technology Stack

- **Frontend**: Next.js 14 with React 18 and TypeScript
- **Styling**: Tailwind CSS
- **Backend**: Next.js API Routes with Node.js
- **Database**: MongoDB with Mongoose ODM
- **Real-time**: Socket.IO for live communication
- **Code Quality**: ESLint and Prettier

## Project Structure

```
plateforme-xp/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── api/                  # API routes
│   │   │   ├── auth/            # Authentication endpoints
│   │   │   ├── xp/              # XP management
│   │   │   ├── badges/          # Badge system
│   │   │   ├── events/          # Event management
│   │   │   ├── peers/           # Peer connections
│   │   │   └── resources/       # Resource sharing
│   │   ├── dashboard/           # Dashboard page
│   │   ├── profile/             # Profile page
│   │   ├── calendar/            # Calendar page
│   │   ├── tutoring/            # Tutoring page
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home page
│   ├── components/              # React components
│   │   ├── gamification/        # XP, levels, badges
│   │   ├── calendar/            # Calendar components
│   │   ├── tutoring/            # Tutoring components
│   │   └── layout/              # Layout components
│   ├── lib/                     # Utilities and config
│   ├── models/                  # MongoDB models
│   ├── types/                   # TypeScript types
│   └── utils/                   # Helper functions
├── public/                      # Static assets
├── .env.local                   # Environment variables
└── package.json                 # Dependencies
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- MongoDB (local or MongoDB Atlas)

### Installation

1. **Extract the project files** to a directory

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env.local` file in the root directory:
   ```env
   # Database
   MONGODB_URI=mongodb://localhost:27017/plateforme-xp
   # or for MongoDB Atlas:
   # MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/plateforme-xp

   # Authentication
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   JWT_EXPIRES_IN=7d

   # App
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### XP & Gamification
- `GET /api/xp` - Get user XP
- `POST /api/xp/add` - Add XP to user
- `GET /api/badges` - Get user badges
- `POST /api/badges/award` - Award badge

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create event
- `GET /api/events/[id]` - Get event details
- `PUT /api/events/[id]` - Update event
- `DELETE /api/events/[id]` - Delete event

### Peer Tutoring
- `GET /api/peers` - Get available tutors
- `POST /api/peers/request` - Request tutoring session
- `GET /api/resources` - Get shared resources
- `POST /api/resources` - Share resource

## Usage Guide

### 1. Register/Login
- Navigate to the home page
- Create an account or login with existing credentials

### 2. Dashboard
- View your XP, level, and badges
- See upcoming events
- Check available tutors

### 3. Profile
- View and edit your profile
- See your achievement history
- Track your progress

### 4. Calendar
- Browse events in month/week/day view
- Click on events to see details
- Filter events by category

### 5. Tutoring System
- Browse available tutors by subject
- Send tutoring requests
- Share resources with peers
- Communicate via real-time chat

## Development

### Run linter
```bash
npm run lint
```

### Format code
```bash
npm run format
```

### Build for production
```bash
npm run build
npm start
```

## Key Features Implementation

### Gamification System
- **XP Calculation**: Based on activities (attending events, completing sessions, sharing resources)
- **Levels**: 1-100, exponential XP requirements
- **Badges**: Achievement system with 20+ badge types
- **Progress Visualization**: Progress bars, level indicators, badge gallery

### Calendar System
- **FullCalendar Integration**: Month, week, and day views
- **Event Types**: Lectures, workshops, study sessions, exams
- **Filtering**: By category, date range, and status
- **Responsive**: Mobile-optimized touch interactions

### Tutoring System
- **Profile Discovery**: Browse tutors by subject and rating
- **Session Requests**: Send and manage tutoring requests
- **Resource Sharing**: Upload and share files, links, and notes
- **Real-time Chat**: Socket.IO powered messaging
- **WebRTC Ready**: Structure for video/audio calls (requires additional setup)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MONGODB_URI` | MongoDB connection string | Yes |
| `JWT_SECRET` | Secret key for JWT tokens | Yes |
| `JWT_EXPIRES_IN` | Token expiration time | No (default: 7d) |
| `NEXT_PUBLIC_APP_URL` | Application URL | Yes |

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens for session management
- Environment variables for sensitive data
- Input validation on all API endpoints
- CORS configuration for production

## Future Enhancements

- [ ] Video/audio calling with WebRTC
- [ ] Push notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile apps (React Native)
- [ ] AI-powered tutor matching
- [ ] Gamification leaderboards
- [ ] Integration with learning management systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for learning and development.

## Support

For issues and questions, please open an issue on the repository or contact the development team.

---

Built with ❤️ using Next.js, TypeScript, and Tailwind CSS
