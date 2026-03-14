# MovieExplainer 项目配置

这是 MovieExplainer 项目的 Claude Code 配置文件。

## 项目概述

雅思字幕学习材料自动生成工作流系统。

## 可用命令

### /extract-subtitle

处理字幕文件，生成学习材料。

**用法**:
- `/extract-subtitle <文件路径>` - 处理指定字幕
- `/extract-subtitle <文件路径> --target-band 7.5` - 指定目标分数
- `/extract-subtitle <文件路径> --formats md,anki` - 选择输出格式

## 工作流组件

- **字幕解析器** (`.claude/agents/subtitle-parser/`) - 解析 SRT/VTT/TXT 格式
- **内容提取器** (`.claude/agents/content-extractor/`) - 提取学习内容
- **内容审核器** (`.claude/agents/content-reviewer/`) - 质量检查
- **迭代优化器** (`.claude/agents/iteration-optimizer/`) - 多轮改进
- **雅思学习顾问** (`.claude/agents/ielts-coach/`) - 交互式个性化定制
- **润色重构器** (`.claude/agents/polish-refactoror/`) - 风格化+元认知强化

## 输出位置

学习材料默认保存在字幕文件同目录下的 `learning-materials/` 文件夹。

## 配置文件

项目级配置位于 `.claude/config/learning-materials.json`。
