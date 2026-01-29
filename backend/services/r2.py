"""
Cloudflare R2 client for Course Companion FTE
Handles content storage and retrieval from Cloudflare R2
"""
import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
import os
from datetime import timedelta
import mimetypes

from backend.core.config import get_settings
from backend.core.exceptions import StorageError


class R2Client:
    """
    Cloudflare R2 client for storing and retrieving course content
    """
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    def get_client(self):
        """
        Initialize and return R2 client
        """
        if self._client is None:
            self._client = boto3.client(
                's3',
                endpoint_url=self.settings.R2_ENDPOINT_URL,
                aws_access_key_id=self.settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.R2_SECRET_ACCESS_KEY,
                region_name=self.settings.R2_REGION
            )
        return self._client

    async def init_client(self) -> bool:
        """
        Initialize the R2 client and verify connectivity

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            client = self.get_client()

            # Test connectivity by listing objects (without actually retrieving them)
            client.list_objects_v2(
                Bucket=self.settings.R2_BUCKET_NAME,
                MaxKeys=0  # Don't actually return any objects, just test access
            )

            return True
        except ClientError as e:
            raise StorageError(f"Failed to initialize R2 client: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error initializing R2 client: {str(e)}")

    async def upload_content(self, key: str, content: bytes, content_type: Optional[str] = None) -> str:
        """
        Upload content to R2 bucket

        Args:
            key: Object key in the bucket (e.g., 'courses/ai-agent-development/chapter-01.md')
            content: Content to upload as bytes
            content_type: MIME type of the content (detected automatically if not provided)

        Returns:
            Full URL of the uploaded object
        """
        try:
            client = self.get_client()

            if content_type is None:
                # Auto-detect content type from file extension
                content_type, _ = mimetypes.guess_type(key)
                if content_type is None:
                    content_type = 'application/octet-stream'

            client.put_object(
                Bucket=self.settings.R2_BUCKET_NAME,
                Key=key,
                Body=content,
                ContentType=content_type
            )

            # Return the object URL
            return f"{self.settings.R2_ENDPOINT_URL}/{self.settings.R2_BUCKET_NAME}/{key}"
        except ClientError as e:
            raise StorageError(f"Failed to upload content to R2: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error uploading content to R2: {str(e)}")

    async def generate_signed_url(self, key: str, expiry_minutes: int = 60) -> str:
        """
        Generate a presigned URL for accessing content in R2

        Args:
            key: Object key in the bucket
            expiry_minutes: Number of minutes until the URL expires

        Returns:
            Presigned URL that can be used to access the content
        """
        try:
            client = self.get_client()

            url = client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.settings.R2_BUCKET_NAME, 'Key': key},
                ExpiresIn=expiry_minutes * 60  # Convert minutes to seconds
            )

            return url
        except ClientError as e:
            raise StorageError(f"Failed to generate signed URL for R2 object: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error generating signed URL for R2 object: {str(e)}")

    async def download_content(self, key: str) -> bytes:
        """
        Download content directly from R2 bucket

        Args:
            key: Object key in the bucket

        Returns:
            Content as bytes
        """
        try:
            client = self.get_client()

            response = client.get_object(
                Bucket=self.settings.R2_BUCKET_NAME,
                Key=key
            )

            return response['Body'].read()
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise StorageError(f"Object '{key}' does not exist in R2 bucket")
            else:
                raise StorageError(f"Failed to download content from R2: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error downloading content from R2: {str(e)}")

    async def delete_content(self, key: str) -> bool:
        """
        Delete content from R2 bucket

        Args:
            key: Object key in the bucket

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            client = self.get_client()

            client.delete_object(
                Bucket=self.settings.R2_BUCKET_NAME,
                Key=key
            )

            return True
        except ClientError as e:
            raise StorageError(f"Failed to delete content from R2: {str(e)}")
        except Exception as e:
            raise StorageError(f"Unexpected error deleting content from R2: {str(e)}")

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on R2 connectivity

        Returns:
            Dictionary with health check results
        """
        try:
            client = self.get_client()

            # Try to list objects to verify access
            response = client.list_objects_v2(
                Bucket=self.settings.R2_BUCKET_NAME,
                MaxKeys=1  # Just check if we can access the bucket
            )

            return {
                "status": "healthy",
                "bucket_accessible": True,
                "error": None
            }
        except ClientError as e:
            return {
                "status": "unhealthy",
                "bucket_accessible": False,
                "error": str(e)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "bucket_accessible": False,
                "error": f"Unexpected error: {str(e)}"
            }


# Global R2 client instance
r2_client = R2Client()


async def get_r2_client() -> R2Client:
    """
    Dependency to provide R2 client to FastAPI endpoints
    """
    return r2_client