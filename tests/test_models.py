import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from models.user import User
from models.video import Video
from models.script import Script


class TestUserModel:
    """Tests for User model"""

    def test_create_user(self, db_session: Session):
        """Test creating a user with required fields"""
        user = User(
            username="testuser",
            password_hash="hashed_password_123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.password_hash == "hashed_password_123"
        assert user.role == "user"
        assert user.created_at is not None

    def test_user_unique_username(self, db_session: Session):
        """Test that username must be unique"""
        user1 = User(username="uniqueuser", password_hash="hash1")
        db_session.add(user1)
        db_session.commit()

        user2 = User(username="uniqueuser", password_hash="hash2")
        db_session.add(user2)
        with pytest.raises(Exception):
            db_session.commit()

    def test_user_relationship_with_videos(self, db_session: Session):
        """Test user has relationship with videos"""
        user = User(username="videouser", password_hash="hash123")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert hasattr(user, 'videos')
        assert user.videos == []


class TestVideoModel:
    """Tests for Video model"""

    def test_create_video(self, db_session: Session):
        """Test creating a video with required fields"""
        user = User(username="videocreator", password_hash="hash123")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test_video.mp4",
            original_filename="test_video.mp4",
            duration=120
        )
        db_session.add(video)
        db_session.commit()
        db_session.refresh(video)

        assert video.id is not None
        assert video.user_id == user.id
        assert video.file_path == "/videos/test_video.mp4"
        assert video.original_filename == "test_video.mp4"
        assert video.duration == 120
        assert video.status == "pending"
        assert video.created_at is not None

    def test_video_relationship_with_user(self, db_session: Session):
        """Test video has relationship with user"""
        user = User(username="testuser2", password_hash="hash456")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()
        db_session.refresh(video)

        assert hasattr(video, 'user')
        assert video.user.username == "testuser2"

    def test_video_relationship_with_scripts(self, db_session: Session):
        """Test video has relationship with scripts"""
        user = User(username="testuser3", password_hash="hash789")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()
        db_session.refresh(video)

        assert hasattr(video, 'scripts')
        assert video.scripts == []

    def test_video_status_values(self, db_session: Session):
        """Test video status can be set to different values"""
        user = User(username="statususer", password_hash="hash111")
        db_session.add(user)
        db_session.commit()

        for status in ["pending", "processing", "done", "failed"]:
            video = Video(
                user_id=user.id,
                file_path=f"/videos/{status}.mp4",
                original_filename=f"{status}.mp4",
                status=status
            )
            db_session.add(video)
            db_session.commit()
            db_session.refresh(video)
            assert video.status == status
            db_session.delete(video)
            db_session.commit()


class TestScriptModel:
    """Tests for Script model"""

    def test_create_script(self, db_session: Session):
        """Test creating a script with required fields"""
        user = User(username="scriptuser", password_hash="hash222")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/script_test.mp4",
            original_filename="script_test.mp4"
        )
        db_session.add(video)
        db_session.commit()

        script = Script(
            video_id=video.id,
            content="This is the script content",
            version=1
        )
        db_session.add(script)
        db_session.commit()
        db_session.refresh(script)

        assert script.id is not None
        assert script.video_id == video.id
        assert script.content == "This is the script content"
        assert script.version == 1
        assert script.status == "draft"
        assert script.created_at is not None

    def test_script_relationship_with_video(self, db_session: Session):
        """Test script has relationship with video"""
        user = User(username="scriptuser2", password_hash="hash333")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()

        script = Script(
            video_id=video.id,
            content="Script content"
        )
        db_session.add(script)
        db_session.commit()
        db_session.refresh(script)

        assert hasattr(script, 'video')
        assert script.video.id == video.id

    def test_script_json_fields(self, db_session: Session):
        """Test script can store JSON data in titles, tags, suggestions"""
        import json

        user = User(username="scriptuser3", password_hash="hash444")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()

        titles = json.dumps(["Title 1", "Title 2"])
        tags = json.dumps(["tag1", "tag2", "tag3"])
        suggestions = json.dumps(["Improve intro", "Add more details"])

        script = Script(
            video_id=video.id,
            content="Script content",
            titles=titles,
            tags=tags,
            suggestions=suggestions
        )
        db_session.add(script)
        db_session.commit()
        db_session.refresh(script)

        assert script.titles == titles
        assert script.tags == tags
        assert script.suggestions == suggestions
        assert json.loads(script.titles) == ["Title 1", "Title 2"]
        assert json.loads(script.tags) == ["tag1", "tag2", "tag3"]

    def test_script_status_values(self, db_session: Session):
        """Test script status can be set to different values"""
        user = User(username="scriptuser4", password_hash="hash555")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()

        for status in ["draft", "reviewed", "approved"]:
            script = Script(
                video_id=video.id,
                content=f"Script with status {status}",
                status=status
            )
            db_session.add(script)
            db_session.commit()
            db_session.refresh(script)
            assert script.status == status
            db_session.delete(script)
            db_session.commit()

    def test_script_version_default(self, db_session: Session):
        """Test script version defaults to 1"""
        user = User(username="scriptuser5", password_hash="hash666")
        db_session.add(user)
        db_session.commit()

        video = Video(
            user_id=user.id,
            file_path="/videos/test.mp4",
            original_filename="test.mp4"
        )
        db_session.add(video)
        db_session.commit()

        script = Script(
            video_id=video.id,
            content="Script content"
        )
        db_session.add(script)
        db_session.commit()
        db_session.refresh(script)

        assert script.version == 1
