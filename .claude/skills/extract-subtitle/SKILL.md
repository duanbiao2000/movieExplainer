---
name: extract-subtitle
description: 从视频字幕文件自动提取雅思学习材料 (支持 .srt, .vtt, .txt)
---

# /extract-subtitle - 字幕学习材料提取器

你是一个协调者，负责调用各个 SubAgent 处理字幕文件，生成雅思学习材料。

## 触发时机

当用户输入 `/extract-subtitle` 或提供字幕文件路径时触发。

## 工作流程

### 步骤 1: 参数解析

从用户输入中提取参数：
- `file_path` (必需): 字幕文件路径，支持 .srt, .vtt, .txt
- `target_band` (可选): 目标雅思分数，默认 7.0
- `formats` (可选): 输出格式，逗号分隔 (md, worksheet, anki)，默认全部
- `no_review` (可选): 是否跳过审核迭代环节，默认 false
- `video_url` (可选): 视频源链接，用于生成 video-source.md 和在各文件中添加引用链接

### 步骤 2: 验证输入

确认文件存在且格式支持。

### 步骤 2.5: 参数标准化 [NEW]

使用 `param-middleware` SubAgent 处理参数：
- 将原始参数转换为标准配置对象
- 提取公共参数（video_url, target_band, formats）
- 初始化数据流转日志

**输出**: 标准化配置对象，传递给后续所有 Agent

### 步骤 3: 字幕解析

使用 `subtitle-parser` SubAgent 解析字幕文件，提取纯文本和时间戳信息。

### 步骤 4: 内容提取

使用 `content-extractor` SubAgent 提取学习内容：
- Key Points (关键观点)
- Verb Phrases (动词短语)
- Vocabulary (词汇)
- IELTS Expressions (雅思高分表达)

### 步骤 5: 质量审核

如果 `no_review` 为 false，使用：
- `content-reviewer` SubAgent 进行质量检查
- `iteration-optimizer` SubAgent 进行多轮优化

### 步骤 6: 格式化输出

生成学习材料文件：
- `key-points.md` - 关键观点
- `vocabulary.md` - 词汇表
- `verb-phrases.md` - 动词短语
- `ielts-expressions.md` - 雅思高分表达
- `worksheet.csv` - 练习工作表（Excel 可打开）
- `anki-deck.csv` - Anki 导入文件（制表符分隔，带 HTML 标签）
- `anki-deck.apkg` - Anki 卡组包（双击直接导入）**[可选]**

**注意**: 仅生成纯学习材料，不生成 study-plan.md 等辅助性文档。

#### anki-deck.csv 格式规范

```csv
#separator:tab
#html:true
#tags:true

Front	Back	Tags
"comprehensive"	"<b>音标</b>: /ˌkɒmprɪˈhensɪv/<br><b>中文</b>: 全面的<br><b>词性</b>: adj<br><b>搭配</b>: ...<br><b>IELTS评分</b>: LR 7.0+"	"vocabulary academic priority-2"
"account for"	"<b>中文</b>: 是……的原因<br><b>例句</b>: ...<br><b>IELTS应用</b>: ..."	"verb-phrase priority-1"
```

**音标规则**:
- `vocabulary-*` 和 `topic-*` 标签的卡片 → **添加音标**，格式 `<b>音标</b>: /音标/<br>`，置于 Back 字段最前
- `verb-phrase-*`, `expression-*`, `key-point-*`, `collocation-*` → **不添加音标**

### 步骤 7: 保存文件

将结果保存到字幕文件同目录下的 `learning-materials/` 文件夹。

**如果提供了 `video_url` 参数**，额外生成 `video-source.md`：

```markdown
# 视频源信息

## 原始视频

[点击观看视频](VIDEO_URL)

## 元数据

- **视频标题**: [从字幕文件名提取]
- **生成日期**: [当前日期 YYYY-MM-DD]
- **目标分数**: Band [target_band]
- **字幕文件**: [subtitle_file].srt
```

**同时**，将 `video_url` 传递给 `content-extractor` SubAgent，使其在所有生成的 `.md` 文件顶部添加视频链接引用：

```markdown
---
**视频源**: [观看原视频](VIDEO_URL)
---
```

## 输出结构

```
video-lesson.srt
└── learning-materials/
    ├── video-source.md       # 视频源信息 [当提供 video_url 时]
    ├── key-points.md          # 关键观点
    ├── vocabulary.md          # 词汇表
    ├── verb-phrases.md        # 动词短语
    ├── ielts-expressions.md   # 雅思高分表达
    ├── worksheet.csv          # 练习工作表（Excel 可打开）
    ├── anki-deck.csv          # Anki 导入文件（制表符分隔）
    └── anki-deck.apkg         # Anki 卡组包（双击导入）[可选]
```

**导入说明**:
- `worksheet.csv`: 直接用 Excel 打开
- `anki-deck.csv`: Anki → 文件 → 导入（制表符分隔，勾选"允许 HTML"）
- `anki-deck.apkg`: 双击直接导入 Anki（需运行 `python .claude/scripts/csv-to-anki.py` 生成）

**生成 .apkg**:
```bash
python .claude/scripts/csv-to-anki.py learning-materials/anki-deck.csv
```

## 使用示例

```
/extract-subtitle examples/sample-lesson.srt
/extract-subtitle examples/sample-lesson.srt --target-band 7.5
/extract-subtitle examples/sample-lesson.srt --formats md,anki
/extract-subtitle examples/sample-lesson.srt --no-review
/extract-subtitle examples/sample-lesson.srt --video-url https://www.bilibili.com/video/BV1xxx/
```
