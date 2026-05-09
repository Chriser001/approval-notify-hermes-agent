# approval-notify

Hermes 审批请求 macOS 系统通知插件。危险命令触发审批时，弹出可点击的系统通知 + 提示音。

## 功能

- 🔔 **系统通知** — 显示命令、来源、匹配规则
- 🔊 **双重提示音** — `Glass`（通知音）+ `Hero`（增强提醒）
- 👆 **点击回到终端** — 点击通知激活 Terminal.app，直接看到审批提示

## 依赖

```bash
brew install terminal-notifier
```

## 安装

插件安装至 `~/.hermes/plugins/approval-notify/` 下，重启 Hermes 自动加载。

## 工作流程

```
审批触发 → pre_approval_request hook
  ├── terminal-notifier → 系统通知（Glass 提示音）
  ├── afplay Hero.aiff  → 增强提醒音
  └── 用户点击通知 → 激活 Terminal.app → 处理审批
```

## 关键设计

- **非阻塞** — 所有通知用 `subprocess.Popen` 火后即忘，不阻塞审批流程
- **容错** — 通知失败只打 debug 日志，绝不 crash Hermes
- **`terminal-notifier`** — 比 `osascript` 更可靠：原生支持换行符/引号、可绑定点击行为

## 为什么不用 osascript？

`osascript display notification` 有两个硬伤：

1. **字符串不能含换行符** — body 里的 `\n` 会静默破坏 AppleScript 语法，通知发不出来
2. **点击无行为** — 默认打开 Script Editor，没法绑定到终端
