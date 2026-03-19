# 贡献指南 (Contributing Guide)

欢迎参与本项目开发！

## 开发流程

### 1. Fork 项目

```bash
# GitHub 上点击 Fork 按钮
```

### 2. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/videos_create.git
cd videos_create
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 开发并测试

```bash
# 安装依赖
pip install -r backend/requirements.txt

# 运行测试
pytest tests/

# 代码格式化
black backend/
```

### 5. 提交代码

```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. 推送并创建 PR

```bash
git push origin feature/your-feature-name
# GitHub 上创建 Pull Request
```

## 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

## 测试要求

- 新功能必须包含测试
- 所有测试必须通过
- 覆盖率不低于 80%

## 代码风格

- 后端：PEP 8
- 前端：ESLint + Prettier

## 问题反馈

遇到问题请提交 Issue，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息

感谢你的贡献！
