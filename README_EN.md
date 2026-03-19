# Video Re-creation Agent

English | [中文](README.md)

🎬 AI-driven video re-creation workflow, generate short video scripts in one click

## Features

- 🎬 **Video Transcription** - Local Whisper model, 95% accuracy
- 📝 **AI Content Analysis** - Extract key points + trending topics
- ✍️ **Re-creation Rewrite** - Generate 3 different expression versions
- 🎯 **Platform Optimization** - Douyin/Xiaohongshu/Bilibili adaptation
- 📊 **AI Review Score** - Multi-dimensional evaluation + suggestions
- 📋 **Script Generation** - With tone, storyboard, key performance
- 🏷️ **Title/Tags** - 10 title variants + trending tags

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (frontend)
- 8GB+ RAM (Whisper local running)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/q17603008535-netizen/videos_create.git
cd videos_create

# 2. Configure environment
cp .env.example .env
# Edit .env and fill in your API keys

# 3. Install backend dependencies
pip install -r backend/requirements.txt

# 4. Install frontend dependencies
cd frontend
npm install

# 5. Start server
python backend/main.py
# Visit http://localhost:8000
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vue 3 + Vite + TailwindCSS |
| Backend | Python FastAPI |
| Database | SQLite |
| Transcription | Whisper (medium) |
| AI Models | Qwen3.5 + DeepSeek V3.2 |

## Complete SOP Flow

```
Video Upload → Transcription → Content Analysis → Rewrite (3 versions) → 
Platform Adaptation → AI Review → Manual Review → Script → Titles/Tags → Output
```

## Project Structure

```
videos_create/
├── backend/           # Backend code
├── frontend/          # Frontend code
├── docs/              # Documentation
├── data/              # Data directory (created at runtime)
├── scripts/           # Helper scripts
└── tests/             # Tests
```

## Roadmap

- [x] v0.1 MVP - Local single user
- [ ] v0.2 - Multi-user + Cloudflare deployment
- [ ] v0.3 - Productization (paid features)

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!
