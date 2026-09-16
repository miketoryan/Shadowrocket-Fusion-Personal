# Shadowrocket Fusion Personal v3

这是完全独立维护的 Shadowrocket 融合模块仓库。压缩包已经内置处理完成的
`Module.sgmodule`，不再从任何父融合仓库下载或覆盖模块。

## 最简建库步骤

1. 新建一个空 GitHub 仓库，建议名称：`Shadowrocket-Fusion-Personal`
2. 上传：
   - `tools/fusion.py`
   - `sources.json`
   - `README.md`
   - `Module.sgmodule`
3. 如果网页拖拽没有上传 `.github`，就在 GitHub 里：
   `Add file → Create new file`
   文件名填写：
   `.github/workflows/fusion.yml`
   然后把根目录 `WORKFLOW-fusion.yml` 的内容完整复制进去。
4. `Settings → Actions → General → Workflow permissions`
   选择 `Read and write permissions`
5. `Actions → Maintain personal fusion module → Run workflow`

`Module.sgmodule` 是本仓库唯一主版本。维护程序只检查和维护这个文件；如果文件缺失，
任务会直接报错，不会回头下载原融合仓库。

## 本版已完成

- 原融合模块中69项失效脚本地址已替换为当前存在的地址
- 8个已确认不保留的脚本声明已删除
- 横店电影的404资源已替换为可用地址
- 已删除2条伪造哔哩哔哩 VIP 状态的内联重写
- 不再残留 `xiangwanguan.github.io` 地址
- 个人保护模块仍保持独立，不合并进本仓库

## 自动维护规则

- 404 / 410：连续确认两次失效，才自动删除对应声明
- 检查范围：`script-path`、`RULE-SET`、`[URL Rewrite]` 中的静态远程资源
- 403 / 429 / 超时：标记 UNKNOWN，保留
- 一年以上未更新但仍可访问：标记 STALE，保留
- QQ 新闻、贴吧：从 `app2smile/rules` 自动同步白名单内的广告接口定义
- 上游内容必须同时通过仓库、区段、依赖地址和风险内容检查；失败时不修改现有规则
- 明确的 VIP/解锁伪造及 Crack 脚本声明会自动删除
- 每日下载现有远程脚本做风险扫描；命中高可信解锁特征时自动停用对应声明
- `fmz200` 合集及 Quantumult X 格式来源只监控变化，不整库自动合并

## 安全边界

- 不自动引入 VIP、订阅、清晰度解锁、地区绕过或第三方 API 转发
- 哔哩哔哩、YouTube、微信、百度网盘、闲鱼等个人规则继续独立维护
- 自动同步只允许 `sources.json` 中列出的仓库和区段
- `reports/interface-updates.md` 会记录每个来源是 `SYNCED` 还是 `BLOCKED`

## Shadowrocket 订阅地址

如果仓库名就是 `Shadowrocket-Fusion-Personal`：

`https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/Module.sgmodule`
