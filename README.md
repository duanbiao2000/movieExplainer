# MovieExplainer - IELTS Subtitle Learning Material Generator

---

**English** | **[简体中文](README.zh-CN.md)** | **[日本語](README.ja.md)**

---

> Generate complete IELTS learning materials from any video subtitle in minutes

An automated Claude Code workflow system that extracts structured English learning materials from video subtitles.

## Why MovieExplainer?

### Problems Solved

| Pain Point | MovieExplainer Solution |
|------------|------------------------|
| **Forget what you watched** | Automatically extract key points into structured notes |
| **Manual organizing takes hours** | One command auto-extraction in minutes |
| **Lack practice materials** | Generate CSV worksheets + Anki cards, ready to use |
| **Pronunciation overlooked** | Vocabulary cards include IPA for pronunciation learning |
| **Video processing hassle** | No need to download videos, just subtitles/text, lightweight |

### What Makes It Unique

**🎯 Any Video Can Be Learning Material**

- Deep review of any interesting or insightful video content
- Just provide subtitle file (SRT/VTT/TXT) or transcript
- No need to download or process video files

**⚡ Lightweight & Efficient**

- Extract directly from text, no video stream processing
- Generate structured materials: key points, vocabulary, expressions, collocations
- Real-time Anki integration, one-click importable card packs

**📚 Multi-Scenario Use**

- TED Talks → Extract points and expressions
- IELTS listening materials → Generate vocabulary and exercises
- News documentaries → Accumulate topic vocabulary
- Any video you're interested in → Personalized learning materials

### Who Benefits?

| User | Benefits |
|------|----------|
| **IELTS Test Takers** | Quickly accumulate high-scoring expressions and vocabulary for all four skills |
| **English Learners** | Learn authentic usage from real materials, improve input-to-output ability |
| **Teachers/Mentors** | Quickly generate practice materials for classroom teaching or assignments |

### Core Features

- 🎯 Auto-extract Key Points, Verb Phrases, Vocabulary, IELTS Expressions
- ✅ Smart review & iterative optimization for content quality
- 📦 Multiple output formats: Markdown, CSV, Anki (.apkg)
- 🔊 Vocabulary cards include International Phonetic Alphabet for pronunciation

## Prerequisites

MovieExplainer depends on the following environments, different components have different requirements:

### Required Environments

| Environment | Purpose | Affected Modules |
|-------------|---------|-------------------|
| **Claude Code** or Agent CLI | AI workflow engine for subtitle parsing and content extraction | Core workflow (`/extract-subtitle`) |
| **LLM API Access** | Claude / GPT-4 etc. for intelligent content extraction and review | All AI-driven features |
| **VSCode** (optional) | Recommended editor for Claude Code extension | Development experience |

### Optional Environments

| Environment | Purpose | Affected Modules |
|-------------|---------|-------------------|
| **Python 3.8+** | Generate .apkg files | `csv-to-anki.py` script |
| **pip** | Install Python dependencies | `genanki` library |

### Environment Dependency Diagram

```
Subtitle File (.srt)
    │
    ▼
┌─────────────────────────────────────┐
│  Claude Code / Agent CLI           │  ← Required
│  + LLM API (Claude/GPT-4)          │  ← Required
├─────────────────────────────────────┤
│  Execute /extract-subtitle workflow │
│  ↓                                  │
│  Generate:                          │
│  • key-points.md                    │
│  • vocabulary.md                    │
│  • verb-phrases.md                  │
│  • ielts-expressions.md             │
│  • worksheet.csv                    │
│  • anki-deck.csv                   │
└─────────────────────────────────────┘
                │
                ▼ (optional)
┌─────────────────────────────────────┐
│  Python 3.8+ + genanki             │  ← Optional
├─────────────────────────────────────┤
│  Execute csv-to-anki.py             │
│  ↓                                  │
│  Generate: anki-deck.apkg          │
└─────────────────────────────────────┘
```

### Installation Guide

#### 1. Install Claude Code

```bash
# Install using npm
npm install -g @anthropic-ai/claude-code

# Or install extension in VSCode
# Search "Claude Code" and install
```

#### 2. Configure LLM API

Claude Code supports multiple LLM providers, choose one:

- **Anthropic Claude** (recommended) - [Get API Key](https://console.anthropic.com/)
- **OpenAI GPT-4** - [Get API Key](https://platform.openai.com/)

Configuration: Add API Key in Claude Code settings.

#### 3. Install Python Environment (Optional)

If you need to generate .apkg files:

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install genanki
```

### Don't Want to Set Up the Environment?

**No problem!** You can directly use the learning materials generated in the `projects/` directory.

The author maintains **1-3 updates per week** with fresh content from various videos (TED talks, documentaries, news, IELTS materials, etc.).

- Browse the `projects/` folder to find ready-to-use learning materials
- Download Anki `.apkg` files for direct import
- Use Markdown files for reference and study

**Got specific needs?** Open an [issue](../../issues) to request:
- Specific video/topic coverage
- Custom vocabulary focus areas
- IELTS band-specific materials
- Feature suggestions

---

## Quick Start

### 1. Open Project in VSCode

Make sure [Claude Code](https://claude.com/claude-code) extension is installed.

### 2. Use the Workflow

```bash
# Process subtitle file
/extract-subtitle examples/sample-lesson.srt

# Specify target band score
/extract-subtitle examples/sample-lesson.srt --target-band 7.5

# Skip review step (faster)
/extract-subtitle examples/sample-lesson.srt --no-review
```

### 3. View Output

Learning materials are generated in the `learning-materials/` folder next to the subtitle file:

```
learning-materials/
├── key-points.md          # Key points
├── vocabulary.md          # Vocabulary list
├── verb-phrases.md        # Verb phrases
├── ielts-expressions.md   # IELTS high-scoring expressions
├── worksheet.csv          # Practice worksheet (opens with Excel)
├── anki-deck.csv          # Anki import file (tab-separated)
└── anki-deck.apkg         # Anki deck package (manually generated)
```

## Language Support

MovieExplainer supports multiple output languages:

- **English (default)** - Learning materials in English
- **Chinese (中文)** - 学习材料使用中文

**Usage:**

```bash
# English output (default)
/extract-subtitle video.srt

# Chinese output
/extract-subtitle video.srt --language zh
```

## Generate Anki .apkg Files

The .apkg format is Anki's official package format that can be imported with a double-click, no additional configuration needed.

### Auto Generation (Recommended)

The workflow automatically generates `anki-deck.csv`. If you need .apkg format, the conversion script can be called automatically in the workflow.

### Manual Generation

#### Step 1: Install Python Dependencies

**Strongly recommend using a virtual environment** (to avoid polluting system Python):

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install genanki
```

#### Step 2: Generate .apkg File

```bash
# Basic usage
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv

# Specify output path
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv learning-materials/my-deck.apkg
```

#### Step 3: Import into Anki

Double-click the generated `.apkg` file, Anki will automatically import it. Deck name is **MovieExplainer**.

## Output Format Guide

| Format | Purpose | How to Open |
| :--- | :--- | :--- |
| `key-points.md` | Key points reference | Text editor |
| `vocabulary.md` | Vocabulary learning | Text editor |
| `verb-phrases.md` | Verb phrase learning | Text editor |
| `ielts-expressions.md` | High-scoring expression learning | Text editor |
| `worksheet.csv` | Practice worksheet | **Double-click (Excel)** |
| `anki-deck.csv` | Anki tab-separated format | Anki → File → Import |
| `anki-deck.apkg` | Anki deck package | **Double-click to import** |

## Project Structure

```
.claude/
├── skills/           # Claude Code skills
├── agents/           # SubAgent definitions
├── hooks/            # Session hooks
├── scripts/          # Utility scripts (e.g. csv-to-anki.py)
└── memory/           # Project improvement records

examples/             # Sample subtitle files
projects/             # Your workspace
```

## Workflow Components

1. **Subtitle Parser** - Parse SRT/VTT/TXT formats
2. **Content Extractor** - Extract learning content
3. **Content Reviewer** - Quality check
4. **Iteration Optimizer** - Multi-round improvement

## About the Author

MovieExplainer is a learning tool developed during the author's IELTS preparation journey. The author is currently using Anki cards to accumulate and review vocabulary and expressions.

If you are also preparing for the IELTS exam or want to improve your English skills, feel free to reach out:

> **Email**: [duanbiao2000@gmail.com](mailto:duanbiao2000@gmail.com)
> **Twitter**: [@duanbiao](https://twitter.com/duanbiao)

---

## 💡 Let's Build Something Amazing Together!

**MovieExplainer is OPEN for collaboration!**

I'm an ENTP-type learner who thrives on innovation, big ideas, and turning chaos into structure. If you're passionate about:

- 🚀 **Expanding language support** - More languages? More exam types? Let's do it!
- 🤖 **Enhancing AI capabilities** - Better extraction, smarter categorization? Bring it on!
- 🎨 **Improving user experience** - Better workflows, cooler outputs? I'm all ears!
- 📚 **Curating content** - Have amazing video recommendations? Fire away!
- 🔧 **Hacking the code** - Want to refactor, optimize, or add features? You're welcome!

**Why collaborate?**
- Learn & grow together in a supportive environment
- Build tools that actually help people (including ourselves!)
- Experiment with cutting-edge AI & automation
- Have fun while solving real problems

**Don't hesitate** — Whether you're a seasoned developer, a curious learner, or just someone with a crazy idea. The best projects come from unexpected collaborations.

Let's connect and create something meaningful together! 🎯

---

## License

MIT License
