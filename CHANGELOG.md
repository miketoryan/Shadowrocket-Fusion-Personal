# 广告屏蔽联网版｜实质更新记录

这里**只记录正式订阅文件 `Module.sgmodule` 的规则、脚本引用、MITM 或广告响应逻辑发生实际变化的时间**。每天自动检查但没有变更时不新增记录，也不刷新模块的时间标签。

自动规则同步每次最多新增 10 个通过安全过滤的精确广告域名。新增不代表经过手机端实测；静态校验通过也不等于能够屏蔽所有 App 广告。

<!-- EFFECTIVE_UPDATES_START -->

## 2026-10-13 23:14（北京时间）｜自动新增 10 条广告域名

**类型：** 安全受控上游同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `ad-cdn.qingting.fm`
- `ad-r.soulapp.cn`
- `ad-reward.soulapp.cn`
- `ad-stat.ksosoft.com`
- `ad.21cn.com`
- `ad.360in.com`
- `ad.chelaile.net.cn`
- `ad.hpplay.cn`
- `ad.k.21cn.com`
- `ad.mcloud.139.com`

[查看当次正式模块提交](https://github.com/miketoryan/Shadowrocket-Fusion-Personal/commit/89dde523fe0d)

## 2026-10-13 23:10—23:11（北京时间）｜京东、联通、闲鱼、B站专项增强

**类型：** 人工审核后修改正式模块。包含京东 12 个精确域名、5 条定向 URL Rewrite、2 个新的广告字段清理脚本、B站开屏脚本替换及所需 MITM 主机补充。保留支付、登录和正常业务保护。

**缓存广告：** 京东和 B站在广告响应下发时清理已知广告字段，闲鱼只过滤明确标记为广告的信息流；不能远程删除 App 沙盒中已缓存的旧广告文件。

[查看主要规则提交](https://github.com/miketoryan/Shadowrocket-Fusion-Personal/commit/e52f396ef7fe287160ca36069dfddd21a25fb9d3) · [B站脚本兼容修正](https://github.com/miketoryan/Shadowrocket-Fusion-Personal/commit/f53885dee87908ade456b78ca7216284600a830f)

<!-- EFFECTIVE_UPDATES_END -->
