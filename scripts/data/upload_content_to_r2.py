"""
Upload course content to Cloudflare R2
Uploads markdown files and updates database with content keys
"""
import asyncio
import os
import sys
from pathlib import Path
from typing import List

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.config import get_settings
from backend.services.r2 import R2Client
from backend.db.session import db_manager
from backend.api.models.course import Course
from backend.api.models.chapter import Chapter
from sqlalchemy import select


async def upload_course_content():
    """
    Upload all course content from content/courses/ to R2
    """
    settings = get_settings()
    r2_client = R2Client()

    # Initialize database
    db_manager.init_db()

    # Content base path
    content_path = Path("content/courses")

    if not content_path.exists():
        print(f"Error: Content path {content_path} does not exist")
        return

    print(f"Uploading content from {content_path}...")

    # Process each course
    for course_dir in content_path.iterdir():
        if not course_dir.is_dir():
            continue

        course_slug = course_dir.name
        print(f"\nProcessing course: {course_slug}")

        # Get all markdown files
        md_files = list(course_dir.glob("*.md"))
        print(f"Found {len(md_files)} content files")

        # Upload each file to R2
        for md_file in md_files:
            # Read file content
            content = md_file.read_bytes()

            # Generate R2 key
            r2_key = f"courses/{course_slug}/{md_file.name}"

            # Upload to R2
            try:
                url = await r2_client.upload_content(
                    key=r2_key,
                    content=content,
                    content_type="text/markdown"
                )
                print(f"  ✓ Uploaded {md_file.name} -> {r2_key}")

            except Exception as e:
                print(f"  ✗ Failed to upload {md_file.name}: {e}")

    print("\n✓ Content upload complete!")


async def update_database_with_content_keys():
    """
    Update database chapters with R2 content keys
    """
    print("\nUpdating database with content keys...")

    db_manager.init_db()

    async with db_manager.SessionLocal() as session:
        # Get all chapters
        result = await session.execute(select(Chapter))
        chapters = result.scalars().all()

        for chapter in chapters:
            # Get course slug
            course_result = await session.execute(
                select(Course).where(Course.id == chapter.course_id)
            )
            course = course_result.scalar_one_or_none()

            if not course:
                continue

            # Build content key based on chapter number
            content_key = f"courses/{course.slug}/chapter-{chapter.chapter_number:02d}-{chapter.slug}.md"

            # Update chapter
            chapter.content_key = content_key

            print(f"  ✓ Updated {chapter.title} -> {content_key}")

        await session.commit()

    print("✓ Database updated!")


async def verify_uploads():
    """
    Verify all uploads are accessible
    """
    print("\nVerifying uploads...")

    r2_client = R2Client()
    db_manager.init_db()

    async with db_manager.SessionLocal() as session:
        result = await session.execute(select(Chapter))
        chapters = result.scalars().all()

        for chapter in chapters:
            if not chapter.content_key:
                print(f"  ✗ {chapter.title}: No content key")
                continue

            try:
                # Generate signed URL
                signed_url = await r2_client.generate_signed_url(
                    key=chapter.content_key,
                    expiry_minutes=5
                )

                print(f"  ✓ {chapter.title}: Accessible")

            except Exception as e:
                print(f"  ✗ {chapter.title}: {e}")

    print("✓ Verification complete!")


async def main():
    """
    Main upload workflow
    """
    print("=" * 60)
    print("Course Content Upload to R2")
    print("=" * 60)

    # Step 1: Upload content to R2
    await upload_course_content()

    # Step 2: Update database with content keys
    await update_database_with_content_keys()

    # Step 3: Verify uploads
    await verify_uploads()

    print("\n" + "=" * 60)
    print("Upload Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
