"""
Seed initial courses into the database
"""
import asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.api.models.course import Course
from backend.api.models.chapter import Chapter
from backend.core.config import get_settings

async def seed_courses():
    settings = get_settings()

    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True
    )

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Clear existing courses and chapters
        await session.execute(delete(Chapter))
        await session.execute(delete(Course))
        await session.commit()
        print("[INFO] Cleared existing courses and chapters")

        # Course 1: Introduction to AI Agents
        course1 = Course(
            title="Introduction to AI Agents",
            slug="introduction-to-ai-agents",
            description="Learn the fundamentals of building AI agents with modern tools and techniques.",
            difficulty_level="beginner",
            estimated_hours=32,  # 4 weeks * 8 hours
            is_published=True,
            free_chapter_limit=3,
            required_tier="free",
            total_chapters=5
        )
        session.add(course1)
        await session.flush()

        # Add chapters for Course 1
        for i in range(1, 6):
            chapter = Chapter(
                course_id=course1.id,
                chapter_number=i,
                slug=f"chapter-{i}",
                title=f"Chapter {i}: AI Agent Fundamentals",
                description=f"Learn AI agent concepts - part {i}",
                content_key=f"ai-agents-intro/chapter-{i:02d}.md",
                estimated_minutes=60
            )
            session.add(chapter)

        # Course 2: Cloud-Native Python Development
        course2 = Course(
            title="Cloud-Native Python Development",
            slug="cloud-native-python-development",
            description="Master cloud-native development with Python, containers, and Kubernetes.",
            difficulty_level="intermediate",
            estimated_hours=48,  # 6 weeks * 8 hours
            is_published=True,
            free_chapter_limit=3,
            required_tier="free",
            total_chapters=8
        )
        session.add(course2)
        await session.flush()

        # Add chapters for Course 2
        for i in range(1, 9):
            chapter = Chapter(
                course_id=course2.id,
                chapter_number=i,
                slug=f"chapter-{i}",
                title=f"Chapter {i}: Cloud-Native Python",
                description=f"Cloud-native development concepts - part {i}",
                content_key=f"cloud-python/chapter-{i:02d}.md",
                estimated_minutes=90
            )
            session.add(chapter)

        # Course 3: Generative AI Fundamentals
        course3 = Course(
            title="Generative AI Fundamentals",
            slug="generative-ai-fundamentals",
            description="Explore the foundations of generative AI, LLMs, prompting, and RAG systems.",
            difficulty_level="intermediate",
            estimated_hours=40,  # 5 weeks * 8 hours
            is_published=True,
            free_chapter_limit=3,
            required_tier="free",
            total_chapters=7
        )
        session.add(course3)
        await session.flush()

        # Add chapters for Course 3
        for i in range(1, 8):
            chapter = Chapter(
                course_id=course3.id,
                chapter_number=i,
                slug=f"chapter-{i}",
                title=f"Chapter {i}: Generative AI Concepts",
                description=f"Generative AI fundamentals - part {i}",
                content_key=f"generative-ai/chapter-{i:02d}.md",
                estimated_minutes=80
            )
            session.add(chapter)

        # Course 4: Modern Python with Typing
        course4 = Course(
            title="Modern Python with Typing",
            slug="modern-python-with-typing",
            description="Advanced Python programming with type hints, async/await, and best practices.",
            difficulty_level="advanced",
            estimated_hours=24,  # 3 weeks * 8 hours
            is_published=True,
            free_chapter_limit=3,
            required_tier="free",
            total_chapters=6
        )
        session.add(course4)
        await session.flush()

        # Add chapters for Course 4
        for i in range(1, 7):
            chapter = Chapter(
                course_id=course4.id,
                chapter_number=i,
                slug=f"chapter-{i}",
                title=f"Chapter {i}: Modern Python Techniques",
                description=f"Advanced Python concepts - part {i}",
                content_key=f"modern-python/chapter-{i:02d}.md",
                estimated_minutes=70
            )
            session.add(chapter)

        await session.commit()

        print("\n[OK] Courses seeded successfully!")
        print("   - Introduction to AI Agents (5 chapters, beginner)")
        print("   - Cloud-Native Python Development (8 chapters, intermediate)")
        print("   - Generative AI Fundamentals (7 chapters, intermediate)")
        print("   - Modern Python with Typing (6 chapters, advanced)")
        print(f"\n   Total: 4 courses with 26 chapters")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_courses())
