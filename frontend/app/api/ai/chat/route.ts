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
  const basePrompt = `You are an expert AI tutor for Course Companion FTE, specializing in AI Agent Development.

Core Principles:
1. **Content Grounding**: Base all explanations on the provided course content
2. **Adaptive Teaching**: Match explanation complexity to student level
3. **Citation**: Always mention which chapter information comes from
4. **Conciseness**: Be clear and brief, expand only when asked

Available Course Context:
${context?.courseContent || 'No specific course content provided'}

Current Chapter: ${context?.currentChapter || 'None'}
Student Level: ${context?.studentLevel || 'Intermediate'}
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
Your task: Conduct engaging quizzes with encouraging feedback.

Steps:
1. Present questions clearly
2. Wait for answers
3. Provide immediate feedback
4. Explain correct answers
5. Celebrate successes, encourage on mistakes

Be enthusiastic and supportive!`,

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
1. Acknowledge progress made
2. Highlight specific improvements
3. Connect to larger learning goals
4. Encourage next steps

Be genuinely encouraging and specific in praise.`,
  };

  return skillPrompts[skill || ''] || basePrompt;
}
