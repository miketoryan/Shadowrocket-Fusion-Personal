# Shadowrocket Fusion Personal v6

这是以联网稳定为前提、支持受控自动更新和应用级定向处理的个人 Shadowrocket 广告屏蔽模块。

## 当前结构

- 稳定核心：人工确认的精确广告域名规则。
- 自动增量：只接受通过全部安全检查的精确 `DOMAIN,REJECT` 广告域名。
- 定向处理：豆瓣、B站、航旅纵横、小宇宙、百度网盘、微信公众号及微信原生小程序广告。
- 不包含远程规则集、`DOMAIN-SUFFIX` 或 `DOMAIN-KEYWORD`。

## 自动更新流程

1. 每日读取 `sources.json` 中固定仓库、固定路径的上游文件。
2. 通用上游只提取精确 `DOMAIN,REJECT`，忽略其脚本、重写、MITM、规则集和广域规则。
3. 域名必须带明确广告特征，并通过核心服务保护列表。
4. 自动排除 YouTube、微信、百度、Apple、Google、哔哩哔哩、爱奇艺、淘宝、京东、美团等核心域名。
5. 校验上游规模、筛选后规模、单次增删数量及变化比例。
6. B站和航旅纵横脚本更新时先扫描内容，再固定到通过审核的 Git 提交版本。
7. 任一检查失败，原 `Module.sgmodule` 保持不变。

目前 `fmz200` 仅作为候选域名数据源，绝不会整库合并。B站只使用 `app2smile` 的两个定向去广告脚本；航旅纵横只使用一个广告位识别脚本。百度网盘使用本仓库的广告专用脚本，不读取或修改会员接口。

微信公众号只处理 `mp.weixin.qq.com/wapad` 广告接口；微信原生小程序广告只拦截 `wxsmsdy.video.qq.com`，不会封锁 `wxs.qq.com` 或微信安全接口。第三方小程序自身业务接口的广告仍需按具体小程序单独添加。

## 更新限制

- 自动规则总量最多 200 条。
- 单次最多新增 20 条、删除 20 条。
- 自动规则总数变化超过 25% 时拒绝更新。
- 自动更新只能改动 `BEGIN/END CONTROLLED AUTO RULES` 标记之间的内容。

## 使用方式

在 Shadowrocket 模块页面更新当前订阅，名称应显示为“广告屏蔽”。

订阅地址：

`https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/Module.sgmodule`
