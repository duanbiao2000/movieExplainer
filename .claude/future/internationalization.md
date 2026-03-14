# Future Todo - 语言参数国际化功能

## 背景

README 已完成国际化（英语/中文/日语），接下来需要实现工作流层面的多语言支持。

## 待实现功能

### 1. 添加语言参数到工作流

**文件**: `.claude/skills/extract-subtitle/SKILL.md`

- 添加 `--language` / `-l` 参数
- 支持值: `zh` (中文/默认), `en` (英语), `ja` (日语)
- 更新使用示例

### 2. 创建本地化配置文件

**文件**: `.claude/config/labels.json` (新建)

定义所有语言的标签映射：

```json
{
  "zh": {
    "anki": {
      "label_ipa": "音标",
      "label_chinese": "中文",
      "label_pos": "词性",
      "label_example": "例句",
      "label_ielts": "IELTS应用"
    }
  },
  "en": {
    "anki": {
      "label_ipa": "IPA",
      "label_chinese": "Meaning",
      "label_pos": "PoS",
      "label_example": "Example",
      "label_ielts": "IELTS Use"
    }
  },
  "ja": {
    "anki": {
      "label_ipa": "IPA",
      "label_chinese": "意味",
      "label_pos": "品詞",
      "label_example": "例文",
      "label_ielts": "IELTS活用"
    }
  }
}
```

### 3. 更新全局配置

**文件**: `.claude/config/learning-materials.json`

添加：
```json
{
  "defaultLanguage": "zh",
  "supportedLanguages": ["zh", "en", "ja"]
}
```

### 4. 修改 content-extractor

**文件**: `.claude/agents/content-extractor/agent.md`

- 添加 `language` 参数说明
- 添加标签使用说明
- 更新 Anki CSV 格式示例

### 5. 传递语言参数

修改以下 agent，确保语言参数正确传递：

- `.claude/agents/content-reviewer/agent.md`
- `.claude/agents/iteration-optimizer/agent.md`
- `.claude/agents/polish-refactoror/agent.md`

### 6. 更新文档

**文件**: `CLAUDE.md`

添加国际化功能说明。

## 优先级

| 优先级 | 功能 |
|--------|------|
| 高 | 语言参数 + labels.json + content-extractor |
| 中 | 其他 agent 参数传递 |
| 低 | 文档更新 |

## 验证方式

```bash
# 默认中文输出
/extract-subtitle test.srt

# 英语输出
/extract-subtitle test.srt --language en

# 日语输出
/extract-subtitle test.srt -l ja

# 组合参数
/extract-subtitle test.srt -l en --target-band 7.5
```
