# 视频二创 Agent

🎬 AI 驱动的视频二创工作流

## 快速开始

### 1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env` 并填入你的 API key：

```bash
cp .env.example .env
```

编辑 `.env`:
```
QWEN_API_KEY=sk-your-qwen-key
DEEPSEEK_API_KEY=sk-your-deepseek-key
```

### 3. 添加视频

将视频文件放入 `data/videos/` 文件夹：

```bash
mkdir -p data/videos
cp your_video.mp4 data/videos/
```

### 4. 启动服务

```bash
python backend/main.py
```

访问 http://127.0.0.1:8000/

### 5. 处理视频

**方式 1: 使用前端界面**
1. 打开 http://127.0.0.1:8000/
2. 点击视频旁边的"处理"按钮
3. 等待处理完成
4. 查看生成的脚本

**方式 2: 使用命令行**
```bash
python backend/pipeline.py your_video.mp4
```

### 输出文件

处理完成后，文件保存在 `data/outputs/`:

```
data/outputs/
├── your_video_script.md       # Markdown 逐字稿
└── your_video_result.json     # 完整结果
```

## 完整 SOP 流程

1. 🎤 **语音转录** - Whisper medium 模型 (95% 准确率)
2. 🔍 **内容分析** - Qwen 提取重点和标签
3. ✍️ **二创改写** - DeepSeek 生成 3 个不同风格版本
4. 📊 **AI 审核** - Qwen 多维度评分（原创度/合规性/吸引力）
5. 📝 **逐字稿生成** - Markdown 格式，包含语气和分镜建议
6. 🏷️ **标题标签** - 10 个标题变体 + 热门标签

## 技术栈

- **前端**: HTML + Alpine.js + TailwindCSS
- **后端**: Python FastAPI
- **转录**: Whisper medium (本地)
- **AI**: Qwen3.5 + DeepSeek V3.2

## 常见问题

### Q: 需要 GPU 吗？
A: 不需要。Whisper medium 在 CPU 上运行良好（约 5-10 分钟/视频）。

### Q: API 费用多少？
A: 单个视频（10 分钟）约 ¥0.5-1 元（Qwen + DeepSeek）。

### Q: 支持哪些视频格式？
A: MP4, MOV, MKV, AVI。

## License

MIT License
