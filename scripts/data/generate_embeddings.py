"""
Generate embeddings for course content
Uses offline sentence-transformers model (NO LLM API calls)
CONSTITUTIONAL REQUIREMENT: All embeddings generated locally, no external API calls
"""
import asyncio
import sys
import json
from pathlib import Path
from typing import List

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.config import get_settings
from backend.db.session import db_manager
from backend.api.models.chapter import Chapter
from backend.services.r2 import R2Client
from sqlalchemy import select


# Check if sentence-transformers is available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("⚠️  WARNING: sentence-transformers not installed")
    print("   Install with: pip install sentence-transformers")
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class EmbeddingGenerator:
    """
    Generates embeddings for course content using local models
    """

    def __init__(self):
        self.settings = get_settings()
        self.r2_client = R2Client()
        self.model = None

    def load_model(self):
        """
        Load sentence-transformers model (offline)
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise RuntimeError("sentence-transformers not installed")

        print(f"Loading model: {self.settings.EMBEDDINGS_MODEL}")
        print("(This may take a moment on first run...)")

        # Load model - will download on first use, then cached locally
        self.model = SentenceTransformer(self.settings.EMBEDDINGS_MODEL)

        print(f"✓ Model loaded: {self.settings.EMBEDDINGS_MODEL}")
        print(f"  Embedding dimension: {self.model.get_sentence_embedding_dimension()}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding
        """
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)

        # Convert to list for JSON serialization
        return embedding.tolist()

    async def get_chapter_content(self, chapter: Chapter) -> str:
        """
        Fetch chapter content from R2

        Args:
            chapter: Chapter object

        Returns:
            Chapter content as string
        """
        try:
            content_bytes = await self.r2_client.download_content(
                chapter.content_key
            )
            return content_bytes.decode('utf-8')
        except Exception as e:
            print(f"  ✗ Error downloading content: {e}")
            return ""

    def extract_text_for_embedding(self, content: str) -> str:
        """
        Extract relevant text from markdown content

        Args:
            content: Full markdown content

        Returns:
            Cleaned text for embedding
        """
        # Simple text extraction - remove markdown formatting
        # In production, you might want more sophisticated processing

        # Remove code blocks
        import re
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remove inline code
        content = re.sub(r'`[^`]*`', '', content)

        # Remove headers markers (keep text)
        content = re.sub(r'#{1,6}\s+', '', content)

        # Remove links (keep text)
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content).strip()

        # Truncate if too long (models have max input length)
        max_chars = 8000  # Conservative limit
        if len(content) > max_chars:
            content = content[:max_chars]

        return content

    async def generate_embeddings_for_all_chapters(self):
        """
        Generate and store embeddings for all published chapters
        """
        print("\n" + "=" * 60)
        print("Generating Embeddings for Course Content")
        print("=" * 60)

        # Initialize database
        db_manager.init_db()

        async with db_manager.SessionLocal() as session:
            # Get all published chapters
            result = await session.execute(
                select(Chapter).where(Chapter.is_published == True)
            )
            chapters = result.scalars().all()

            print(f"\nFound {len(chapters)} published chapters")

            if not chapters:
                print("No chapters to process")
                return

            # Load model
            self.load_model()

            # Process each chapter
            success_count = 0
            error_count = 0

            for i, chapter in enumerate(chapters, 1):
                print(f"\n[{i}/{len(chapters)}] Processing: {chapter.title}")

                # Check if already has embedding
                if chapter.embedding:
                    print(f"  ℹ️  Already has embedding, skipping...")
                    continue

                # Get content
                content = await self.get_chapter_content(chapter)

                if not content:
                    print(f"  ✗ No content available")
                    error_count += 1
                    continue

                # Extract text for embedding
                text = self.extract_text_for_embedding(content)
                print(f"  Text length: {len(text)} characters")

                # Generate embedding
                try:
                    embedding = self.generate_embedding(text)
                    print(f"  ✓ Generated embedding ({len(embedding)} dimensions)")

                    # Store embedding as JSON
                    chapter.embedding = json.dumps(embedding)

                    success_count += 1

                except Exception as e:
                    print(f"  ✗ Error generating embedding: {e}")
                    error_count += 1

            # Commit changes
            await session.commit()

            print("\n" + "=" * 60)
            print("Embedding Generation Complete")
            print("=" * 60)
            print(f"✓ Success: {success_count}")
            print(f"✗ Errors: {error_count}")
            print(f"Total: {len(chapters)}")

    async def test_semantic_search(self, query: str):
        """
        Test semantic search with a query

        Args:
            query: Search query to test
        """
        print("\n" + "=" * 60)
        print(f"Testing Semantic Search: '{query}'")
        print("=" * 60)

        # Load model
        if not self.model:
            self.load_model()

        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        print(f"\n✓ Query embedding generated ({len(query_embedding)} dimensions)")

        # Initialize database
        db_manager.init_db()

        async with db_manager.SessionLocal() as session:
            # Get all chapters with embeddings
            result = await session.execute(
                select(Chapter).where(
                    Chapter.is_published == True,
                    Chapter.embedding.isnot(None)
                )
            )
            chapters = result.scalars().all()

            if not chapters:
                print("No chapters with embeddings found")
                return

            print(f"Comparing with {len(chapters)} chapters...")

            # Calculate similarities
            from backend.services.search_service import SearchService
            search_service = SearchService(session, self.r2_client)

            results = []
            for chapter in chapters:
                # Parse stored embedding
                chapter_embedding = json.loads(chapter.embedding)

                # Calculate similarity
                similarity = search_service.calculate_cosine_similarity(
                    query_embedding,
                    chapter_embedding
                )

                results.append({
                    "chapter": chapter,
                    "similarity": similarity
                })

            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)

            # Display top 5 results
            print("\nTop 5 Results:")
            for i, result in enumerate(results[:5], 1):
                chapter = result["chapter"]
                similarity = result["similarity"]
                print(f"\n{i}. {chapter.title}")
                print(f"   Similarity: {similarity:.4f}")
                print(f"   Chapter {chapter.chapter_number}")


async def main():
    """
    Main function
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate embeddings for course content"
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Test semantic search with a query",
        metavar="QUERY"
    )

    args = parser.parse_args()

    generator = EmbeddingGenerator()

    if args.test:
        # Test mode
        await generator.test_semantic_search(args.test)
    else:
        # Generate embeddings
        await generator.generate_embeddings_for_all_chapters()


if __name__ == "__main__":
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("\nERROR: sentence-transformers is required")
        print("Install with: pip install sentence-transformers")
        sys.exit(1)

    asyncio.run(main())
