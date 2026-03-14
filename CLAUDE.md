# MovieExplainer Project Configuration

This is the Claude Code configuration file for the MovieExplainer project.

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
