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
