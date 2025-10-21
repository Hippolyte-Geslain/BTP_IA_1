# PLATEFORME XP - COMPLETE SOURCE CODE
# =====================================
# This file contains all the source code for the Plateforme XP MVP
# Extract each section to its corresponding file path

## FILE: src/types/index.ts
## ========================

```typescript
// User Types
export interface IUser {
  _id: string;
  email: string;
  name: string;
  password?: string;
  xp: number;
  level: number;
  badges: IBadge[];
  subjects: string[];
  bio?: string;
  avatar?: string;
  isAvailableForTutoring: boolean;
  rating: number;
  createdAt: Date;
  updatedAt: Date;
}

// Badge Types
export interface IBadge {
  _id: string;
  name: string;
  description: string;
  icon: string;
  type: BadgeType;
  awardedAt: Date;
}

export enum BadgeType {
  FIRST_LOGIN = 'first_login',
  XP_MILESTONE = 'xp_milestone',
  EVENT_ATTENDANCE = 'event_attendance',
  TUTORING_SESSION = 'tutoring_session',
  RESOURCE_SHARE = 'resource_share',
  LEVEL_UP = 'level_up',
}

// Event Types
export interface IEvent {
  _id: string;
  title: string;
  description: string;
  start: Date;
  end: Date;
  type: EventType;
  location?: string;
  organizer: string;
  attendees: string[];
  maxAttendees?: number;
  xpReward: number;
  createdAt: Date;
}

export enum EventType {
  LECTURE = 'lecture',
  WORKSHOP = 'workshop',
  STUDY_SESSION = 'study_session',
  EXAM = 'exam',
  SOCIAL = 'social',
}

// Tutoring Types
export interface ITutoringSession {
  _id: string;
  tutor: IUser;
  student: IUser;
  subject: string;
  status: SessionStatus;
  scheduledAt?: Date;
  duration?: number;
  notes?: string;
  rating?: number;
  createdAt: Date;
  completedAt?: Date;
}

export enum SessionStatus {
  REQUESTED = 'requested',
  ACCEPTED = 'accepted',
  DECLINED = 'declined',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

// Resource Types
export interface IResource {
  _id: string;
  title: string;
  description: string;
  type: ResourceType;
  url?: string;
  fileUrl?: string;
  subject: string;
  owner: IUser;
  sharedWith: string[];
  downloads: number;
  createdAt: Date;
}

export enum ResourceType {
  DOCUMENT = 'document',
  LINK = 'link',
  VIDEO = 'video',
  NOTE = 'note',
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  subjects?: string[];
}

export interface AuthResponse {
  user: IUser;
  token: string;
}

// Socket Event Types
export interface ChatMessage {
  id: string;
  senderId: string;
  receiverId: string;
  message: string;
  timestamp: Date;
  read: boolean;
}
```

## FILE: src/lib/constants.ts
## ==========================

```typescript
// XP and Level Constants
export const XP_PER_LEVEL = 1000;
export const LEVEL_MULTIPLIER = 1.5;
export const MAX_LEVEL = 100;

// XP Rewards
export const XP_REWARDS = {
  EVENT_ATTENDANCE: 50,
  TUTORING_SESSION_COMPLETE: 100,
  RESOURCE_SHARE: 25,
  FIRST_LOGIN: 10,
  DAILY_LOGIN: 5,
  PROFILE_COMPLETE: 50,
};

// Badge Definitions
export const BADGES = {
  FIRST_STEPS: {
    name: 'First Steps',
    description: 'Created your account',
    icon: '🎯',
    type: 'first_login',
  },
  KNOWLEDGE_SEEKER: {
    name: 'Knowledge Seeker',
    description: 'Attended 5 events',
    icon: '📚',
    type: 'event_attendance',
  },
  HELPFUL_TUTOR: {
    name: 'Helpful Tutor',
    description: 'Completed 10 tutoring sessions',
    icon: '👨‍🏫',
    type: 'tutoring_session',
  },
  RESOURCE_MASTER: {
    name: 'Resource Master',
    description: 'Shared 20 resources',
    icon: '📦',
    type: 'resource_share',
  },
  LEVEL_10: {
    name: 'Rising Star',
    description: 'Reached level 10',
    icon: '⭐',
    type: 'level_up',
  },
  LEVEL_25: {
    name: 'Expert Learner',
    description: 'Reached level 25',
    icon: '🌟',
    type: 'level_up',
  },
  LEVEL_50: {
    name: 'Master',
    description: 'Reached level 50',
    icon: '💫',
    type: 'level_up',
  },
  XP_1000: {
    name: 'XP Collector',
    description: 'Earned 1,000 XP',
    icon: '🏆',
    type: 'xp_milestone',
  },
  XP_5000: {
    name: 'XP Master',
    description: 'Earned 5,000 XP',
    icon: '🥇',
    type: 'xp_milestone',
  },
  XP_10000: {
    name: 'XP Legend',
    description: 'Earned 10,000 XP',
    icon: '👑',
    type: 'xp_milestone',
  },
};

// Subject Categories
export const SUBJECTS = [
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'Computer Science',
  'English',
  'French',
  'History',
  'Geography',
  'Economics',
  'Philosophy',
  'Art',
  'Music',
  'Physical Education',
];

// Event Types
export const EVENT_TYPES = [
  { value: 'lecture', label: 'Lecture', color: 'blue' },
  { value: 'workshop', label: 'Workshop', color: 'green' },
  { value: 'study_session', label: 'Study Session', color: 'purple' },
  { value: 'exam', label: 'Exam', color: 'red' },
  { value: 'social', label: 'Social', color: 'yellow' },
];
```

## FILE: src/lib/mongodb.ts
## ========================

```typescript
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/plateforme-xp';

if (!MONGODB_URI) {
  throw new Error('Please define the MONGODB_URI environment variable');
}

interface MongooseCache {
  conn: typeof mongoose | null;
  promise: Promise<typeof mongoose> | null;
}

declare global {
  var mongoose: MongooseCache;
}

let cached: MongooseCache = global.mongoose || { conn: null, promise: null };

if (!global.mongoose) {
  global.mongoose = cached;
}

async function connectDB(): Promise<typeof mongoose> {
  if (cached.conn) {
    return cached.conn;
  }

  if (!cached.promise) {
    const opts = {
      bufferCommands: false,
    };

    cached.promise = mongoose.connect(MONGODB_URI, opts).then((mongoose) => {
      console.log('✅ MongoDB connected successfully');
      return mongoose;
    });
  }

  try {
    cached.conn = await cached.promise;
  } catch (e) {
    cached.promise = null;
    throw e;
  }

  return cached.conn;
}

export default connectDB;
```

## FILE: src/lib/auth.ts
## =====================

```typescript
import jwt from 'jsonwebtoken';
import { NextRequest } from 'next/server';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';

export interface JWTPayload {
  userId: string;
  email: string;
}

export function generateToken(payload: JWTPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
}

export function verifyToken(token: string): JWTPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET) as JWTPayload;
  } catch (error) {
    return null;
  }
}

export function getTokenFromRequest(request: NextRequest): string | null {
  const authHeader = request.headers.get('authorization');
  
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }
  
  return null;
}

export async function authenticateRequest(request: NextRequest): Promise<JWTPayload | null> {
  const token = getTokenFromRequest(request);
  
  if (!token) {
    return null;
  }
  
  return verifyToken(token);
}
```

## FILE: src/utils/xp.ts
## =====================

```typescript
import { XP_PER_LEVEL, LEVEL_MULTIPLIER, MAX_LEVEL } from '@/lib/constants';

export function calculateLevel(xp: number): number {
  let level = 1;
  let requiredXP = XP_PER_LEVEL;

  while (xp >= requiredXP && level < MAX_LEVEL) {
    level++;
    requiredXP = Math.floor(XP_PER_LEVEL * Math.pow(LEVEL_MULTIPLIER, level - 1));
  }

  return level;
}

export function getXPForLevel(level: number): number {
  if (level <= 1) return 0;
  return Math.floor(XP_PER_LEVEL * Math.pow(LEVEL_MULTIPLIER, level - 1));
}

export function getXPToNextLevel(currentXP: number): {
  currentLevelXP: number;
  nextLevelXP: number;
  xpInCurrentLevel: number;
  xpToNextLevel: number;
  progressPercentage: number;
} {
  const currentLevel = calculateLevel(currentXP);
  const currentLevelXP = getXPForLevel(currentLevel);
  const nextLevelXP = getXPForLevel(currentLevel + 1);
  const xpInCurrentLevel = currentXP - currentLevelXP;
  const xpToNextLevel = nextLevelXP - currentXP;
  const progressPercentage = (xpInCurrentLevel / (nextLevelXP - currentLevelXP)) * 100;

  return {
    currentLevelXP,
    nextLevelXP,
    xpInCurrentLevel,
    xpToNextLevel,
    progressPercentage,
  };
}

export function formatXP(xp: number): string {
  if (xp >= 1000000) {
    return `${(xp / 1000000).toFixed(1)}M`;
  }
  if (xp >= 1000) {
    return `${(xp / 1000).toFixed(1)}K`;
  }
  return xp.toString();
}
```

## FILE: src/utils/badges.ts
## =========================

```typescript
import { BADGES } from '@/lib/constants';
import { IBadge, BadgeType } from '@/types';

export function checkBadgeEligibility(
  type: BadgeType,
  count: number,
  currentBadges: IBadge[]
): { eligible: boolean; badge?: any } {
  const hasBadge = (badgeName: string) =>
    currentBadges.some((b) => b.name === badgeName);

  switch (type) {
    case BadgeType.FIRST_LOGIN:
      if (!hasBadge(BADGES.FIRST_STEPS.name)) {
        return { eligible: true, badge: BADGES.FIRST_STEPS };
      }
      break;

    case BadgeType.EVENT_ATTENDANCE:
      if (count >= 5 && !hasBadge(BADGES.KNOWLEDGE_SEEKER.name)) {
        return { eligible: true, badge: BADGES.KNOWLEDGE_SEEKER };
      }
      break;

    case BadgeType.TUTORING_SESSION:
      if (count >= 10 && !hasBadge(BADGES.HELPFUL_TUTOR.name)) {
        return { eligible: true, badge: BADGES.HELPFUL_TUTOR };
      }
      break;

    case BadgeType.RESOURCE_SHARE:
      if (count >= 20 && !hasBadge(BADGES.RESOURCE_MASTER.name)) {
        return { eligible: true, badge: BADGES.RESOURCE_MASTER };
      }
      break;

    case BadgeType.LEVEL_UP:
      if (count >= 50 && !hasBadge(BADGES.LEVEL_50.name)) {
        return { eligible: true, badge: BADGES.LEVEL_50 };
      }
      if (count >= 25 && !hasBadge(BADGES.LEVEL_25.name)) {
        return { eligible: true, badge: BADGES.LEVEL_25 };
      }
      if (count >= 10 && !hasBadge(BADGES.LEVEL_10.name)) {
        return { eligible: true, badge: BADGES.LEVEL_10 };
      }
      break;

    case BadgeType.XP_MILESTONE:
      if (count >= 10000 && !hasBadge(BADGES.XP_10000.name)) {
        return { eligible: true, badge: BADGES.XP_10000 };
      }
      if (count >= 5000 && !hasBadge(BADGES.XP_5000.name)) {
        return { eligible: true, badge: BADGES.XP_5000 };
      }
      if (count >= 1000 && !hasBadge(BADGES.XP_1000.name)) {
        return { eligible: true, badge: BADGES.XP_1000 };
      }
      break;
  }

  return { eligible: false };
}

export function awardBadge(badge: any): IBadge {
  return {
    _id: Date.now().toString(),
    name: badge.name,
    description: badge.description,
    icon: badge.icon,
    type: badge.type,
    awardedAt: new Date(),
  };
}
```

## FILE: src/models/User.ts
## ========================

```typescript
import mongoose, { Schema, Model } from 'mongoose';
import bcrypt from 'bcryptjs';
import { IUser } from '@/types';

interface IUserMethods {
  comparePassword(candidatePassword: string): Promise<boolean>;
}

type UserModel = Model<IUser, {}, IUserMethods>;

const BadgeSchema = new Schema({
  name: { type: String, required: true },
  description: String,
  icon: String,
  type: String,
  awardedAt: { type: Date, default: Date.now },
});

const UserSchema = new Schema<IUser, UserModel, IUserMethods>(
  {
    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    password: {
      type: String,
      required: true,
      select: false,
    },
    xp: {
      type: Number,
      default: 0,
    },
    level: {
      type: Number,
      default: 1,
    },
    badges: [BadgeSchema],
    subjects: [String],
    bio: String,
    avatar: String,
    isAvailableForTutoring: {
      type: Boolean,
      default: false,
    },
    rating: {
      type: Number,
      default: 0,
    },
  },
  {
    timestamps: true,
  }
);

// Hash password before saving
UserSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error: any) {
    next(error);
  }
});

// Compare password method
UserSchema.methods.comparePassword = async function (
  candidatePassword: string
): Promise<boolean> {
  return bcrypt.compare(candidatePassword, this.password);
};

export default (mongoose.models.User as UserModel) ||
  mongoose.model<IUser, UserModel>('User', UserSchema);
```

## FILE: src/models/Event.ts
## =========================

```typescript
import mongoose, { Schema, Model } from 'mongoose';
import { IEvent } from '@/types';

const EventSchema = new Schema<IEvent>(
  {
    title: {
      type: String,
      required: true,
    },
    description: String,
    start: {
      type: Date,
      required: true,
    },
    end: {
      type: Date,
      required: true,
    },
    type: {
      type: String,
      enum: ['lecture', 'workshop', 'study_session', 'exam', 'social'],
      required: true,
    },
    location: String,
    organizer: {
      type: String,
      required: true,
    },
    attendees: [String],
    maxAttendees: Number,
    xpReward: {
      type: Number,
      default: 50,
    },
  },
  {
    timestamps: true,
  }
);

export default (mongoose.models.Event as Model<IEvent>) ||
  mongoose.model<IEvent>('Event', EventSchema);
```

## FILE: src/models/TutoringSession.ts
## ====================================

```typescript
import mongoose, { Schema, Model } from 'mongoose';
import { ITutoringSession } from '@/types';

const TutoringSessionSchema = new Schema<ITutoringSession>(
  {
    tutor: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    student: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    subject: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      enum: ['requested', 'accepted', 'declined', 'in_progress', 'completed', 'cancelled'],
      default: 'requested',
    },
    scheduledAt: Date,
    duration: Number,
    notes: String,
    rating: Number,
    completedAt: Date,
  },
  {
    timestamps: true,
  }
);

export default (mongoose.models.TutoringSession as Model<ITutoringSession>) ||
  mongoose.model<ITutoringSession>('TutoringSession', TutoringSessionSchema);
```

## FILE: src/models/Resource.ts
## =============================

```typescript
import mongoose, { Schema, Model } from 'mongoose';
import { IResource } from '@/types';

const ResourceSchema = new Schema<IResource>(
  {
    title: {
      type: String,
      required: true,
    },
    description: String,
    type: {
      type: String,
      enum: ['document', 'link', 'video', 'note'],
      required: true,
    },
    url: String,
    fileUrl: String,
    subject: {
      type: String,
      required: true,
    },
    owner: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    sharedWith: [String],
    downloads: {
      type: Number,
      default: 0,
    },
  },
  {
    timestamps: true,
  }
);

export default (mongoose.models.Resource as Model<IResource>) ||
  mongoose.model<IResource>('Resource', ResourceSchema);
```

---

# Continue to Part 2 for API Routes and Components...
