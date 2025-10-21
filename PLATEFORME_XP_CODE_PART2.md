# PLATEFORME XP - API ROUTES AND COMPONENTS (PART 2)
# ===================================================

## FILE: src/app/api/auth/register/route.ts
## ==========================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { generateToken } from '@/lib/auth';
import { calculateLevel } from '@/utils/xp';
import { XP_REWARDS, BADGES } from '@/lib/constants';

export async function POST(request: NextRequest) {
  try {
    await connectDB();

    const body = await request.json();
    const { email, password, name, subjects } = body;

    // Validation
    if (!email || !password || !name) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Check if user exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return NextResponse.json(
        { success: false, error: 'User already exists' },
        { status: 400 }
      );
    }

    // Create user with first login badge
    const user = await User.create({
      email,
      password,
      name,
      subjects: subjects || [],
      xp: XP_REWARDS.FIRST_LOGIN,
      level: 1,
      badges: [
        {
          name: BADGES.FIRST_STEPS.name,
          description: BADGES.FIRST_STEPS.description,
          icon: BADGES.FIRST_STEPS.icon,
          type: BADGES.FIRST_STEPS.type,
          awardedAt: new Date(),
        },
      ],
    });

    // Generate token
    const token = generateToken({
      userId: user._id.toString(),
      email: user.email,
    });

    // Remove password from response
    const userResponse = user.toObject();
    delete userResponse.password;

    return NextResponse.json(
      {
        success: true,
        data: {
          user: userResponse,
          token,
        },
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Registration error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Registration failed' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/auth/login/route.ts
## ======================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { generateToken } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    await connectDB();

    const body = await request.json();
    const { email, password } = body;

    // Validation
    if (!email || !password) {
      return NextResponse.json(
        { success: false, error: 'Email and password are required' },
        { status: 400 }
      );
    }

    // Find user with password
    const user = await User.findOne({ email }).select('+password');
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'Invalid credentials' },
        { status: 401 }
      );
    }

    // Check password
    const isPasswordValid = await user.comparePassword(password);
    if (!isPasswordValid) {
      return NextResponse.json(
        { success: false, error: 'Invalid credentials' },
        { status: 401 }
      );
    }

    // Generate token
    const token = generateToken({
      userId: user._id.toString(),
      email: user.email,
    });

    // Remove password from response
    const userResponse = user.toObject();
    delete userResponse.password;

    return NextResponse.json({
      success: true,
      data: {
        user: userResponse,
        token,
      },
    });
  } catch (error: any) {
    console.error('Login error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Login failed' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/auth/me/route.ts
## ===================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { authenticateRequest } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const user = await User.findById(auth.userId);
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'User not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: user,
    });
  } catch (error: any) {
    console.error('Get user error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get user' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/xp/route.ts
## ==============================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { authenticateRequest } from '@/lib/auth';
import { getXPToNextLevel } from '@/utils/xp';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const user = await User.findById(auth.userId);
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'User not found' },
        { status: 404 }
      );
    }

    const xpInfo = getXPToNextLevel(user.xp);

    return NextResponse.json({
      success: true,
      data: {
        xp: user.xp,
        level: user.level,
        ...xpInfo,
      },
    });
  } catch (error: any) {
    console.error('Get XP error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get XP' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/xp/add/route.ts
## ==================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { authenticateRequest } from '@/lib/auth';
import { calculateLevel } from '@/utils/xp';
import { checkBadgeEligibility, awardBadge } from '@/utils/badges';
import { BadgeType } from '@/types';

export async function POST(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const body = await request.json();
    const { amount, reason } = body;

    if (!amount || amount <= 0) {
      return NextResponse.json(
        { success: false, error: 'Invalid XP amount' },
        { status: 400 }
      );
    }

    const user = await User.findById(auth.userId);
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'User not found' },
        { status: 404 }
      );
    }

    const oldLevel = user.level;
    const oldXP = user.xp;

    // Add XP
    user.xp += amount;
    user.level = calculateLevel(user.xp);

    // Check for level up badges
    if (user.level > oldLevel) {
      const levelBadge = checkBadgeEligibility(
        BadgeType.LEVEL_UP,
        user.level,
        user.badges
      );
      if (levelBadge.eligible && levelBadge.badge) {
        user.badges.push(awardBadge(levelBadge.badge));
      }
    }

    // Check for XP milestone badges
    const xpBadge = checkBadgeEligibility(
      BadgeType.XP_MILESTONE,
      user.xp,
      user.badges
    );
    if (xpBadge.eligible && xpBadge.badge) {
      user.badges.push(awardBadge(xpBadge.badge));
    }

    await user.save();

    return NextResponse.json({
      success: true,
      data: {
        xp: user.xp,
        level: user.level,
        leveledUp: user.level > oldLevel,
        newBadges: user.badges.slice(user.badges.length - 2),
      },
      message: `Added ${amount} XP${reason ? ` for ${reason}` : ''}`,
    });
  } catch (error: any) {
    console.error('Add XP error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to add XP' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/badges/route.ts
## ==================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { authenticateRequest } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const user = await User.findById(auth.userId);
    if (!user) {
      return NextResponse.json(
        { success: false, error: 'User not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: user.badges,
    });
  } catch (error: any) {
    console.error('Get badges error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get badges' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/events/route.ts
## ==================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import Event from '@/models/Event';
import { authenticateRequest } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const { searchParams } = new URL(request.url);
    const startDate = searchParams.get('start');
    const endDate = searchParams.get('end');
    const type = searchParams.get('type');

    let query: any = {};

    if (startDate && endDate) {
      query.start = {
        $gte: new Date(startDate),
        $lte: new Date(endDate),
      };
    }

    if (type) {
      query.type = type;
    }

    const events = await Event.find(query).sort({ start: 1 });

    return NextResponse.json({
      success: true,
      data: events,
    });
  } catch (error: any) {
    console.error('Get events error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get events' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const body = await request.json();
    const { title, description, start, end, type, location, maxAttendees, xpReward } = body;

    // Validation
    if (!title || !start || !end || !type) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const event = await Event.create({
      title,
      description,
      start: new Date(start),
      end: new Date(end),
      type,
      location,
      organizer: auth.userId,
      attendees: [],
      maxAttendees,
      xpReward: xpReward || 50,
    });

    return NextResponse.json(
      {
        success: true,
        data: event,
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Create event error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to create event' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/events/[id]/route.ts
## =======================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import Event from '@/models/Event';
import { authenticateRequest } from '@/lib/auth';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const event = await Event.findById(params.id);
    if (!event) {
      return NextResponse.json(
        { success: false, error: 'Event not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: event,
    });
  } catch (error: any) {
    console.error('Get event error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get event' },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const body = await request.json();
    const event = await Event.findByIdAndUpdate(params.id, body, {
      new: true,
      runValidators: true,
    });

    if (!event) {
      return NextResponse.json(
        { success: false, error: 'Event not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: event,
    });
  } catch (error: any) {
    console.error('Update event error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to update event' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const event = await Event.findByIdAndDelete(params.id);
    if (!event) {
      return NextResponse.json(
        { success: false, error: 'Event not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Event deleted successfully',
    });
  } catch (error: any) {
    console.error('Delete event error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to delete event' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/peers/route.ts
## =================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import User from '@/models/User';
import { authenticateRequest } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const { searchParams } = new URL(request.url);
    const subject = searchParams.get('subject');

    let query: any = { isAvailableForTutoring: true };

    if (subject) {
      query.subjects = subject;
    }

    const tutors = await User.find(query)
      .select('-password')
      .sort({ rating: -1 });

    return NextResponse.json({
      success: true,
      data: tutors,
    });
  } catch (error: any) {
    console.error('Get peers error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get peers' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/peers/request/route.ts
## =========================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import TutoringSession from '@/models/TutoringSession';
import { authenticateRequest } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const body = await request.json();
    const { tutorId, subject, scheduledAt, notes } = body;

    if (!tutorId || !subject) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const session = await TutoringSession.create({
      tutor: tutorId,
      student: auth.userId,
      subject,
      scheduledAt: scheduledAt ? new Date(scheduledAt) : undefined,
      notes,
      status: 'requested',
    });

    const populatedSession = await TutoringSession.findById(session._id)
      .populate('tutor', 'name email avatar subjects rating')
      .populate('student', 'name email avatar');

    return NextResponse.json(
      {
        success: true,
        data: populatedSession,
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Create session request error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to create session request' },
      { status: 500 }
    );
  }
}
```

## FILE: src/app/api/resources/route.ts
## =====================================

```typescript
import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import Resource from '@/models/Resource';
import { authenticateRequest } from '@/lib/auth';

export async function GET(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const { searchParams } = new URL(request.url);
    const subject = searchParams.get('subject');
    const type = searchParams.get('type');

    let query: any = {
      $or: [{ owner: auth.userId }, { sharedWith: auth.userId }],
    };

    if (subject) {
      query.subject = subject;
    }

    if (type) {
      query.type = type;
    }

    const resources = await Resource.find(query)
      .populate('owner', 'name email avatar')
      .sort({ createdAt: -1 });

    return NextResponse.json({
      success: true,
      data: resources,
    });
  } catch (error: any) {
    console.error('Get resources error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to get resources' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const auth = await authenticateRequest(request);
    if (!auth) {
      return NextResponse.json(
        { success: false, error: 'Unauthorized' },
        { status: 401 }
      );
    }

    await connectDB();

    const body = await request.json();
    const { title, description, type, url, subject, sharedWith } = body;

    if (!title || !type || !subject) {
      return NextResponse.json(
        { success: false, error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const resource = await Resource.create({
      title,
      description,
      type,
      url,
      subject,
      owner: auth.userId,
      sharedWith: sharedWith || [],
    });

    const populatedResource = await Resource.findById(resource._id).populate(
      'owner',
      'name email avatar'
    );

    return NextResponse.json(
      {
        success: true,
        data: populatedResource,
      },
      { status: 201 }
    );
  } catch (error: any) {
    console.error('Create resource error:', error);
    return NextResponse.json(
      { success: false, error: error.message || 'Failed to create resource' },
      { status: 500 }
    );
  }
}
```

---

# Continue to Part 3 for Frontend Components...
