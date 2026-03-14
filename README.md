# MovieExplainer - 雅思字幕学习材料生成器

> 在几分钟内，从任何视频字幕生成完整的雅思学习材料

自动从视频字幕提取结构化英语学习材料的 Claude Code 工作流系统。

---

## 为什么要用 MovieExplainer？

### 解决的问题

| 痛点 | MovieExplainer 解决方案 |
|------|------------------------|
| **看完视频记不住** | 自动提炼关键观点，形成结构化笔记 |
| **手动整理耗时数小时** | 一条命令自动提取，几分钟完成 |
| **缺少练习材料** | 生成 CSV 工作表 + Anki 卡片，直接可用 |
| **发音学习被忽略** | 词汇卡片包含国际音标，支持发音学习 |
| **处理视频麻烦** | 无需下载视频，只需字幕/文本，轻量高效 |

### 独特之处

**🎯 任何视频都能成为学习材料**

- 对任何感兴趣或有感悟的视频材料进行深度复习
- 只需提供字幕文件 (SRT/VTT/TXT) 或转录文本
- 无需下载或处理视频文件

**⚡ 轻量高效**

- 直接从文本中提取，无需处理视频流
- 生成结构化学习材料：关键观点、词汇、表达、搭配
- 与 Anki 实时联动，一键生成可导入的卡片包

**📚 多场景适用**

- TED 演讲 → 提炼观点和表达
- 雅思听力材料 → 生成词汇和练习
- 新闻纪录片 → 积累话题词汇
- 任何你感兴趣的视频 → 个人定制学习材料

### 谁会受益？

| 用户 | 收益 |
|------|------|
| **雅思备考者** | 快速积累高分表达和词汇，针对听说读写四科 |
| **英语学习者** | 从真实材料中学习地道用法，提升输入转输出能力 |
| **教师/导师** | 快速生成练习材料，用于课堂教学或作业布置 |

### 核心功能

- 🎯 自动提取 Key Points、Verb Phrases、Vocabulary、IELTS Expressions
- ✅ 智能审核与迭代优化，确保内容质量
- 📦 多种输出格式：Markdown、CSV、Anki (.apkg)
- 🔊 词汇卡片包含国际音标，支持发音学习

---

## 前置条件

MovieExplainer 依赖以下环境，不同组件有不同的依赖：

### 必需环境

| 环境 | 用途 | 影响的模块 |
|------|------|-----------|
| **Claude Code** 或 Agent CLI | AI 工作流引擎，执行字幕解析和内容提取 | 核心工作流 (`/extract-subtitle`) |
| **LLM API 访问** | Claude / GPT-4 等，用于智能内容提取和审核 | 所有 AI 驱动的功能 |
| **VSCode** (可选) | 使用 Claude Code 扩展的推荐编辑器 | 开发体验 |

### 可选环境

| 环境 | 用途 | 影响的模块 |
|------|------|-----------|
| **Python 3.8+** | 生成 .apkg 文件 | `csv-to-anki.py` 脚本 |
| **pip** | 安装 Python 依赖 | `genanki` 库 |

### 环境依赖关系图

```
字幕文件 (.srt)
    │
    ▼
┌─────────────────────────────────────┐
│  Claude Code / Agent CLI           │  ← 必需
│  + LLM API (Claude/GPT-4)          │  ← 必需
├─────────────────────────────────────┤
│  执行 /extract-subtitle 工作流      │
│  ↓                                  │
│  生成:                              │
│  • key-points.md                    │
│  • vocabulary.md                    │
│  • verb-phrases.md                  │
│  • ielts-expressions.md             │
│  • worksheet.csv                    │
│  • anki-deck.csv                   │
└─────────────────────────────────────┘
                │
                ▼ (可选)
┌─────────────────────────────────────┐
│  Python 3.8+ + genanki             │  ← 可选
├─────────────────────────────────────┤
│  执行 csv-to-anki.py                │
│  ↓                                  │
│  生成: anki-deck.apkg              │
└─────────────────────────────────────┘
```

### 安装指南

#### 1. 安装 Claude Code

```bash
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code

# 或在 VSCode 中安装扩展
# 搜索 "Claude Code" 并安装
```

#### 2. 配置 LLM API

Claude Code 支持多种 LLM 提供商，选择其一：

- **Anthropic Claude** (推荐) - [获取 API Key](https://console.anthropic.com/)
- **OpenAI GPT-4** - [获取 API Key](https://platform.openai.com/)

配置方式：在 Claude Code 设置中添加 API Key。

#### 3. 安装 Python 环境（可选）

如需生成 .apkg 文件：

```bash
# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 安装依赖
pip install genanki
```

---

## 快速开始

### 1. 在 VSCode 中打开项目

确保已安装 [Claude Code](https://claude.com/claude-code) 扩展。

### 2. 使用工作流

```bash
# 处理字幕文件
/extract-subtitle examples/sample-lesson.srt

# 指定目标分数
/extract-subtitle examples/sample-lesson.srt --target-band 7.5

# 跳过审核环节（更快）
/extract-subtitle examples/sample-lesson.srt --no-review
```

### 3. 查看输出

学习材料生成在字幕文件同目录下的 `learning-materials/` 文件夹：

```
learning-materials/
├── key-points.md          # 关键观点
├── vocabulary.md          # 词汇表
├── verb-phrases.md        # 动词短语
├── ielts-expressions.md   # 雅思高分表达
├── worksheet.csv          # 练习工作表（Excel 可打开）
├── anki-deck.csv          # Anki 导入文件（制表符分隔）
└── anki-deck.apkg         # Anki 卡组包（需手动生成）
```

---

## 生成 Anki .apkg 文件

.apkg 格式是 Anki 的官方打包格式，双击即可直接导入，无需额外配置。

### 自动生成（推荐）

工作流会自动生成 `anki-deck.csv`，如需 .apkg 格式，可在工作流中自动调用转换脚本。

### 手动生成

#### 步骤 1: 安装 Python 依赖

**强烈建议使用虚拟环境**（避免污染系统 Python 环境）：

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install genanki
```

#### 步骤 2: 生成 .apkg 文件

```bash
# 基本用法
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv

# 指定输出路径
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv learning-materials/my-deck.apkg
```

#### 步骤 3: 导入 Anki

双击生成的 `.apkg` 文件，Anki 会自动导入。卡组名称为 **MovieExplainer**。

---

## 输出格式说明

| 格式 | 用途 | 打开方式 |
| :--- | :--- | :--- |
| `key-points.md` | 关键观点参考 | 文本编辑器 |
| `vocabulary.md` | 词汇学习 | 文本编辑器 |
| `verb-phrases.md` | 动词短语学习 | 文本编辑器 |
| `ielts-expressions.md` | 高分表达学习 | 文本编辑器 |
| `worksheet.csv` | 练习工作表 | **双击（Excel）** |
| `anki-deck.csv` | Anki 制表符格式 | Anki → 文件 → 导入 |
| `anki-deck.apkg` | Anki 卡组包 | **双击导入** |

---

## 项目结构

```
.claude/
├── skills/           # Claude Code 技能
├── agents/           # SubAgent 定义
├── hooks/            # 会话钩子
├── scripts/          # 辅助脚本（如 csv-to-anki.py）
└── memory/           # 项目改进记录

examples/             # 示例字幕文件
projects/             # 你的工作区
```

## 工作流组件

1. **字幕解析器** - 解析 SRT/VTT/TXT 格式
2. **内容提取器** - 提取学习内容
3. **内容审核器** - 质量检查
4. **迭代优化器** - 多轮改进

---

## 关于作者

MovieExplainer 是作者本人雅思备考过程中开发的学习工具。作者目前正在使用 Anki 卡片进行词汇和表达的积累与复习。

如果你也在准备雅思考试或希望提升英语能力，欢迎联系作者一起学习交流：

> **Email**: [duanbiao2000@gmail.com](mailto:duanbiao2000@gmail.com)

## 许可证

MIT License
