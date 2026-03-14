# Language Core Migration Design: Chinese-Dominant to English-Default

**Date**: 2026-03-14
**Status**: Design Approved
**Author**: Claude (with human collaboration)

---

## Context

MovieExplainer is currently a Chinese-dominant project with emerging internationalization (i18n) support. The README has been internationalized (EN/ZH/JA), and there is an existing i18n roadmap in `.claude/future/internationalization.md`. However, all Agent configurations, internal documentation, and default outputs remain in Chinese.

**Problem Statement**: The Chinese-dominant architecture creates friction for English-speaking users and limits the project's global accessibility. While Chinese content should remain fully supported, English should become the default/primary language.

**Intended Outcome**: English becomes the default language throughout the project while maintaining complete Chinese i18n support. Users can seamlessly switch between languages via parameters.

---

## Design Overview

```
Existing State                      Target State
┌─────────────────┐                 ┌─────────────────┐
│  Chinese-First  │      ──────►    │  English-First  │
│  Architecture   │                 │  Architecture   │
├─────────────────┤                 ├─────────────────┤
│ Agent configs:  │                 │ Agent configs:  │
│   Chinese       │                 │   English        │
│ Output default: │                 │ Output default: │
│   Chinese       │                 │   English        │
│ Language param: │                 │ Language param:  │
│   None          │                 │   --lang / -l    │
│ labels.json:    │                 │ labels.json:     │
│   Does not exist│                 │   Created        │
└─────────────────┘                 └─────────────────┘
        ↓                                    ↓
   ┌──────────────────────────────────────────┐
   │         Migration Path (Existing Plan)    │
   ├──────────────────────────────────────────┤
   │  Phase 1: Create labels.json (EN/ZH)      │
   │  Phase 2: Add --language param to skill   │
   │  Phase 3: Update Agent configs to EN      │
   │  Phase 4: Update CLAUDE.md project config │
   │  Phase 5: Create EN versions of docs      │
   └──────────────────────────────────────────┘
```

### Core Changes

1. **Create `.claude/config/labels.json`** - Centralized storage for all Chinese and English labels, prompts, and output templates
2. **Modify `extract-subtitle` skill** - Add `--language` / `-l` parameter with default value `en`
3. **Update all Agent configurations** - Use English descriptions by default, reference `labels.json` for Chinese content
4. **Update `CLAUDE.md`** - Change project overview to English
5. **Create English versions of developer docs** - Parallel documentation (EN/ZH)

> **Note**: This specification changes the default language from `zh` to `en`, diverging from the existing `.claude/future/internationalization.md` roadmap which specified Chinese as default. This is intentional to better serve the global user base and align with international best practices.

---

## File Changes

### New Files

| Path | Description | Priority |
|------|-------------|----------|
| `.claude/config/labels.json` | Centralized EN/ZH labels, prompts, templates | P0 - Core |
| `documents/philosophy-analysis.en.md` | English version of philosophy analysis | P2 - Dev Docs |

### Modified Files

| Path | Changes | Priority |
|------|---------|----------|
| `.claude/skills/extract-subtitle/SKILL.md` | Add `--language` / `-l` parameter | P0 |
| `.claude/agents/content-extractor/agent.md` | Description → EN, add language param handling | P1 |
| `.claude/agents/content-reviewer/agent.md` | Description → EN, add language param handling | P1 |
| `.claude/agents/iteration-optimizer/agent.md` | Description → EN, add language param handling | P1 |
| `.claude/agents/polish-refactoror/agent.md` | Description → EN, add language param handling | P1 |
| `.claude/agents/subtitle-parser/agent.md` | Description → EN | P1 |
| `.claude/agents/ielts-coach/agent.md` | Description → EN | P1 |
| `.claude/agents/param-middleware/agent.md` | Description → EN | P1 |
| `CLAUDE.md` | Project overview → EN | P1 |
| `README.md` | Update default language documentation | P2 |

### Archived Files

| Path | Action |
|------|--------|
| `.claude/future/internationalization.md` | Archive to `.claude/archive/` (plan implemented) |

---

## Template System Architecture

### Template Syntax

The template system uses a simple string substitution pattern. Agents reference localized content using the following syntax:

```
{{labels.<lang>.<category>.<key>}}
```

### Resolution Mechanism

**Important**: In this document-driven architecture, template substitution is **not** an automated runtime process. Instead:

1. **param-middleware Agent** receives the `--language` parameter
2. It **constructs a configuration object** containing the resolved language strings from `labels.json`
3. This configuration is **passed to downstream Agents** via their input context
4. Agents use the resolved strings directly in their prompts (no template engine needed)

### Example: Before and After

**Agent Configuration (Before)**:

```markdown
## Output Format

输出词汇表时，使用以下格式：
- **IPA**: [国际音标]
- **释义**: [中文释义]
```

**Agent Configuration (After)**:

```markdown
## Output Format

When outputting vocabulary, use the following format:
- **IPA**: [International Phonetic Alphabet]
- **Meaning**: [Definition]

The actual labels to use will be provided in the `output_labels` field of your input context.
```

**Configuration Object Passed to Agent**:
```json
{
  "language": "en",
  "output_labels": {
    "ipa": "IPA",
    "meaning": "Meaning",
    "example": "Example"
  }
}
```

### labels.json Complete Structure

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
      "extract_intro": "Extract vocabulary from the following text...",
      "review_intro": "Review the following content for quality..."
    },
    "output_formats": {
      "anki_header": "#separator:tab\n#html:true\n#tags:ielts",
      "markdown_header": "# Vocabulary List\n\n"
    },
    "categories": {
      "academic": "Academic",
      "colloquial": "Colloquial",
      "idiomatic": "Idiomatic"
    },
    "proficiency_levels": {
      "c2": "Mastery",
      "c1": "Advanced",
      "b2": "Upper Intermediate"
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
      "extract_intro": "从以下文本中提取词汇...",
      "review_intro": "审查以下内容的质量..."
    },
    "output_formats": {
      "anki_header": "#separator:tab\n#html:true\n#tags:雅思",
      "markdown_header": "# 词汇表\n\n"
    },
    "categories": {
      "academic": "学术",
      "colloquial": "口语",
      "idiomatic": "习语"
    },
    "proficiency_levels": {
      "c2": "精通",
      "c1": "高级",
      "b2": "中高级"
    }
  }
}
```

### Language Parameter Flow

```
User Command: /extract-subtitle video.srt -l zh
       │
       ▼
┌──────────────────────────┐
│  extract-subtitle SKILL  │
│  - Captures -l zh        │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│  param-middleware Agent  │
│  - Validates language    │
│  - Reads labels.json     │
│  - Builds config object  │
└──────────────────────────┘
       │
       ▼ passes config object to all downstream agents
┌──────────────────────────┐
│  subtitle-parser Agent   │
│  Input: {language: "zh", │
│          labels: {...}}  │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│  content-extractor Agent │
│  Input: {language: "zh", │
│          labels: {...},  │
│          parsed_subs}    │
└──────────────────────────┘
       │
       └───► (continues through workflow with language context)
```

---

## Implementation Plan

### Phase 1: Create Language Labels Configuration (P0)

**Objective**: Establish i18n infrastructure

**Tasks**:
1. Create `.claude/config/labels.json`
   - Define structure: `labels.[lang].[category].[key]`
   - Populate English translations for all existing Chinese labels
   - Include: vocabulary categories, example templates, output format descriptions

**Verification**:
- JSON format validation passes
- EN/ZH content pairs are complete

**Estimated**: 1-2 hours (translation-heavy)

---

### Phase 2: Add Language Parameter Support (P0)

**Objective**: Enable language selection via CLI

**Tasks**:
1. Modify `.claude/skills/extract-subtitle/SKILL.md`
   - Add `--language` / `-l` parameter definition
   - Set default value to `en`
   - Supported values: `en`, `zh`

2. Update `.claude/agents/param-middleware/agent.md`
   - Add language parameter validation logic
   - Pass language parameter to downstream Agents

**Verification**:
```bash
/extract-subtitle test.srt           # → generates English materials
/extract-subtitle test.srt -l zh     # → generates Chinese materials
```

**Estimated**: 30 minutes

---

### Phase 3: Update Agent Configurations to English Default (P1)

**Objective**: All Agents use English as default description and behavior

**Tasks**:
Update Agents in priority order:
1. `subtitle-parser` - No language dependency, update first
2. `param-middleware` - Parameter handling layer
3. `content-extractor` - Core extraction logic
4. `content-reviewer` - Quality checking
5. `iteration-optimizer` - Iterative improvement
6. `polish-refactoror` - Polishing and refactoring
7. `ielts-coach` - Interactive coaching

Each Agent update:
- Change description to English
- Add `language` parameter reference
- Use `{{labels.language.xxx}}` for localized content

**Verification**:
- All Agent config files have valid syntax
- English descriptions are clear and accurate

**Estimated**: 2-3 hours

---

### Phase 4: Update Project Configuration (P1)

**Objective**: Project-level documentation reflects new default language

**Tasks**:
1. Update `CLAUDE.md`
   - Project overview → English
   - Command examples → English
   - Retain Chinese comments as explanatory notes

2. Update `README.md`
   - Adjust default language description
   - Update command examples

**Verification**:
- New users can successfully use the project following English documentation

**Estimated**: 30 minutes

---

### Phase 5: Create English Developer Documentation (P2)

**Objective**: Developer documentation in parallel languages

**Tasks**:
1. Create `documents/philosophy-analysis.en.md`
   - Translate core philosophical concepts
   - Preserve Chinese terms (e.g., "Yin-Yang dialectic") with English explanations

2. Update `documents/README.md`
   - Add EN/ZH documentation links

**Verification**:
- English-speaking developers can understand project design philosophy

**Estimated**: 1-2 hours

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Chinese users suddenly face English interface** | User experience disruption | High | 1) Pre-announcement 2) Preserve `-l zh` quick switch 3) Clear documentation |
| **Poor translation quality causes Agent behavior issues** | Output quality degradation | Medium | 1) Professional translation 2) Per-Agent validation 3) Keep Chinese as fallback |
| **labels.json structure poorly designed** | Technical debt | Medium | 1) Reference i18n best practices 2) Flexible nested structure 3) Extensibility预留 |
| **Existing Chinese learning materials users affected** | Compatibility issues | Low | Language parameter only affects new materials, existing materials unchanged |

---

## Testing Strategy

### Unit Tests

**labels.json Validation**:

- JSON schema validation
- Verify all English keys have corresponding Chinese keys
- Verify no orphaned (missing translation) keys

**Parameter Validation**:

- Test valid language codes: `en`, `zh`
- Test invalid language codes are rejected
- Test default behavior when no language specified

### Integration Tests

**Parameter Passing Flow**:

- Verify `param-middleware` passes language to all downstream Agents
- Verify each Agent receives and uses the correct labels from context

**Language Output Verification**:

```bash
# Test English output (default)
/extract-subtitle test.srt
# Verify: vocabulary.md contains English labels

# Test Chinese output
/extract-subtitle test.srt -l zh
# Verify: vocabulary.md contains Chinese labels

# Test all 7 language-dependent Agents
# For each agent, verify output language matches parameter
```

### Regression Tests

**Backward Compatibility**:

```bash
# Existing Chinese workflow should produce identical results
/extract-subtitle test.srt -l zh
# Compare with pre-migration baseline output
```

**Edge Cases**:

- Missing or malformed `labels.json` → Should fail gracefully with clear error
- Partial translations (missing keys) → Should warn and use fallback language
- Empty subtitle file → Should handle regardless of language setting

### Test Data

**Sample Test Files**:

- `test/fixtures/sample-bilingual.srt` - Bilingual subtitle for testing
- `test/fixtures/baselines/zh-output/` - Pre-migration Chinese outputs for comparison
- `test/fixtures/baselines/en-output/` - Expected English outputs

---

## Acceptance Criteria

### Functional Acceptance

**Phase 1 Complete**:
- [ ] `labels.json` exists with valid format
- [ ] Contains all necessary Chinese and English labels

**Phase 2 Complete**:
- [ ] `/extract-subtitle test.srt` generates English materials
- [ ] `/extract-subtitle test.srt -l zh` generates Chinese materials
- [ ] Default behavior (no parameter) is English

**Phase 3 Complete**:
- [ ] All Agent configurations use English descriptions
- [ ] English descriptions accurately convey original meaning

**Phase 4 Complete**:
- [ ] `CLAUDE.md` uses English
- [ ] New users can successfully run following English documentation

**Phase 5 Complete**:
- [ ] `philosophy-analysis.en.md` exists
- [ ] English-speaking developers understand design philosophy

### Regression Testing

- [ ] Existing Chinese users using `-l zh` get the same experience as before
- [ ] New users get English output without specifying language
- [ ] All Agents work correctly after language switching

---

## Time Estimates

| Phase | Estimate | Notes |
|-------|----------|-------|
| Phase 1: labels.json | 1-2 hours | Translation-heavy |
| Phase 2: Language parameter | 30 min | Configuration change |
| Phase 3: Agent config updates | 2-3 hours | 7 Agent configs |
| Phase 4: Project config | 30 min | Documentation update |
| Phase 5: Developer docs | 1-2 hours | Philosophy concept translation |
| **Total** | **5-8 hours** | Can be split across sessions |

---

## Architecture Insights

**Key Design Decision**: This solution uses the existing `.claude/future/internationalization.md` plan as the foundation, avoiding any new dependencies. The `labels.json` approach is purely configuration-based, meaning language switching requires only config file changes, not code modifications.

**Modularity**: Each Phase is independent and verifiable. The system remains functional after any completed Phase, with no "broken intermediate state" risk.

**Extensibility**: The `labels.json` structure supports future language additions (e.g., Japanese, Korean) without architectural changes.

---

## Summary

This design:
- ✅ **Minimizes changes**: Builds on existing i18n plan, no new dependencies
- ✅ **Phased implementation**: 5 independent stages, each verifiable
- ✅ **Backward compatible**: Chinese users maintain experience via `-l zh`
- ✅ **Extensible**: `labels.json` structure supports future languages
- ✅ **Document-driven**: Aligns with project's existing document-driven architecture
