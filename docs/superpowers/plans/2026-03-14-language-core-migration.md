# Language Core Migration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate MovieExplainer from Chinese-dominant to English-default architecture while maintaining full Chinese i18n support.

**Architecture:** Document-driven architecture with centralized `labels.json` for language configuration. The `param-middleware` Agent validates language parameters and builds configuration objects passed to downstream Agents.

**Tech Stack:** JSON configuration, Markdown documents, Claude Code Agents

---

## File Structure Overview

### New Files
- `.claude/config/labels.json` - Centralized EN/ZH labels, prompts, templates
- `docs/developer/philosophy-analysis.en.md` - English version of philosophy analysis

### Modified Files
- `.claude/skills/extract-subtitle/SKILL.md` - Add language parameter
- `.claude/agents/param-middleware/agent.md` - Language validation and config building
- `.claude/agents/content-extractor/agent.md` - English description
- `.claude/agents/content-reviewer/agent.md` - English description
- `.claude/agents/iteration-optimizer/agent.md` - English description
- `.claude/agents/polish-refactoror/agent.md` - English description
- `.claude/agents/subtitle-parser/agent.md` - English description
- `.claude/agents/ielts-coach/agent.md` - English description
- `CLAUDE.md` - English project overview
- `README.md` - Update language documentation

### Moved Files
- `documents/philosophy-analysis.md` → `docs/developer/philosophy-analysis.zh.md`
- `documents/README.md` → `docs/developer/README.md`

---

## Chunk 1: Phase 1 - Create labels.json

### Task 1: Create labels.json with complete EN/ZH structure

**Files:**
- Create: `.claude/config/labels.json`

- [ ] **Step 1: Create labels.json with complete structure**

Create `.claude/config/labels.json` with the following content:

```json
{
  "en": {
    "vocabulary": {
      "label_ipa": "IPA",
      "label_meaning": "Meaning",
      "label_example": "Example",
      "label_synonyms": "Synonyms",
      "label_context": "Context"
    },
    "prompts": {
      "extract_intro": "Extract vocabulary from the following text. Focus on words useful for IELTS preparation.",
      "review_intro": "Review the following content for quality, accuracy, and completeness.",
      "optimize_intro": "Optimize the following content for clarity and educational value."
    },
    "output_formats": {
      "anki_header": "#separator:tab\n#html:true\n#tags:ielts",
      "markdown_header": "# Vocabulary List\n\n"
    },
    "categories": {
      "academic": "Academic",
      "colloquial": "Colloquial",
      "idiomatic": "Idiomatic",
      "phrasal": "Phrasal Verb"
    },
    "proficiency_levels": {
      "c2": "Mastery",
      "c1": "Advanced",
      "b2": "Upper Intermediate",
      "b1": "Intermediate"
    }
  },
  "zh": {
    "vocabulary": {
      "label_ipa": "国际音标",
      "label_meaning": "释义",
      "label_example": "例句",
      "label_synonyms": "同义词",
      "label_context": "语境"
    },
    "prompts": {
      "extract_intro": "从以下文本中提取词汇。重点关注对雅思备考有用的词汇。",
      "review_intro": "审查以下内容的质量、准确性和完整性。",
      "optimize_intro": "优化以下内容的清晰度和教育价值。"
    },
    "output_formats": {
      "anki_header": "#separator:tab\n#html:true\n#tags:雅思",
      "markdown_header": "# 词汇表\n\n"
    },
    "categories": {
      "academic": "学术",
      "colloquial": "口语",
      "idiomatic": "习语",
      "phrasal": "短语动词"
    },
    "proficiency_levels": {
      "c2": "精通",
      "c1": "高级",
      "b2": "中高级",
      "b1": "中级"
    }
  }
}
```

- [ ] **Step 2: Create config directory**

```bash
mkdir -p .claude/config/
```

- [ ] **Step 3: Validate JSON syntax**

```bash
# Cross-platform JSON validation
python -m json.tool .claude/config/labels.json
echo "✓ Valid JSON"
```
Expected: JSON output without syntax errors

- [ ] **Step 4: Verify structure completeness**

Check that all English keys have corresponding Chinese keys:

```bash
# Verify EN and ZH have matching structure
python -c "
import json
import sys

with open('.claude/config/labels.json') as f:
    data = json.load(f)

def get_all_keys(obj, keys=None):
    if keys is None:
        keys = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(k)
            get_all_keys(v, keys)
    return keys

en_keys = get_all_keys(data['en'])
zh_keys = get_all_keys(data['zh'])

if en_keys == zh_keys:
    print('✓ EN and ZH have matching structure')
    print(f'  Total keys: {len(en_keys)}')
else:
    print('✗ Structure mismatch:')
    print(f'  EN-only keys: {en_keys - zh_keys}')
    print(f'  ZH-only keys: {zh_keys - en_keys}')
    sys.exit(1)
"
```
Expected: "✓ EN and ZH have matching structure"

- [ ] **Step 5: Test loading labels.json**

```bash
python -c "
import json
with open('.claude/config/labels.json') as f:
    labels = json.load(f)
    print(f'✓ Loaded {len(labels)} languages')
    print(f'  EN vocabulary labels: {list(labels[\"en\"][\"vocabulary\"].keys())}')
    print(f'  ZH vocabulary labels: {list(labels[\"zh\"][\"vocabulary\"].keys())}')
"
```
Expected: Shows loaded languages and vocabulary labels

- [ ] **Step 6: Commit**

```bash
git add .claude/config/labels.json
git commit -m "feat(i18n): create labels.json with EN/ZH translations

- Add centralized language configuration
- Includes vocabulary labels, prompts, output formats
- Supports academic, colloquial, idiomatic, phrasal categories
- Proficiency levels from B1 to C2

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 2: Phase 2 - Add Language Parameter Support

### Task 2: Update extract-subtitle skill with language parameter

**Files:**
- Modify: `.claude/skills/extract-subtitle/SKILL.md`

- [ ] **Step 1: Read current skill definition**

Read: `.claude/skills/extract-subtitle/SKILL.md`
Note the current parameter structure and location where new parameters should be added.

- [ ] **Step 2: Add language parameter to skill**

Add the following parameter definition to the SKILL.md frontmatter or parameters section:

```yaml
# If using YAML frontmatter:
args:
  - name: language
    description: "Output language for learning materials"
    shorthand: "l"
    default: "en"
    values: ["en", "zh"]
```

Or add to documentation section:

```markdown
## Parameters

### --language, -l <lang>

Output language for generated learning materials.

**Values:**
- `en` - English (default)
- `zh` - Chinese

**Example:**
\`\`\`bash
/extract-subtitle video.srt -l zh
\`\`\`
```

- [ ] **Step 3: Update skill examples to show language parameter**

Add examples showing both default (English) and explicit Chinese:

```markdown
## Examples

### Generate English materials (default)
/extract-subtitle video.srt

### Generate Chinese materials
/extract-subtitle video.srt -l zh
```

- [ ] **Step 4: Verify skill syntax**

Run: Check that the skill file has valid frontmatter (if applicable)
Expected: No syntax errors

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/extract-subtitle/SKILL.md
git commit -m "feat(skill): add --language parameter to extract-subtitle

- Add --language/-l parameter with default value 'en'
- Supported values: en, zh
- Update examples to show language switching

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 3: Update param-middleware agent for language handling

**Files:**
- Modify: `.claude/agents/param-middleware/agent.md`

- [ ] **Step 1: Read current param-middleware agent**

Read: `.claude/agents/param-middleware/agent.md`
Understand current parameter processing logic.

- [ ] **Step 2: Add language validation logic**

Add to the agent's task description:

```markdown
## Language Parameter Handling

When processing the `--language` parameter:

1. **Validate the language code**
   - Accept: `en`, `zh`
   - Default: `en`
   - Reject: any other value with clear error message

2. **Load labels from config**
   - Read `.claude/config/labels.json`
   - Extract labels for the specified language
   - Build configuration object

3. **Pass to downstream agents**
   - Include `language` in config object
   - Include resolved labels in `output_labels` field
```

- [ ] **Step 3: Add example config object**

```markdown
## Output Configuration

The agent builds a configuration object that is passed to all downstream agents:

\`\`\`json
{
  "language": "en",
  "output_labels": {
    "ipa": "IPA",
    "meaning": "Meaning",
    "example": "Example"
  }
}
\`\`\`

For Chinese (`language: "zh"`):

\`\`\`json
{
  "language": "zh",
  "output_labels": {
    "ipa": "国际音标",
    "meaning": "释义",
    "example": "例句"
  }
}
\`\`\`
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/param-middleware/agent.md
git commit -m "feat(agent): param-middleware language handling

- Add language parameter validation (en, zh)
- Load labels from .claude/config/labels.json
- Build configuration object for downstream agents
- Include example config objects for EN and ZH

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 3: Phase 3 - Update Agent Configurations (Part 1)

### Task 4: Update subtitle-parser agent

**Files:**
- Modify: `.claude/agents/subtitle-parser/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/subtitle-parser/agent.md`

- [ ] **Step 2: Update description to English**

Replace Chinese description with English. Key points to translate:
- Agent purpose and role
- Input/output specifications
- Output format description

Example transformation:
```markdown
# Subtitle Parser Agent

## Purpose
Parses subtitle files (SRT, VTT, TXT) and extracts structured dialogue data.

## Input
- Subtitle file path
- File format (auto-detected or specified)

## Output
Structured JSON containing:
- Dialogue entries with timestamps
- Language detection
- Bilingual subtitle identification
```

- [ ] **Step 3: Add language context note**

```markdown
## Language Context

This agent receives language context from param-middleware but does not
generate language-specific output. Language handling is done by downstream agents.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/subtitle-parser/agent.md
git commit -m "refactor(agent): subtitle-parser English description

- Translate agent description to English
- Add language context note
- Maintain technical accuracy

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 5: Update content-extractor agent

**Files:**
- Modify: `.claude/agents/content-extractor/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/content-extractor/agent.md`

- [ ] **Step 2: Update description to English**

Translate the main description. Focus on:
- Core purpose (vocabulary and expressions extraction)
- Extraction categories (academic, colloquial, etc.)
- Output format

- [ ] **Step 3: Add language-specific output section**

```markdown
## Language-Specific Output

The agent uses labels from the input context:

\`\`\`markdown
## {{labels.vocabulary.label_ipa}}
[International Phonetic Alphabet transcription]

## {{labels.vocabulary.label_meaning}}
[Definition in target language]

## {{labels.vocabulary.label_example}}
[Example sentence from subtitle]
\`\`\`

The actual labels (IPA/Meaning/Example vs 国际音标/释义/例句)
are provided in the \`output_labels\` field of the input context.
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/content-extractor/agent.md
git commit -m "refactor(agent): content-extractor English description

- Translate agent description to English
- Add language-specific output section
- Reference output_labels from input context

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 6: Update content-reviewer agent

**Files:**
- Modify: `.claude/agents/content-reviewer/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/content-reviewer/agent.md`

- [ ] **Step 2: Update description to English**

Translate quality review criteria and process description.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/content-reviewer/agent.md
git commit -m "refactor(agent): content-reviewer English description

- Translate quality review criteria to English
- Maintain review standards

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 4: Phase 3 - Update Agent Configurations (Part 2)

### Task 7: Update iteration-optimizer agent

**Files:**
- Modify: `.claude/agents/iteration-optimizer/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/iteration-optimizer/agent.md`

- [ ] **Step 2: Update description to English**

This agent contains philosophical concepts. Translate while preserving technical terms:

- Keep terms like "dialectical optimization" in English
- Translate explanatory text

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/iteration-optimizer/agent.md
git commit -m "refactor(agent): iteration-optimizer English description

- Translate agent description to English
- Preserve philosophical/technical terms
- Maintain dialectical optimization framework

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 8: Update polish-refactoror agent

**Files:**
- Modify: `.claude/agents/polish-refactoror/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/polish-refactoror/agent.md`

- [ ] **Step 2: Update description to English**

Translate polishing and refactoring guidelines.

- [ ] **Step 3: Add language note for style transfer**

```markdown
## Language and Style

This agent operates in the target language specified in the input context.
Style improvements should match:
- English: Academic/formal register for IELTS preparation
- Chinese: Clear, educational Chinese appropriate for language learners
```

- [ ] **Step 4: Commit**

```bash
git add .claude/agents/polish-refactoror/agent.md
git commit -m "refactor(agent): polish-refactoror English description

- Translate agent description to English
- Add language and style guidelines
- Maintain educational focus

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 9: Update ielts-coach agent

**Files:**
- Modify: `.claude/agents/ielts-coach/agent.md`

- [ ] **Step 1: Read current agent**

Read: `.claude/agents/ielts-coach/agent.md`

- [ ] **Step 2: Update description to English**

Translate coaching questions and interaction patterns.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/ielts-coach/agent.md
git commit -m "refactor(agent): ielts-coach English description

- Translate coaching questions to English
- Maintain interactive coaching approach

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 5: Phase 4 - Update Project Configuration

### Task 10: Update CLAUDE.md to English

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read current CLAUDE.md**

Read: `CLAUDE.md`

- [ ] **Step 2: Update project overview to English**

Replace the Chinese project overview with English:

```markdown
# MovieExplainer Project Configuration

## Project Overview

Automated IELTS learning material generation workflow from subtitle files.

## Available Commands

### /extract-subtitle

Process subtitle files to generate learning materials.

**Usage:**
- `/extract-subtitle <file-path>` - Process specified subtitle (English output by default)
- `/extract-subtitle <file-path> --language zh` - Generate Chinese output
- `/extract-subtitle <file-path> -l en` - Explicit English output
- `/extract-subtitle <file-path> --target-band 7.5` - Specify target score
- `/extract-subtitle <file-path> --formats md,anki` - Select output formats

## Workflow Components

- **Subtitle Parser** (`.claude/agents/subtitle-parser/`) - Parses SRT/VTT/TXT formats
- **Content Extractor** (`.claude/agents/content-extractor/`) - Extracts learning content
- **Content Reviewer** (`.claude/agents/content-reviewer/`) - Quality checking
- **Iteration Optimizer** (`.claude/agents/iteration-optimizer/`) - Iterative improvement
- **IELTS Coach** (`.claude/agents/ielts-coach/`) - Interactive personalized coaching
- **Polish Refactoror** (`.claude/agents/polish-refactoror/`) - Styling + metacognitive enhancement

## Output Location

Learning materials are saved in `learning-materials/` folder next to the subtitle file by default.

## Configuration

Project-level configuration is in `.claude/config/learning-materials.json` and `.claude/config/labels.json`.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md to English

- Translate project overview to English
- Update command examples to show English default
- Add language parameter examples
- Reference new labels.json configuration

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 11: Update README.md language documentation

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Read current README.md**

Read: `README.md`

- [ ] **Step 2: Update default language description**

Find and update the language/i18n section to reflect English as default:

```markdown
## Language Support

MovieExplainer supports multiple output languages:

- **English (default)** - Learning materials in English
- **Chinese (中文)** - 学习材料使用中文

**Usage:**

\`\`\`bash
# English output (default)
/extract-subtitle video.srt

# Chinese output
/extract-subtitle video.srt --language zh
\`\`\`
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: update README language documentation

- Document English as default output language
- Add Chinese language option examples
- Update language switching syntax

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 6: Phase 5 - Documentation Restructuring

### Task 12: Create docs/developer directory structure

**Files:**
- Create: `docs/developer/` directory

- [ ] **Step 1: Create developer docs directory**

```bash
mkdir -p docs/developer
```

- [ ] **Step 2: Move existing documents**

```bash
# Move philosophy analysis with language suffix
mv documents/philosophy-analysis.md docs/developer/philosophy-analysis.zh.md

# Move README
mv documents/README.md docs/developer/README.md
```

- [ ] **Step 3: Verify moves**

```bash
ls -la docs/developer/
# Expected: philosophy-analysis.zh.md, README.md
```

- [ ] **Step 4: Update docs/developer/README.md**

Add links to both language versions:

```markdown
# Developer Documentation

## Philosophy & Design

- [English](philosophy-analysis.en.md) - Design philosophy and architectural principles
- [中文](philosophy-analysis.zh.md) - 设计哲学与架构原则
```

- [ ] **Step 5: Commit**

```bash
git add docs/developer/
git commit -m "docs: consolidate documents to docs/developer

- Move documents/philosophy-analysis.md → docs/developer/philosophy-analysis.zh.md
- Move documents/README.md → docs/developer/README.md
- Add language links to developer README
- Resolves confusion between docs/ and documents/ directories

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 13: Create English philosophy analysis

**Files:**
- Create: `docs/developer/philosophy-analysis.en.md`

- [ ] **Step 1: Read Chinese version**

Read: `docs/developer/philosophy-analysis.zh.md`

- [ ] **Step 2: Create English translation**

Create `docs/developer/philosophy-analysis.en.md` with the following structure:

```markdown
# Philosophy Analysis

## Overview

This document explains the philosophical principles guiding the MovieExplainer architecture.

## Core Principles

### 1. Dialectical Optimization

The system employs a dialectical approach to content optimization, embracing the tension between opposing forces:

- **Thesis (正)**: Initial extraction from source material
- **Antithesis (反)**: Critical review and quality assessment
- **Synthesis (合)**: Refined output through iterative improvement

### 2. Metacognitive Enhancement

Learning materials include metacognitive prompts that encourage learners to reflect on:

- Why certain vocabulary is useful for IELTS
- How expressions are used in context
- What makes a particular example valuable

### 3. Educational Scaffolding

Content is structured to provide scaffolding for learners:

1. **Recognition** - Vocabulary identification
2. **Understanding** - Meaning and context
3. **Application** - Example usage
4. **Analysis** - Why it matters for IELTS

## Architectural Decisions

### Document-Driven Architecture

All Agent behaviors are defined through Markdown documents rather than code. This enables:

- Rapid iteration without deployment
- Clear visibility into agent reasoning
- Easy A/B testing of prompts

### Language-First Design

The system is designed to be language-agnostic at the core, with all language-specific content externalized to `labels.json`. This enables:

- Easy addition of new languages
- Consistent behavior across languages
- Centralized translation management

## Quality Standards

Content must meet these standards before being presented to learners:

1. **Accuracy** - Correct transcription and translation
2. **Relevance** - Appropriate for IELTS preparation
3. **Clarity** - Easy to understand
4. **Completeness** - All necessary context provided

---

*This document is a translation of [philosophy-analysis.zh.md](philosophy-analysis.zh.md). For the original Chinese version, please refer to that file.*
```

- [ ] **Step 3: Commit**

```bash
git add docs/developer/philosophy-analysis.en.md
git commit -m "docs: add English philosophy analysis

- Create English version of philosophy analysis document
- Translate core principles: dialectical optimization, metacognitive enhancement
- Preserve Chinese philosophical terms with English explanations
- Add reference to original Chinese version

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

### Task 14: Archive old internationalization roadmap

**Files:**
- Move: `.claude/future/internationalization.md` → `.claude/archive/internationalization.md`

- [ ] **Step 1: Create archive directory**

```bash
mkdir -p .claude/archive
```

- [ ] **Step 2: Archive the roadmap**

```bash
mv .claude/future/internationalization.md .claude/archive/internationalization.md
```

- [ ] **Step 3: Add archive note**

Add to top of archived file:

```markdown
> **ARCHIVED**: This roadmap has been implemented. See the implementation plan at
> `docs/superpowers/plans/2026-03-14-language-core-migration.md` and the design spec at
> `docs/superpowers/specs/2026-03-14-language-core-migration-design.md`.

---

# Internationalization Roadmap (Original)
```

- [ ] **Step 4: Commit**

```bash
git add .claude/archive/
git rm .claude/future/internationalization.md
git commit -m "docs: archive implemented i18n roadmap

- Move internationalization.md to archive/
- This roadmap has been implemented in language core migration
- Add reference to implementation plan and design spec

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Chunk 7: Verification

### Task 15: End-to-end verification

**Files:**
- Test: Manual verification

- [ ] **Step 1: Verify labels.json exists and is valid**

```bash
test -f .claude/config/labels.json && python -m json.tool .claude/config/labels.json > /dev/null && echo "✓ labels.json exists and is valid"
```

- [ ] **Step 2: Verify all agent files have been updated**

```bash
# Check for remaining Chinese in critical agent sections
for agent in .claude/agents/*/agent.md; do
  echo "Checking: $agent"
  # This is a manual check - review each file
done
```

- [ ] **Step 3: Verify directory structure**

```bash
echo "=== Directory Structure ==="
ls -la docs/developer/
echo ""
echo "=== Archive ==="
ls -la .claude/archive/
```

Expected output:
```
=== Directory Structure ===
philosophy-analysis.zh.md
philosophy-analysis.en.md
README.md

=== Archive ===
internationalization.md
```

- [ ] **Step 4: Create test summary**

Create `docs/verify-language-migration.md`:

```markdown
# Language Migration Verification Checklist

## Phase 1: labels.json
- [ ] File exists at `.claude/config/labels.json`
- [ ] JSON is valid
- [ ] Contains both `en` and `zh` keys
- [ ] All categories present: vocabulary, prompts, output_formats, categories, proficiency_levels

## Phase 2: Language Parameter
- [ ] `extract-subtitle` skill has `--language` / `-l` parameter
- [ ] Default value is `en`
- [ ] `param-middleware` agent handles language validation

## Phase 3: Agent Configurations
- [ ] All 7 agent descriptions in English
- [ ] Language context properly referenced
- [ ] No Chinese-only sections remaining

## Phase 4: Project Config
- [ ] `CLAUDE.md` in English
- [ ] `README.md` documents language switching
- [ ] Default language documented as English

## Phase 5: Documentation
- [ ] `documents/` moved to `docs/developer/`
- [ ] English philosophy analysis exists
- [ ] Developer README has language links
- [ ] Old roadmap archived

## Functional Tests
- [ ] `/extract-subtitle test.srt` generates English output
- [ ] `/extract-subtitle test.srt -l zh` generates Chinese output
- [ ] Chinese workflow (`-l zh`) produces expected results
```

- [ ] **Step 5: Final commit**

```bash
git add docs/verify-language-migration.md
git commit -m "docs: add language migration verification checklist

- Add comprehensive verification checklist
- Covers all 5 phases of migration
- Includes functional test cases

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

This plan implements the language core migration in 7 chunks:

1. **Chunk 1**: Create `labels.json` with complete EN/ZH structure
2. **Chunk 2**: Add language parameter support to skill and param-middleware
3. **Chunk 3**: Update subtitle-parser, content-extractor, content-reviewer agents
4. **Chunk 4**: Update iteration-optimizer, polish-refactoror, ielts-coach agents
5. **Chunk 5**: Update CLAUDE.md and README.md to English
6. **Chunk 6**: Restructure documentation (documents → docs/developer)
7. **Chunk 7**: Verification and testing

**Total estimated time**: 5-8 hours

**Key principles**:
- DRY - Language content centralized in labels.json
- YAGNI - Only implement EN and ZH (no premature generalization)
- TDD - Each change is verified before committing
- Frequent commits - Each task commits independently
