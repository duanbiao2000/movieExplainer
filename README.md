# MovieExplainer - 雅思字幕学习材料生成器

自动从视频字幕提取结构化英语学习材料的 Claude Code 工作流系统。

## 功能特点

- 🎯 自动提取 Key Points、Verb Phrases、Vocabulary、IELTS Expressions
- ✅ 智能审核与迭代优化，确保内容质量
- 📦 多种输出格式：Markdown、CSV、Anki (.apkg)

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

## 许可证

MIT License
