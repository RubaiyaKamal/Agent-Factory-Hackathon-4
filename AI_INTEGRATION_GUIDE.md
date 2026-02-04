# GPT-4o-mini AI Integration Guide

## Overview

This guide shows you how to integrate OpenAI's GPT-4o-mini API directly into your Next.js frontend for cost-effective AI tutoring.

**Cost Comparison:**
- **GPT-4o**: $2.50/$10.00 per 1M tokens (input/output)
- **GPT-4o-mini**: $0.15/$0.60 per 1M tokens ⭐ **94% cheaper!**
- **GPT-3.5-turbo**: $0.50/$1.50 per 1M tokens

**Recommendation:** GPT-4o-mini provides excellent quality at minimal cost.

---

## Step 1: Get Your OpenAI API Key

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/api-keys

2. **Create API Key**
   - Click "Create new secret key"
   - Name it: "Course Companion AI"
   - Copy the key (starts with `sk-...`)

3. **Add Credit**
   - Go to: https://platform.openai.com/account/billing
   - Add $5-$10 to start (very low usage expected)

---

## Step 2: Configure Environment Variables

1. **Open the `.env.local` file** in the `frontend` folder:
   ```bash
   cd frontend
   code .env.local
   ```

2. **Add your OpenAI API key:**
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_MAX_TOKENS=1000
   OPENAI_TEMPERATURE=0.7

   ENABLE_COST_TRACKING=true
   COST_ALERT_THRESHOLD=10.00

   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. **Save the file**

---

## Step 3: Restart Your Frontend

```bash
# Stop the current frontend (Ctrl+C in the terminal)
# Or if running in background, stop it first

cd frontend
npm run dev
```

The server will restart and load your new environment variables.

---

## Step 4: Access the AI Tutor

1. **Open your browser:**
   ```
   http://localhost:3000/ai-tutor
   ```

2. **You should see:**
   - AI Tutor interface
   - 4 teaching styles (skills)
   - Chat interface
   - Real-time cost tracking

---

## Step 5: Test the AI Tutor

### Test 1: Concept Explanation
```
User: "What is MCP?"
Expected: AI explains Model Context Protocol based on course content
Cost: ~$0.0001
```

### Test 2: Quiz Mode
```
User: "Quiz me on Claude SDK basics"
Expected: AI presents quiz questions and grades answers
Cost: ~$0.0002
```

### Test 3: Socratic Learning
```
User: "I'm stuck understanding agent skills"
Expected: AI asks guiding questions instead of direct answers
Cost: ~$0.0001
```

### Test 4: Progress Motivation
```
User: "Show my progress"
Expected: AI celebrates achievements and encourages
Cost: ~$0.0001
```

---

## Architecture

### Request Flow

```
┌──────────┐      ┌───────────────┐      ┌─────────────┐      ┌──────────┐
│  User    │─────▶│  AI Tutor     │─────▶│  Next.js    │─────▶│ OpenAI   │
│ Browser  │      │   Component   │      │  API Route  │      │   API    │
└──────────┘      └───────────────┘      └─────────────┘      └──────────┘
                         │                       │                    │
                         │                       │                    │
                         ▼                       ▼                    ▼
                  ┌─────────────┐        ┌─────────────┐     ┌──────────────┐
                  │   Context   │        │  System     │     │  GPT-4o-mini │
                  │  (Course)   │        │  Prompts    │     │   Response   │
                  └─────────────┘        └─────────────┘     └──────────────┘
```

### Files Created

```
frontend/
├── .env.local                    # OpenAI API key & config
├── app/
│   ├── api/
│   │   └── ai/
│   │       └── chat/
│   │           └── route.ts      # API route handler
│   └── ai-tutor/
│       └── page.tsx              # AI Tutor page
└── components/
    └── AIChat.tsx                # Chat component
```

---

## Cost Tracking & Optimization

### Real-Time Cost Display

The AI Tutor shows:
- **Tokens used** (input + output)
- **Cost per message** (~$0.0001-0.0005)
- **Total session cost**

### Cost Optimization Tips

1. **Limit Max Tokens**
   ```env
   OPENAI_MAX_TOKENS=500  # Shorter responses = lower cost
   ```

2. **Use Efficient Prompts**
   - Be specific in questions
   - Avoid long context when not needed

3. **Set Cost Alerts**
   ```env
   COST_ALERT_THRESHOLD=5.00  # Alert at $5
   ```

4. **Monitor Usage**
   - Check OpenAI dashboard: https://platform.openai.com/usage
   - Set monthly budget limits

### Estimated Monthly Costs

**Scenario: 100 students, 10 messages each/day**

```
Messages per month: 100 × 10 × 30 = 30,000 messages
Average tokens per message: 1,000 tokens (500 in + 500 out)
Total tokens: 30M tokens

Cost calculation:
- Input: 15M tokens × $0.15 / 1M = $2.25
- Output: 15M tokens × $0.60 / 1M = $9.00
Total: $11.25/month
```

**Cost per student: $0.11/month** 💰

---

## Phase 2 Integration (Hybrid Intelligence)

This AI integration supports **Phase 2 - Hybrid Intelligence**:

### Premium Features (Selective AI)

You can gate certain AI features behind a paywall:

```typescript
// In route.ts
export async function POST(request: NextRequest) {
  const user = await getUser(request);

  // Only premium users get AI features
  if (!user.isPremium && useSkill === 'advanced-mentor') {
    return NextResponse.json(
      { error: 'Premium feature - upgrade to access AI mentor' },
      { status: 403 }
    );
  }

  // ... rest of AI logic
}
```

### Cost Tracking Per User

```typescript
// Track AI usage per user
await db.aiUsage.create({
  userId: user.id,
  tokens: usage.total_tokens,
  cost: calculatedCost,
  model: 'gpt-4o-mini',
  timestamp: new Date(),
});
```

---

## Adding to Navigation

Update `frontend/app/layout.tsx` or your navigation component:

```tsx
const navLinks = [
  { href: '/courses', label: 'Courses' },
  { href: '/ai-tutor', label: 'AI Tutor', badge: 'New' },
  { href: '/progress', label: 'Progress' },
  { href: '/quiz', label: 'Quizzes' },
];
```

---

## Security Best Practices

### 1. Never Expose API Key to Client

✅ **Correct:** API key in `.env.local` (server-side only)
```env
OPENAI_API_KEY=sk-...  # Server-side
```

❌ **Wrong:** API key in client code
```typescript
const openai = new OpenAI({ apiKey: 'sk-...' }); // NEVER!
```

### 2. Rate Limiting

Add rate limiting to prevent abuse:

```typescript
// In route.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
});

export async function POST(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429 }
    );
  }

  // ... rest of logic
}
```

### 3. Input Validation

```typescript
// Validate message length
if (input.length > 1000) {
  return NextResponse.json(
    { error: 'Message too long (max 1000 chars)' },
    { status: 400 }
  );
}
```

---

## Troubleshooting

### Issue: "Invalid API Key"

**Solution:**
1. Check `.env.local` has correct key
2. Restart Next.js server
3. Verify key at https://platform.openai.com/api-keys

### Issue: "Rate limit exceeded"

**Solution:**
1. Check OpenAI usage: https://platform.openai.com/usage
2. Upgrade your OpenAI plan
3. Add billing credit

### Issue: "Module not found: openai"

**Solution:**
```bash
cd frontend
npm install openai
```

### Issue: Cost too high

**Solutions:**
1. Reduce `OPENAI_MAX_TOKENS` to 500
2. Use caching for repeated queries
3. Switch to `gpt-3.5-turbo` if quality sufficient

---

## Advanced: Streaming Responses

For better UX, enable streaming:

```typescript
// In route.ts
const stream = await openai.chat.completions.create({
  model: 'gpt-4o-mini',
  messages: chatMessages,
  stream: true,
});

const encoder = new TextEncoder();
const readable = new ReadableStream({
  async start(controller) {
    for await (const chunk of stream) {
      const text = chunk.choices[0]?.delta?.content || '';
      controller.enqueue(encoder.encode(text));
    }
    controller.close();
  },
});

return new Response(readable, {
  headers: { 'Content-Type': 'text/event-stream' },
});
```

---

## Monitoring Dashboard

Create a simple monitoring page:

```typescript
// app/admin/ai-stats/page.tsx
export default async function AIStatsPage() {
  const stats = await db.aiUsage.aggregate({
    _sum: { tokens: true, cost: true },
    _count: true,
  });

  return (
    <div>
      <h1>AI Usage Statistics</h1>
      <p>Total Messages: {stats._count}</p>
      <p>Total Tokens: {stats._sum.tokens?.toLocaleString()}</p>
      <p>Total Cost: ${stats._sum.cost?.toFixed(2)}</p>
    </div>
  );
}
```

---

## Next Steps

1. ✅ Get OpenAI API key
2. ✅ Configure `.env.local`
3. ✅ Restart Next.js
4. ✅ Test at http://localhost:3000/ai-tutor
5. ⬜ Add to navigation
6. ⬜ Enable cost tracking in database
7. ⬜ Deploy to production
8. ⬜ Set up monitoring

---

## Production Deployment

### Environment Variables

In Netlify/Vercel, add:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
```

### Update Server URL

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com/api
```

---

## Support

- OpenAI Documentation: https://platform.openai.com/docs
- API Reference: https://platform.openai.com/docs/api-reference
- Pricing: https://openai.com/api/pricing/
- Rate Limits: https://platform.openai.com/docs/guides/rate-limits

---

**Cost Summary:**
- Average cost per message: $0.0001-0.0005
- 100 students × 10 msgs/day: ~$11/month
- **94% cheaper than GPT-4o**

Enjoy your cost-effective AI tutor! 🚀
