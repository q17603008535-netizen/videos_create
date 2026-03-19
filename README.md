# 视频二创 Agent (Video Re-creation Agent)

[English](README_EN.md) | 中文

🎬 AI 驱动的视频二创工作流，一键生成短视频稿子

## 功能特性

- 🎬 **视频语音转录** - 本地 Whisper 模型，95% 准确率
- 📝 **AI 内容分析** - 提取重点 + 热门话题建议
- ✍️ **二创改写** - 生成 3 个不同表达方式的版本
- 🎯 **平台适配优化** - 抖音/小红书/B 站规则适配
- 📊 **AI 审核评分** - 多维度评估 + 修改建议
- 📋 **逐字稿生成** - 包含语气、分镜、重点表现方式
- 🏷️ **标题/标签建议** - 10 个标题变体 + 热门标签推荐

## 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+ (前端)
- 8GB+ RAM (Whisper 本地运行)

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/q17603008535-netizen/videos_create.git
cd videos_create

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API key

# 3. 安装后端依赖
pip install -r backend/requirements.txt

# 4. 安装前端依赖
cd frontend
npm install

# 5. 启动服务
python backend/main.py
# 访问 http://localhost:8000
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TailwindCSS |
| 后端 | Python FastAPI |
| 数据库 | SQLite |
| 语音转录 | Whisper (medium) |
| AI 模型 | Qwen3.5 + DeepSeek V3.2 |

## 完整 SOP 流程

```
视频上传 → 语音转录 → 内容分析 → 二创改写 (3 版本) → 
平台适配 → AI 审核 → 人工审核 → 逐字稿 → 标题/标签 → 输出
```

## 项目结构

```
videos_create/
├── backend/           # 后端代码
├── frontend/          # 前端代码
├── docs/              # 文档
├── data/              # 数据目录 (运行时创建)
├── scripts/           # 辅助脚本
└── tests/             # 测试
```

## 开发计划

- [x] v0.1 MVP - 本地单人使用
- [ ] v0.2 - 多用户 + Cloudflare 部署
- [ ] v0.3 - 产品化 (付费功能)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!
