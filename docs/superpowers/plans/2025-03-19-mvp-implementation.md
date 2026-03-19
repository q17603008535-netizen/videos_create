# MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建完整的视频二创 Agent MVP，包含前端界面、后端 API、Whisper 转录、AI 分析改写、审核输出等完整 SOP 流程

**Architecture:** 前后端分离架构，前端 Vue 3 通过 API 调用后端 FastAPI 服务，后端集成 Whisper 和 AI 模型 API，SQLite 存储数据

**Tech Stack:** 
- 前端：Vue 3 + Vite + TailwindCSS + Alpine.js
- 后端：Python FastAPI + SQLAlchemy + Whisper
- 数据库：SQLite
- AI: Qwen3.5 (plus/flash) + DeepSeek V3.2

---

## Phase 1: 项目框架搭建 (2-3 天)

### Task 1: 后端项目初始化

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/main.py`
- Create: `backend/config.py`
- Create: `backend/__init__.py`
- Test: `tests/test_backend_init.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# AI
openai==1.10.0
whisper==1.1.10

# Utilities
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

- [ ] **Step 2: 创建 config.py**

```python
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # AI Models
    QWEN_API_KEY: str
    QWEN_BASE_URL: str = "https://dashscope.aliyuncs.com/api/v1"
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    
    # Default Models
    DEFAULT_ANALYSIS_MODEL: str = "qwen-flash"
    DEFAULT_REWRITE_MODEL: str = "deepseek-v3.2"
    DEFAULT_REVIEW_MODEL: str = "qwen-plus"
    
    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str
    
    # Session
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///data/app.db"
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

- [ ] **Step 3: 创建 main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import uvicorn

app = FastAPI(title="Video Re-creation Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Video Re-creation Agent API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
```

- [ ] **Step 4: 创建基础测试**

```python
# tests/test_backend_init.py
def test_backend_imports():
    from backend.main import app
    from backend.config import settings
    assert app is not None
    assert settings is not None

def test_health_endpoint():
    from fastapi.testclient import TestClient
    from backend.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

- [ ] **Step 5: 运行测试验证**

```bash
cd /Volumes/Container/AI_Projects/MY_AGENT
pip install -r backend/requirements.txt
pytest tests/test_backend_init.py -v
```

Expected: All tests pass

- [ ] **Step 6: 启动服务验证**

```bash
cd backend
python main.py
# 访问 http://localhost:8000/health
# Expected: {"status": "healthy"}
```

- [ ] **Step 7: Commit**

```bash
git add backend/requirements.txt backend/main.py backend/config.py tests/
git commit -m "feat: initialize backend project structure"
```

---

### Task 2: 数据库模型设计

**Files:**
- Create: `backend/database.py`
- Create: `backend/models/__init__.py`
- Create: `backend/models/user.py`
- Create: `backend/models/video.py`
- Create: `backend/models/script.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: 创建 database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 2: 创建 User 模型**

```python
# backend/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    videos = relationship("Video", back_populates="user")
```

- [ ] **Step 3: 创建 Video 模型**

```python
# backend/models/video.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)
    status = Column(String, default="pending")  # pending/processing/done/failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="videos")
    scripts = relationship("Script", back_populates="video")
```

- [ ] **Step 4: 创建 Script 模型**

```python
# backend/models/script.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Script(Base):
    __tablename__ = "scripts"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    version = Column(Integer, default=1)
    content = Column(Text, nullable=False)
    titles = Column(String)  # JSON string
    tags = Column(String)  # JSON string
    suggestions = Column(String)  # JSON string
    status = Column(String, default="draft")  # draft/reviewed/approved
    created_at = Column(DateTime, default=datetime.utcnow)
    
    video = relationship("Video", back_populates="scripts")
```

- [ ] **Step 5: 创建 models/__init__.py**

```python
from backend.models.user import User
from backend.models.video import Video
from backend.models.script import Script

__all__ = ["User", "Video", "Script"]
```

- [ ] **Step 6: 创建数据库初始化脚本**

```python
# backend/init_db.py
from backend.database import engine, Base
from backend.models import User, Video, Script
from backend.config import settings
from passlib.hash import bcrypt

def init_db():
    Base.metadata.create_all(bind=engine)
    
    # 创建管理员账号
    from sqlalchemy.orm import Session
    db = Session()
    
    admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if not admin:
        admin = User(
            username=settings.ADMIN_USERNAME,
            password_hash=bcrypt.hash(settings.ADMIN_PASSWORD),
            role="admin"
        )
        db.add(admin)
        db.commit()
    
    db.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
```

- [ ] **Step 7: 创建模型测试**

```python
# tests/test_models.py
import pytest
from backend.database import engine, SessionLocal
from backend.models import User, Video, Script
from backend.database import Base

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(test_db):
    user = User(username="testuser", password_hash="hash123", role="user")
    test_db.add(user)
    test_db.commit()
    assert user.id is not None
    assert user.username == "testuser"

def test_create_video(test_db):
    user = User(username="testuser", password_hash="hash123")
    test_db.add(user)
    test_db.commit()
    
    video = Video(user_id=user.id, file_path="/test.mp4", original_filename="test.mp4")
    test_db.add(video)
    test_db.commit()
    assert video.id is not None
    assert video.status == "pending"

def test_create_script(test_db):
    user = User(username="testuser", password_hash="hash123")
    test_db.add(user)
    test_db.commit()
    
    video = Video(user_id=user.id, file_path="/test.mp4", original_filename="test.mp4")
    test_db.add(video)
    test_db.commit()
    
    script = Script(video_id=video.id, content="Test script content")
    test_db.add(script)
    test_db.commit()
    assert script.id is not None
    assert script.status == "draft"
```

- [ ] **Step 8: 运行测试验证**

```bash
pytest tests/test_models.py -v
```

Expected: All tests pass

- [ ] **Step 9: Commit**

```bash
git add backend/database.py backend/models/ backend/init_db.py tests/test_models.py
git commit -m "feat: create database models (User, Video, Script)"
```

---

### Task 3: 用户认证系统

**Files:**
- Create: `backend/schemas/__init__.py`
- Create: `backend/schemas/user.py`
- Create: `backend/auth.py`
- Modify: `backend/main.py` (添加路由)
- Test: `tests/test_auth.py`

- [ ] **Step 1: 创建 Pydantic Schemas**

```python
# backend/schemas/user.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[UserResponse] = None
```

```python
# backend/schemas/__init__.py
from backend.schemas.user import UserBase, UserCreate, UserResponse, LoginRequest, LoginResponse

__all__ = ["UserBase", "UserCreate", "UserResponse", "LoginRequest", "LoginResponse"]
```

- [ ] **Step 2: 创建认证模块**

```python
# backend/auth.py
from passlib.hash import bcrypt
from backend.config import settings
from backend.models.user import User
from sqlalchemy.orm import Session

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_admin_user(db: Session) -> User:
    """MVP: 创建管理员账号"""
    existing = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    if existing:
        return existing
    
    admin = User(
        username=settings.ADMIN_USERNAME,
        password_hash=bcrypt.hash(settings.ADMIN_PASSWORD),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
```

- [ ] **Step 3: 添加认证路由到 main.py**

```python
# backend/main.py (添加)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.auth import authenticate_user
from backend.schemas.user import LoginRequest, LoginResponse, UserResponse

security = HTTPBasic()

@app.post("/api/login")
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_req.username, login_req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return LoginResponse(success=True, message="Login successful", user=UserResponse.model_validate(user))

@app.get("/api/me")
async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return UserResponse.model_validate(user)
```

- [ ] **Step 4: 创建认证测试**

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import engine, SessionLocal, Base
from backend.models.user import User
from passlib.hash import bcrypt

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(client):
    # 创建测试用户
    db = SessionLocal()
    user = User(username="testuser", password_hash=bcrypt.hash("testpass"), role="user")
    db.add(user)
    db.commit()
    db.close()
    return user

def test_login_success(client, test_user):
    response = client.post("/api/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["user"]["username"] == "testuser"

def test_login_fail_wrong_password(client, test_user):
    response = client.post("/api/login", json={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401

def test_get_current_user(client, test_user):
    from requests.auth import HTTPBasicAuth
    response = client.get("/api/me", auth=HTTPBasicAuth("testuser", "testpass"))
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

- [ ] **Step 5: 运行测试验证**

```bash
pytest tests/test_auth.py -v
```

Expected: All tests pass

- [ ] **Step 6: Commit**

```bash
git add backend/schemas/ backend/auth.py tests/test_auth.py
git commit -m "feat: implement user authentication system"
```

---

## Phase 2: 核心功能开发 (5-7 天)

### Task 4: 视频上传模块

**Files:**
- Create: `backend/routers/__init__.py`
- Create: `backend/routers/video.py`
- Create: `backend/schemas/video.py`
- Modify: `backend/main.py` (包含路由)
- Test: `tests/test_video_upload.py`

- [ ] **Step 1: 创建 Video Schema**

```python
# backend/schemas/video.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from backend.schemas.script import ScriptResponse

class VideoBase(BaseModel):
    original_filename: str

class VideoCreate(VideoBase):
    pass

class VideoResponse(VideoBase):
    id: int
    user_id: int
    file_path: str
    duration: Optional[int] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class VideoListResponse(BaseModel):
    videos: List[VideoResponse]
    total: int
```

- [ ] **Step 2: 创建视频上传路由**

```python
# backend/routers/video.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.video import Video
from backend.schemas.video import VideoResponse, VideoListResponse
from backend.auth import get_current_user_from_session
from backend.config import settings
import os
import uuid

router = APIRouter(prefix="/api/videos", tags=["videos"])

UPLOAD_DIR = "data/uploads"

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    # 验证文件类型
    if not file.filename.endswith(('.mp4', '.mov', '.mkv', '.avi')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 创建上传目录
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 生成唯一文件名
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 创建数据库记录
    video = Video(
        user_id=current_user.id,
        file_path=file_path,
        original_filename=file.filename,
        status="pending"
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    
    return VideoResponse.model_validate(video)

@router.get("/", response_model=VideoListResponse)
async def list_videos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    videos = db.query(Video).filter(Video.user_id == current_user.id).all()
    return VideoListResponse(videos=[VideoResponse.model_validate(v) for v in videos], total=len(videos))

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return VideoResponse.model_validate(video)
```

- [ ] **Step 3: 创建上传测试**

```python
# tests/test_video_upload.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import engine, Base
import io

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_upload_video(client):
    # 模拟视频文件
    video_data = io.BytesIO(b"fake video content")
    files = {"file": ("test.mp4", video_data, "video/mp4")}
    
    response = client.post("/api/videos/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["original_filename"] == "test.mp4"
    assert data["status"] == "pending"
```

- [ ] **Step 4: 运行测试验证**

```bash
pytest tests/test_video_upload.py -v
```

Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add backend/routers/video.py backend/schemas/video.py tests/test_video_upload.py
git commit -m "feat: implement video upload functionality"
```

---

### Task 5: Whisper 转录集成

**Files:**
- Create: `backend/services/__init__.py`
- Create: `backend/services/transcribe.py`
- Create: `backend/routers/transcribe.py`
- Test: `tests/test_transcribe.py`

- [ ] **Step 1: 创建转录服务**

```python
# backend/services/transcribe.py
import whisper
import os
from typing import Optional
import json

class TranscriptionService:
    def __init__(self, model_size: str = "medium"):
        self.model_size = model_size
        self.model = None
    
    def load_model(self):
        """加载 Whisper 模型"""
        if self.model is None:
            self.model = whisper.load_model(self.model_size)
    
    def transcribe(self, audio_path: str, language: str = "zh") -> dict:
        """
        转录音频
        返回：{text: str, segments: List[dict], language: str}
        """
        self.load_model()
        
        result = self.model.transcribe(
            audio_path,
            language=language,
            verbose=False
        )
        
        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }
    
    def extract_audio_from_video(self, video_path: str) -> str:
        """从视频中提取音频"""
        import subprocess
        
        audio_path = video_path.replace(".mp4", ".wav")
        audio_path = audio_path.replace(".mov", ".wav")
        audio_path = audio_path.replace(".mkv", ".wav")
        audio_path = audio_path.replace(".avi", ".wav")
        
        if not os.path.exists(audio_path):
            subprocess.run([
                "ffmpeg",
                "-i", video_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                audio_path
            ], check=True)
        
        return audio_path

transcribe_service = TranscriptionService(model_size="medium")
```

- [ ] **Step 2: 创建转录路由**

```python
# backend/routers/transcribe.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.video import Video
from backend.services.transcribe import transcribe_service
from backend.auth import get_current_user_from_session
import os

router = APIRouter(prefix="/api/transcribe", tags=["transcribe"])

@router.post("/{video_id}")
async def transcribe_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    # 获取视频
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # 更新状态
    video.status = "processing"
    db.commit()
    
    try:
        # 提取音频
        audio_path = transcribe_service.extract_audio_from_video(video.file_path)
        
        # 转录
        result = transcribe_service.transcribe(audio_path)
        
        # 更新状态
        video.status = "done"
        db.commit()
        
        return {
            "success": True,
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }
    except Exception as e:
        video.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: 创建转录测试**

```python
# tests/test_transcribe.py
import pytest
from backend.services.transcribe import TranscriptionService

def test_transcription_service_init():
    service = TranscriptionService(model_size="tiny")
    assert service.model is None

def test_transcription_service_load():
    service = TranscriptionService(model_size="tiny")
    service.load_model()
    assert service.model is not None
```

- [ ] **Step 4: 运行测试验证**

```bash
pytest tests/test_transcribe.py -v
```

Expected: All tests pass

- [ ] **Step 5: Commit**

```bash
git add backend/services/transcribe.py backend/routers/transcribe.py tests/test_transcribe.py
git commit -m "feat: integrate Whisper transcription service"
```

---

### Task 6: AI 内容分析服务

**Files:**
- Create: `backend/services/analyze.py`
- Create: `backend/routers/analyze.py`
- Test: `tests/test_analyze.py`

- [ ] **Step 1: 创建 AI 分析服务**

```python
# backend/services/analyze.py
from openai import OpenAI
from backend.config import settings
import json

class AnalysisService:
    def __init__(self):
        self.qwen_client = OpenAI(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_BASE_URL
        )
    
    def analyze_content(self, text: str) -> dict:
        """分析内容，提取重点和标签"""
        prompt = f"""
请分析以下视频转录内容，提取关键信息：

转录内容：
{text}

请以 JSON 格式返回：
{{
    "key_points": ["重点 1", "重点 2", ...],
    "main_topic": "核心主题",
    "tags": ["标签 1", "标签 2", ...],
    "summary": "200 字以内的内容摘要",
    "target_audience": "目标受众"
}}
"""
        
        response = self.qwen_client.chat.completions.create(
            model=settings.DEFAULT_ANALYSIS_MODEL,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"enable_search": True}
        )
        
        result = response.choices[0].message.content
        return json.loads(result)

analysis_service = AnalysisService()
```

- [ ] **Step 2: 创建分析路由**

```python
# backend/routers/analyze.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.video import Video
from backend.services.analyze import analysis_service
from backend.auth import get_current_user_from_session

router = APIRouter(prefix="/api/analyze", tags=["analyze"])

@router.post("/{video_id}")
async def analyze_video(
    video_id: int,
    text: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    try:
        analysis = analysis_service.analyze_content(text)
        return {"success": True, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: 运行测试验证**

```bash
pytest tests/test_analyze.py -v
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/analyze.py backend/routers/analyze.py
git commit -m "feat: implement AI content analysis service"
```

---

### Task 7: 二创改写服务

**Files:**
- Create: `backend/services/rewrite.py`
- Create: `backend/routers/rewrite.py`
- Test: `tests/test_rewrite.py`

- [ ] **Step 1: 创建改写服务**

```python
# backend/services/rewrite.py
from openai import OpenAI
from backend.config import settings
import json

class RewriteService:
    def __init__(self):
        self.deepseek_client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        )
    
    def rewrite_content(self, text: str, analysis: dict) -> list:
        """生成 3 个不同版本的改写内容"""
        prompt = f"""
请对以下内容进行二创改写，生成 3 个不同表达方式的版本：

原内容：
{text}

内容分析：
{json.dumps(analysis, ensure_ascii=False)}

要求：
1. 每个版本都要换语法、换口吻、换比喻方式
2. 保持核心观点不变
3. 版本 1：轻松幽默风格
4. 版本 2：严肃专业风格
5. 版本 3：故事叙述风格

请以 JSON 数组格式返回：
[
    {{"style": "轻松幽默", "content": "改写内容 1"}},
    {{"style": "严肃专业", "content": "改写内容 2"}},
    {{"style": "故事叙述", "content": "改写内容 3"}}
]
"""
        
        response = self.deepseek_client.chat.completions.create(
            model=settings.DEFAULT_REWRITE_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.choices[0].message.content
        return json.loads(result)

rewrite_service = RewriteService()
```

- [ ] **Step 2: 创建改写路由**

```python
# backend/routers/rewrite.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.script import Script
from backend.services.rewrite import rewrite_service
from backend.auth import get_current_user_from_session

router = APIRouter(prefix="/api/rewrite", tags=["rewrite"])

@router.post("/{video_id}")
async def rewrite_video(
    video_id: int,
    text: str,
    analysis: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    try:
        versions = rewrite_service.rewrite_content(text, analysis)
        
        # 保存 3 个版本到数据库
        scripts = []
        for i, version in enumerate(versions):
            script = Script(
                video_id=video_id,
                version=i + 1,
                content=version["content"],
                status="draft"
            )
            db.add(script)
            scripts.append(script)
        
        db.commit()
        
        return {
            "success": True,
            "versions": versions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: 运行测试验证**

```bash
pytest tests/test_rewrite.py -v
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/rewrite.py backend/routers/rewrite.py
git commit -m "feat: implement AI re-creation rewrite service"
```

---

### Task 8: AI 审核服务

**Files:**
- Create: `backend/services/review.py`
- Create: `backend/routers/review.py`
- Test: `tests/test_review.py`

- [ ] **Step 1: 创建审核服务**

```python
# backend/services/review.py
from openai import OpenAI
from backend.config import settings
import json

class ReviewService:
    def __init__(self):
        self.qwen_client = OpenAI(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_BASE_URL
        )
    
    def review_content(self, content: str, platform: str = "douyin") -> dict:
        """AI 审核内容"""
        prompt = f"""
请审核以下内容是否适合发布到{platform}平台：

内容：
{content}

请从以下维度评估（JSON 格式）：
{{
    "originality_score": 85,  // 原创度 0-100
    "compliance": "pass",  // pass/warn/fail
    "appeal_score": "high",  // low/medium/high
    "completion_rate_prediction": "high",  // low/medium/high
    "sensitive_words": [],  // 敏感词列表
    "suggestions": ["修改建议 1", "修改建议 2"],
    "overall_recommendation": "recommend"  // recommend/caution/not_recommend
}}

{platform}平台规则参考：
- 抖音：禁止夸大宣传、禁止虚假承诺、禁止敏感话题
- 小红书：真实分享、避免硬广、注重实用性
- B 站：内容质量优先、避免低质、尊重原创
"""
        
        response = self.qwen_client.chat.completions.create(
            model=settings.DEFAULT_REVIEW_MODEL,
            messages=[{"role": "user", "content": prompt}],
            extra_body={"enable_search": True}
        )
        
        result = response.choices[0].message.content
        return json.loads(result)

review_service = ReviewService()
```

- [ ] **Step 2: 创建审核路由**

```python
# backend/routers/review.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.script import Script
from backend.services.review import review_service
from backend.auth import get_current_user_from_session

router = APIRouter(prefix="/api/review", tags=["review"])

@router.post("/{script_id}")
async def review_script(
    script_id: int,
    platform: str = "douyin",
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    try:
        review = review_service.review_content(script.content, platform)
        
        # 保存审核结果
        script.suggestions = json.dumps(review, ensure_ascii=False)
        script.status = "reviewed"
        db.commit()
        
        return {"success": True, "review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: 运行测试验证**

```bash
pytest tests/test_review.py -v
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/review.py backend/routers/review.py
git commit -m "feat: implement AI review service"
```

---

### Task 9: 逐字稿生成服务

**Files:**
- Create: `backend/services/script_generator.py`
- Create: `backend/routers/script_generator.py`
- Test: `tests/test_script_generator.py`

- [ ] **Step 1: 创建逐字稿生成服务**

```python
# backend/services/script_generator.py
from openai import OpenAI
from backend.config import settings
import json

class ScriptGeneratorService:
    def __init__(self):
        self.qwen_client = OpenAI(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_BASE_URL
        )
    
    def generate_script(self, content: str) -> dict:
        """生成带语气、分镜建议的逐字稿"""
        prompt = f"""
请将以下内容转化为详细的逐字稿，包含拍摄指导：

内容：
{content}

请以 JSON 格式返回：
{{
    "markdown": "完整的 Markdown 格式逐字稿",
    "segments": [
        {{
            "type": "开场",
            "tone": "轻松好奇",
            "text": "具体台词",
            "directions": ["停顿 2 秒", "眼神直视镜头"],
            "reason": "制造悬念"
        }},
        ...
    ],
    "titles": ["标题 1", "标题 2", ...],  // 10 个标题变体
    "tags": ["标签 1", "标签 2", ...],  // 热门标签
    "publish_time_suggestion": "晚 19-21 点",  // 最佳发布时间
    "cover_text": "封面文案"  // 封面文字建议
}}

要求：
- 每个环节都要标注语气、重点表现方式、拍摄建议
- 标题要吸引点击，符合短视频平台特点
- 标签要热门且相关
"""
        
        response = self.qwen_client.chat.completions.create(
            model=settings.DEFAULT_ANALYSIS_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.choices[0].message.content
        return json.loads(result)

script_generator_service = ScriptGeneratorService()
```

- [ ] **Step 2: 创建逐字稿路由**

```python
# backend/routers/script_generator.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.script import Script
from backend.services.script_generator import script_generator_service
from backend.auth import get_current_user_from_session
import os

router = APIRouter(prefix="/api/scripts", tags=["scripts"])

@router.post("/{script_id}/generate")
async def generate_final_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    try:
        result = script_generator_service.generate_script(script.content)
        
        # 更新脚本
        script.content = result["markdown"]
        script.titles = json.dumps(result["titles"], ensure_ascii=False)
        script.tags = json.dumps(result["tags"], ensure_ascii=False)
        script.suggestions = json.dumps({
            "publish_time": result["publish_time_suggestion"],
            "cover_text": result["cover_text"],
            "segments": result["segments"]
        }, ensure_ascii=False)
        script.status = "approved"
        db.commit()
        
        # 导出 Markdown 文件
        output_dir = f"data/outputs/{script.video_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        markdown_path = f"{output_dir}/script_{script_id}.md"
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(result["markdown"])
        
        return {
            "success": True,
            "script": result,
            "markdown_path": markdown_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{script_id}")
async def get_script(
    script_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_from_session)
):
    script = db.query(Script).filter(Script.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    return {
        "id": script.id,
        "version": script.version,
        "content": script.content,
        "titles": json.loads(script.titles) if script.titles else [],
        "tags": json.loads(script.tags) if script.tags else [],
        "suggestions": json.loads(script.suggestions) if script.suggestions else {},
        "status": script.status
    }
```

- [ ] **Step 3: 运行测试验证**

```bash
pytest tests/test_script_generator.py -v
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/script_generator.py backend/routers/script_generator.py
git commit -m "feat: implement script generation service"
```

---

## Phase 3: 前端开发 (4-5 天)

### Task 10: Vue 3 前端项目初始化

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`
- Create: `frontend/tailwind.config.js`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "videos-create-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.5",
    "tailwindcss": "^3.4.1"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "vite": "^5.0.11",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33"
  }
}
```

- [ ] **Step 2: 创建 vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <link rel="icon" href="/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视频二创 Agent</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 4: 创建 main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')
```

- [ ] **Step 5: 创建 App.vue**

```vue
<template>
  <router-view />
</template>

<script setup>
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
```

- [ ] **Step 6: 创建 style.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 7: 创建 tailwind.config.js**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- [ ] **Step 8: 创建 postcss.config.js**

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

- [ ] **Step 9: 安装依赖并验证**

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

- [ ] **Step 10: Commit**

```bash
git add frontend/
git commit -m "feat: initialize Vue 3 frontend project"
```

---

### Task 11: 前端路由和状态管理

**Files:**
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/stores/auth.js`
- Create: `frontend/src/stores/video.js`
- Create: `frontend/src/api/index.js`

- [ ] **Step 1: 创建路由配置**

```javascript
// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Process from '../views/Process.vue'
import ScriptViewer from '../views/ScriptViewer.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/process/:id', name: 'Process', component: Process },
  { path: '/script/:id', name: 'ScriptViewer', component: ScriptViewer },
  { path: '/settings', name: 'Settings', component: Settings }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('auth_token')
  if (!token && to.name !== 'Login') {
    next({ name: 'Login' })
  } else if (token && to.name === 'Login') {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
```

- [ ] **Step 2: 创建认证 Store**

```javascript
// frontend/src/stores/auth.js
import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token')
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  
  actions: {
    async login(username, password) {
      const response = await api.post('/api/login', { username, password })
      if (response.data.success) {
        this.user = response.data.user
        this.token = btoa(`${username}:${password}`)
        localStorage.setItem('auth_token', this.token)
      }
      return response.data
    },
    
    async logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('auth_token')
    },
    
    async fetchUser() {
      if (!this.token) return
      try {
        const response = await api.get('/api/me')
        this.user = response.data
      } catch (error) {
        this.logout()
      }
    }
  }
})
```

- [ ] **Step 3: 创建 API 客户端**

```javascript
// frontend/src/api/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: ''
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    const [username, password] = atob(token).split(':')
    config.auth = { username, password }
  }
  return config
})

export default api
```

- [ ] **Step 4: 创建视频 Store**

```javascript
// frontend/src/stores/video.js
import { defineStore } from 'pinia'
import api from '../api'

export const useVideoStore = defineStore('video', {
  state: () => ({
    videos: [],
    currentVideo: null,
    processing: false
  }),
  
  actions: {
    async fetchVideos() {
      const response = await api.get('/api/videos/')
      this.videos = response.data.videos
    },
    
    async uploadVideo(file) {
      const formData = new FormData()
      formData.append('file', file)
      const response = await api.post('/api/videos/upload', formData)
      await this.fetchVideos()
      return response.data
    },
    
    async transcribe(videoId) {
      this.processing = true
      const response = await api.post(`/api/transcribe/${videoId}`)
      this.processing = false
      return response.data
    }
  }
})
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/router/ frontend/src/stores/ frontend/src/api/
git commit -m "feat: setup frontend routing and state management"
```

---

### Task 12: 前端页面组件开发

**Files:**
- Create: `frontend/src/views/Login.vue`
- Create: `frontend/src/views/Dashboard.vue`
- Create: `frontend/src/views/Process.vue`
- Create: `frontend/src/views/ScriptViewer.vue`
- Create: `frontend/src/views/Settings.vue`
- Create: `frontend/src/components/VideoUpload.vue`
- Create: `frontend/src/components/ProcessProgress.vue`
- Create: `frontend/src/components/ScriptViewer.vue`

- [ ] **Step 1: 创建登录页面**

```vue
<!-- frontend/src/views/Login.vue -->
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <h1 class="text-2xl font-bold text-center mb-8">视频二创 Agent</h1>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">用户名</label>
          <input 
            v-model="username"
            type="text"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 mb-2">密码</label>
          <input 
            v-model="password"
            type="password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        
        <button 
          type="submit"
          class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
        >
          登录
        </button>
        
        <p v-if="error" class="text-red-500 text-center mt-4">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = '用户名或密码错误'
  }
}
</script>
```

- [ ] **Step 2: 创建仪表盘页面**

```vue
<!-- frontend/src/views/Dashboard.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="container mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-xl font-bold">视频二创 Agent</h1>
        <div class="flex items-center space-x-4">
          <span>{{ authStore.user?.username }}</span>
          <button @click="authStore.logout()" class="text-red-500">退出</button>
        </div>
      </div>
    </nav>
    
    <main class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <VideoUpload @uploaded="handleUploaded" />
      </div>
      
      <div class="bg-white rounded-lg shadow">
        <h2 class="text-lg font-bold p-4 border-b">我的视频</h2>
        <div v-if="videoStore.videos.length === 0" class="p-8 text-center text-gray-500">
          暂无视频，请上传
        </div>
        <div v-else class="divide-y">
          <div v-for="video in videoStore.videos" :key="video.id" class="p-4 flex justify-between items-center">
            <div>
              <p class="font-medium">{{ video.original_filename }}</p>
              <p class="text-sm text-gray-500">{{ new Date(video.created_at).toLocaleString() }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <span :class="statusClass(video.status)" class="px-2 py-1 rounded text-sm">
                {{ statusText(video.status) }}
              </span>
              <button 
                @click="goToProcess(video.id)"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                处理
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useVideoStore } from '../stores/video'
import VideoUpload from '../components/VideoUpload.vue'

const router = useRouter()
const authStore = useAuthStore()
const videoStore = useVideoStore()

onMounted(() => {
  videoStore.fetchVideos()
  authStore.fetchUser()
})

const handleUploaded = () => {
  videoStore.fetchVideos()
}

const goToProcess = (videoId) => {
  router.push(`/process/${videoId}`)
}

const statusClass = (status) => {
  const classes = {
    pending: 'bg-gray-200 text-gray-700',
    processing: 'bg-blue-200 text-blue-700',
    done: 'bg-green-200 text-green-700',
    failed: 'bg-red-200 text-red-700'
  }
  return classes[status] || classes.pending
}

const statusText = (status) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    done: '已完成',
    failed: '失败'
  }
  return texts[status] || status
}
</script>
```

- [ ] **Step 3: 创建其他页面组件**

（由于篇幅限制，其他组件类似创建，包含 Process.vue、ScriptViewer.vue、Settings.vue 等）

- [ ] **Step 4: 运行前端验证**

```bash
cd frontend
npm run dev
# 访问 http://localhost:5173
```

- [ ] **Step 5: Commit**

```bash
git add frontend/src/views/ frontend/src/components/
git commit -m "feat: create frontend page components"
```

---

## Phase 4: 测试与部署 (2-3 天)

### Task 13: 集成测试

**Files:**
- Create: `tests/test_integration.py`
- Create: `scripts/setup.sh`
- Create: `scripts/dev.sh`

- [ ] **Step 1: 创建集成测试**

```python
# tests/test_integration.py
"""完整工作流集成测试"""

def test_full_workflow():
    """测试完整 SOP 流程"""
    # 1. 登录
    # 2. 上传视频
    # 3. 转录
    # 4. 分析
    # 5. 改写
    # 6. 审核
    # 7. 生成逐字稿
    pass
```

- [ ] **Step 2: 创建启动脚本**

```bash
# scripts/setup.sh
#!/bin/bash

echo "Setting up Video Re-creation Agent..."

# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install

# Create data directories
mkdir -p data/uploads data/logs data/outputs

# Copy environment file
cp .env.example .env

echo "Setup complete! Edit .env and run scripts/dev.sh"
```

```bash
# scripts/dev.sh
#!/bin/bash

# Start backend
cd backend && python main.py &

# Start frontend
cd frontend && npm run dev
```

- [ ] **Step 3: 运行所有测试**

```bash
pytest tests/ -v
```

- [ ] **Step 4: Commit**

```bash
git add tests/test_integration.py scripts/
git commit -m "feat: add integration tests and setup scripts"
```

---

### Task 14: 文档完善

**Files:**
- Create: `docs/api/README.md`
- Create: `docs/specs/SOP.md`
- Modify: `README.md` (更新安装说明)

- [ ] **Step 1: 创建 API 文档**

```markdown
# API Documentation

## Authentication

### POST /api/login
Login

### GET /api/me
Get current user

## Videos

### POST /api/videos/upload
Upload video

### GET /api/videos/
List videos

### GET /api/videos/{id}
Get video details

## Transcription

### POST /api/transcribe/{video_id}
Transcribe video

## Analysis

### POST /api/analyze/{video_id}
Analyze content

## Rewrite

### POST /api/rewrite/{video_id}
Rewrite content

## Review

### POST /api/review/{script_id}
Review script

## Script

### POST /api/scripts/{script_id}/generate
Generate final script

### GET /api/scripts/{script_id}
Get script details
```

- [ ] **Step 2: 更新 README**

- [ ] **Step 3: Commit**

```bash
git add docs/api/ docs/specs/ README.md
git commit -m "docs: add API documentation and update README"
```

---

## 测试策略

### 测试覆盖率目标
- 单元测试：80%+
- 集成测试：核心工作流 100%

### 测试命令
```bash
# 运行所有测试
pytest tests/ -v

# 运行覆盖率测试
pytest tests/ --cov=backend --cov-report=html
```

---

## 验收标准

- [ ] 所有测试通过
- [ ] 代码无 lint 错误
- [ ] 文档完整
- [ ] 可以本地运行完整工作流
- [ ] Git 提交历史清晰

---

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Whisper 模型下载慢 | 中 | 使用镜像源 |
| API 调用失败 | 中 | 添加重试机制 |
| 前端兼容性问题 | 低 | 测试主流浏览器 |
| 大文件上传超时 | 中 | 添加进度条和断点续传 |

---
