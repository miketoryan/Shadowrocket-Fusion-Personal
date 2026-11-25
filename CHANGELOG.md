# 广告屏蔽联网版｜实质更新记录

这里**只记录正式订阅文件 `Module.sgmodule` 的规则、脚本引用、MITM 或广告响应逻辑发生实际变化的时间**。每天自动检查但没有变更时不新增记录，也不刷新模块的时间标签。

自动规则同步每次最多新增 10 个通过安全过滤的精确广告域名。新增不代表经过手机端实测；静态校验通过也不等于能够屏蔽所有 App 广告。

<!-- EFFECTIVE_UPDATES_START -->

## 2026-11-25 22:12（北京时间）｜豆瓣 / B站开屏修复及日志补漏

**类型：** 人工审核 2026-11-25 PacketTunnel 日志后的专项更新。

- 新增 4 个精确广告域名：`erebor.douban.com`、`ad.doubanio.com`、`bootrealtime.uve.weibo.com`、`iadmatapk.nosdn.127.net`。
- 豆瓣：`app_ads` 改为成功的空 JSON 响应；新增 frodo 明确广告接口及图片服务器 `dale_ad` 广告素材专用路径，补齐 MITM。域名及素材路径参考 fmz200 上游，未拦整个图片域名。
- B站：四个开屏接口统一走响应脚本，返回成功的空广告配置；处理缺失 data、数组和未知嵌套结构，取消旧的一年刷新间隔，并通过版本化 URL 更新脚本。
- 网易云：新增 `eapi/xeapi` 广告目录定向拦截，覆盖日志中实际漏过的 loading/get、bidget、get、materialconfig 等请求；补齐 interface 系列及 IPv4 / IPv6 主机。
- 微博：补上实时开屏广告服务器。
- 保留 Apple TV / Pay、YouTube 和正常业务的现有保护。离线检查不代表手机端已验证，也无法删除 App 沙盒的历史广告文件。

上游核对：[fmz200](https://github.com/fmz200/wool_scripts/blob/main/Shadowrocket/module/blockAds.srmodule)。日志原文与用户标识不上传仓库。


## 2026-10-19 12:57（北京时间）｜自动新增 8 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：8 条；删除：0 条。**

新增域名：
- `iqiyim.adtrack.enlightent.cn`
- `mobad.ijinshan.com`
- `optimus-ads.amap.com`
- `optimus-ads.amap.com.w.alikunlun.com`
- `sdkconfig.ad.xiaomi.com`
- `soul-ad.soulapp.cn`
- `t-ads.xiaohongshu.com`
- `yk-ssp.ad.youku.com`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


## 2026-10-18 12:48（北京时间）｜自动新增 10 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `advertise.baicizhan.com`
- `advertise.baicizhan.org`
- `adx-os.bridgeturbo.com`
- `adx.adtaipo.com`
- `adx.yiche.com`
- `adxapi.readgps.com`
- `adxlog.vivo.com.cn`
- `app-ad.variflight.com`
- `cdn-new-ad.wtzw.com`
- `img.auction-ads.wpscdn.cn`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


## 2026-10-17 12:42（北京时间）｜自动新增 10 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `ads.mojicdn.com`
- `ads.service.kugou.com`
- `ads.yahoo.de`
- `adsapi.snapchat.com`
- `adsdk.vivo.com.cn`
- `adse.wsa.ximalaya.com`
- `adsehera.ximalaya.com`
- `adserviceretry.kugou.com`
- `adsstatic.vivo.com.cn`
- `adv-ads.variflight.com`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


## 2026-10-16 12:45（北京时间）｜自动新增 10 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `ads-marketing-vivofs.vivo.com.cn`
- `ads-shopping.shouqianba.com`
- `ads-video-al.xhscdn.com`
- `ads-video-qc.xhscdn.com`
- `ads.95516.com`
- `ads.aplus.pptv.com`
- `ads.aplusapi.pptv.com`
- `ads.auctions.yahoo.com`
- `ads.cup.com.cn`
- `ads.finance.yahoo.com`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


## 2026-10-15 12:54（北京时间）｜自动新增 10 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `admarket.21cn.com`
- `admarketing.yahoo.net`
- `admonitor.thepaper.cn`
- `adnew.wifi8.com`
- `adpai.thepaper.cn`
- `adproxy.autohome.com.cn`
- `adreport.adtianmai.com`
- `adreq.vivo.com.cn`
- `ads-img-al.xhscdn.com`
- `ads-img-qc.xhscdn.com`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


## 2026-10-14 13:05（北京时间）｜自动新增 10 条广告域名

**类型：** 可信上游精确广告域名安全同步（fmz200）。**新增：10 条；删除：0 条。**

新增域名：
- `ad.mobile.youku.com`
- `ad.qingting.fm`
- `ad.seeyouyima.com`
- `ad.yixin.im`
- `ad.zijieapi.com`
- `adcdn.hpplay.cn`
- `adfile.wifi8.com`
- `adlaunch.moji.com`
- `adlaunch.qingting.fm`
- `adlog.vivo.com.cn`

本次只更新精确域名规则；未导入第三方脚本、MITM 或宽泛拦截。静态检查不代表 App 端已验证。


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

