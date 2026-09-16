# Shadowrocket Fusion Personal v6

这是以“联网稳定优先”为目标的个人 Shadowrocket 广告屏蔽模块。

## 修复内容

- 删除 71 个远程依赖及全部远程脚本，避免脚本下载、执行或失效引发连锁故障。
- 删除约 1690 条 URL 重写，不再对普通 HTTPS 流量做重写。
- 完全关闭 MITM；YouTube、微信、百度网盘不会被解密或修改，真实会员状态保持原样。
- 删除 `DOMAIN-KEYWORD,pangolin-sdk-toutiao`，避免广告 SDK 重试风暴。
- 删除 `DOMAIN-SUFFIX,wxs.qq.com`，避免微信资源被误拦截。
- 删除对 HTTPDNS、共用 CDN 和应用核心 API 的拦截。
- 只保留精确 `DOMAIN` 广告主机规则；自动任务只做安全校验，不再自动合并上游内容。

## 使用方式

1. 在 Shadowrocket 的模块页面更新当前订阅。
2. 确认模块名称显示为“广告屏蔽（稳定修正版）”。
3. 重新启用模块后，先测试大陆网站，再测试代理网站。
4. 如果仍显示旧名称，删除旧模块后使用下方地址重新添加。

## 订阅地址

`https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/Module.sgmodule`

## 自动维护边界

`tools/fusion.py` 会拒绝以下内容进入主模块：脚本、URL 重写、MITM、远程规则集、`DOMAIN-KEYWORD`、HTTPDNS 拦截，以及 YouTube/百度网盘会员相关流量。
