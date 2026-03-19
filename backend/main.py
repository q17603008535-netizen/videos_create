from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from config import settings
import uvicorn
from routers.auth import router as auth_router

app = FastAPI(title="Video Re-creation Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")


@app.get("/")
async def root():
    return FileResponse("../frontend/index.html")


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/api/videos")
async def list_videos_api():
    from services.video_reader import list_videos
    return list_videos()


@app.post("/api/process")
async def process_video_api(request: dict):
    from pipeline import process_video
    result = process_video(request["video"])
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
