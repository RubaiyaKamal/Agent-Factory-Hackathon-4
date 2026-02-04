import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Token pricing (per 1M tokens)
const PRICING = {
  'gpt-4o': { input: 2.50, output: 10.00 },
  'gpt-4o-mini': { input: 0.15, output: 0.60 },
  'gpt-3.5-turbo': { input: 0.50, output: 1.50 },
};

// Calculate cost
function calculateCost(model: string, inputTokens: number, outputTokens: number): number {
  const pricing = PRICING[model as keyof typeof PRICING] || PRICING['gpt-4o-mini'];
  const inputCost = (inputTokens / 1_000_000) * pricing.input;
  const outputCost = (outputTokens / 1_000_000) * pricing.output;
  return inputCost + outputCost;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { messages, context, useSkill } = body;

    // Get model from env or default to gpt-4o-mini
    const model = process.env.OPENAI_MODEL || 'gpt-4o-mini';
    const maxTokens = parseInt(process.env.OPENAI_MAX_TOKENS || '1000');
    const temperature = parseFloat(process.env.OPENAI_TEMPERATURE || '0.7');

    // System prompt based on skill
    const systemPrompt = getSystemPrompt(useSkill, context);

    // Prepare messages
    const chatMessages: OpenAI.Chat.ChatCompletionMessageParam[] = [
      { role: 'system', content: systemPrompt },
      ...messages.map((msg: any) => ({
        role: msg.role,
        content: msg.content,
      })),
    ];

    // Call OpenAI API
    const startTime = Date.now();
    const completion = await openai.chat.completions.create({
      model,
      messages: chatMessages,
      max_tokens: maxTokens,
      temperature,
      stream: false,
    });

    const responseTime = Date.now() - startTime;

    // Extract response
    const assistantMessage = completion.choices[0]?.message?.content || '';
    const usage = completion.usage;

    // Calculate cost
    const cost = calculateCost(
      model,
      usage?.prompt_tokens || 0,
      usage?.completion_tokens || 0
    );

    // Return response with metadata
    return NextResponse.json({
      message: assistantMessage,
      usage: {
        prompt_tokens: usage?.prompt_tokens || 0,
        completion_tokens: usage?.completion_tokens || 0,
        total_tokens: usage?.total_tokens || 0,
      },
      cost: {
        amount: cost,
        currency: 'USD',
        model,
      },
      metadata: {
        response_time_ms: responseTime,
        model,
        finish_reason: completion.choices[0]?.finish_reason,
      },
    });
  } catch (error: any) {
    console.error('AI Chat Error:', error);
    return NextResponse.json(
      {
        error: 'Failed to get AI response',
        details: error.message,
      },
      { status: 500 }
    );
  }
}

function getSystemPrompt(skill: string | undefined, context: any): string {
  const userProgressInfo = context?.userProgress
    ? `\nUser Progress:
- Completed: ${context.userProgress.completedChapters}/${context.userProgress.totalChapters} chapters
- Current Streak: ${context.userProgress.currentStreak} days`
    : '';

  const basePrompt = `You are an expert AI tutor for Course Companion FTE, specializing in AI Agent Development.

**IMPORTANT COURSE TERMINOLOGY:**
- **MCP** = Model Context Protocol (NOT Model Context Provider)
- MCP is a standard protocol that allows Claude to access tools and services
- MCP Servers expose resources, tools, and prompts that AI can use

Core Principles:
1. **Content Grounding**: Base all explanations on the provided course content
2. **Adaptive Teaching**: Match explanation complexity to student level
3. **Citation**: Always mention which chapter information comes from
4. **Conciseness**: Be clear and brief, expand only when asked

Available Course Context:
${context?.courseContent || 'AI Agent Development Course covering Claude SDK, MCP (Model Context Protocol), and Agent Skills'}

Current Chapter: ${context?.currentChapter || 'Introduction to MCP (Model Context Protocol)'}
Student Level: ${context?.studentLevel || 'Intermediate'}${userProgressInfo}

When users ask about their progress, use the progress information above to provide specific feedback.
When explaining MCP, always use the full term "Model Context Protocol" at least once.
`;

  // Skill-specific prompts
  const skillPrompts: Record<string, string> = {
    'concept-explainer': `${basePrompt}

**Skill: Concept Explainer**
Your task: Explain concepts clearly at the appropriate level.

Steps:
1. Assess student's current understanding
2. Search for relevant course content
3. Explain using analogies and examples
4. Offer to go deeper if interested

Use simple language for beginners, technical details for advanced students.`,

    'quiz-master': `${basePrompt}

**Skill: Quiz Master**
Your task: Conduct engaging MCQ quizzes with encouraging feedback.

**CRITICAL QUIZ FORMAT - FOLLOW EXACTLY:**

1. **Ask ONE question at a time** (never multiple questions together)
2. **Always provide 4 options** labeled A, B, C, D
3. **Format like this:**

   Question 1: [Question text]

   A) [Option 1]
   B) [Option 2]
   C) [Option 3]
   D) [Option 4]

   Choose your answer (A, B, C, or D)

4. **After user answers:**
   - If correct: ✅ "Correct! [Explanation why it's right]"
   - If wrong: ❌ "Not quite. The correct answer is [X]. [Explanation]"
   - Then ask: "Ready for the next question?"

5. **Keep score** (e.g., "Score: 2/3")

6. **Be enthusiastic!** Use phrases like:
   - "Great job!"
   - "You're on fire!"
   - "Nice work!"
   - "Don't worry, you'll get the next one!"

Never ask all questions at once. Always wait for the user's answer before moving to the next question.`,

    'socratic-tutor': `${basePrompt}

**Skill: Socratic Tutor**
Your task: Guide learning through questions, not direct answers.

Steps:
1. Ask probing questions to reveal student's thinking
2. Guide discovery through strategic questioning
3. Help student arrive at answers themselves
4. Only explain after student has explored

Ask questions that build on what they know.`,

    'progress-motivator': `${basePrompt}

**Skill: Progress Motivator**
Your task: Celebrate achievements and maintain motivation.

Steps:
1. Review the user's progress data (chapters completed, streak)
2. Acknowledge specific milestones (e.g., "You've completed 5 chapters!")
3. Celebrate streak consistency
4. Highlight what they've learned so far
5. Encourage next steps with specific suggestions

When user asks "show my progress":
- Share their current stats from the context
- Celebrate what they've accomplished
- Encourage them to keep going
- Suggest what to learn next

Be genuinely encouraging and specific in praise!`,
  };

  return skillPrompts[skill || ''] || basePrompt;
}
