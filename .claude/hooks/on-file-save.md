---
description: 监控字幕文件保存，自动触发处理
---

# On File Save Hook

监控字幕文件保存事件，自动触发学习材料生成。

## 触发条件

满足以下条件时触发：
1. 文件扩展名匹配: `.srt`, `.vtt`, `.txt`
2. 文件位于 `projects/` 目录下
3. 配置中 `autoProcessOnSave` 为 `true`

## 文件模式

**监控模式**:
```json
{
  "watchPatterns": [
    "projects/**/*.srt",
    "projects/**/*.vtt",
    "projects/**/*.txt"
  ],
  "excludePatterns": [
    "**/learning-materials/**",
    "**/node_modules/**",
    "**/.git/**"
  ]
}
```

## 行为逻辑

```
文件保存事件
    │
    ▼
检查文件扩展名
    │
    ├─ 不匹配 → 忽略
    │
    └─ 匹配 → 继续检查
              │
              ▼
        检查是否在监控目录
              │
              ├─ 否 → 忽略
              │
              └─ 是 → 继续检查
                    │
                    ▼
              检查 autoProcessOnSave
                    │
                    ├─ false → 仅记录通知
                    │
                    └─ true → 自动处理
                          │
                          ▼
                    调用 /extract-subtitle
                          │
                          ▼
                    在后台处理，不阻塞编辑
```

## 用户通知

当文件被保存时：

**自动处理开启**:
```
📁 检测到字幕文件: video.srt
🔄 开始生成学习材料...
✅ 完成！材料已保存到 learning-materials/
```

**自动处理关闭**:
```
📁 检测到字幕文件: video.srt
💡 提示: 运行 /extract-subtitle video.srt 生成学习材料
```

## 配置

在 `.claude/config/learning-materials.json` 中配置：

```json
{
  "autoProcessOnSave": false,
  "notification": {
    "showOnSave": true,
    "showWhenProcessed": true
  }
}
```

## 注意事项

1. **不阻塞编辑** - 处理在后台进行，不影响用户继续编辑
2. **避免重复处理** - 检查文件是否已处理过
3. **错误处理** - 处理失败时给出清晰的错误信息
4. **可取消** - 允许用户取消正在进行的处理
