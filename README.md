# 广告屏蔽联网版

这是一个用于 **Shadowrocket（小火箭）** 的个人广告屏蔽模块仓库，目标是在尽量保持联网稳定、减少误杀和降低 MITM 范围的前提下，屏蔽常用 App 的开屏广告、信息流广告、推广接口及常见第三方广告 SDK。

- **模块名称：** 广告屏蔽联网版
- **最近更新时间：** 2026-10-09 18:29
- **正式订阅文件：** `Module.sgmodule`
- **维护方式：** 先更新 GitHub 仓库规则，再由手机端通过订阅链接更新

## 规则涉及的软件

当前模块重点包含以下 App / 场景的定向广告规则：

- 12306
- B站
- 百度地图
- 美图秀秀
- 微店
- 微博 / 微博国际版
- QQ音乐
- 下厨房
- 高德地图
- 爱思全能版
- 微信公众号文章广告
- 腾讯手机助手
- 腾讯手机管家
- 网易云音乐
- 闲鱼
- 住这儿
- 途强智能
- 豆瓣
- 小宇宙
- 航旅纵横
- 百度网盘
- 京东
- 淘宝

此外还包含中国联通、美团 / 大众点评、部分银行广告或跟踪域名，以及穿山甲 / Pangle、腾讯广点通、百度广告、友盟、1RTB、Sigmob、Menta 等常见第三方广告 SDK 的域名级拦截规则。

> 规则覆盖以当前 `Module.sgmodule` 为准。部分 App 只做域名级广告拦截，部分 App 会使用 URL Rewrite / Body Rewrite / Script / MITM 做定向处理。

## 这次重点补强

- **12306：** 拦截专用广告域名 `ad.12306.cn`。
- **B站：** `list/show` 开屏响应采用 app2smile 脚本的固定 commit，避免直接追随可变的 `master`；`brand/list`、`event/list2` 保留精确接口拦截。
- **百度地图：** 增加 `newclient.map.baidu.com/...qt=ads` 精确广告接口，并补充 `afd.baidu.com`、`afdconf.baidu.com` 与日志实证的 1RTB 兜底。
- **美图秀秀：** 增加 `mea.meitudata.com/kaiping` 开屏接口以及 `adui.tg.meitu.com` 等美图广告域名。
- **微店：** 增加 `thor.weidian.com/ares/home.splash` 精确开屏接口，并保留第三方广告 SDK 兜底。
- **微博：** 将旧的 `/v1/ad/preload` 单一路径规则升级为 `bootpreload.uve.weibo.com` 精确广告主机拦截，覆盖当前日志中的 `/v2/ad/preload`，无需额外 MITM。
- **QQ音乐：** 仅加入 `ad*.tencentmusic.com` 与 `tmead*.y.qq.com` 等专用广告主机，不加入音乐业务域名，也不新增 QQ音乐 MITM。
- **下厨房：** 增加 `api.xiachufang.com/v*/ad/` 精确广告接口，并补充日志实证且被多库交叉确认的快手、1RTB、UYUN 广告备用通道。

## 这个库的作用

1. **统一维护广告屏蔽规则**：手机端不再手工复制整份规则，所有正式修改先进入 GitHub。
2. **保持联网稳定优先**：尽量减少不必要的 HTTPS 解密和过宽域名匹配，降低断网、SSL 握手失败、支付或银行 App 异常的风险。
3. **按实际日志修规则**：新广告优先根据 Shadowrocket 日志定位真实广告接口，再与成熟规则库交叉验证后做定向补充。
4. **避免功能篡改**：不为了去广告修改会员状态、解锁付费功能或大规模重排 App UI。
5. **集中订阅更新**：GitHub 中的 `Module.sgmodule` 是唯一正式联网版本，手机只需刷新订阅即可获取最新规则。

## Shadowrocket 更新链接

```text
https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/Module.sgmodule
```

在 Shadowrocket 的模块页面使用上面的链接添加订阅。以后规则更新后，只需要对该模块执行“更新”即可。

## 模块显示信息

手机通过订阅链接更新后，模块应显示：

```text
广告屏蔽联网版
仓库更新时间：2026-10-09 18:29
```

其中第二行来自 `Module.sgmodule` 的 `#!desc`，每次正式修改仓库规则时同步更新日期。

## 当前维护原则

- 使用 YouTube Premium，不启用 YouTube 去广告规则、脚本或专用路由；YouTube 流量交由主配置分流并使用手动选择的代理节点。模块中仅保留 YouTube 的不解密排除项。

- 能用精确域名级 `REJECT` 解决的，不增加 MITM。
- 能用单一广告接口解决的，不扩大为整个业务域名或整站后缀。
- 对微信、银行、支付、京东等敏感链路采用更保守的处理方式。
- 外部脚本优先固定到已审核 commit；不直接把第三方整库自动合并进正式模块。
- GitHub Actions 负责去重、应用已批准的高置信度规则、更新时间并执行验证；验证失败时不会提交新的正式模块。
- 出现联网异常时优先回滚最新新增的 MITM / Script / Rewrite，而不是继续叠加规则。


## 手动导入的混合分流配置

- **文件：** `profiles/Smart-Hybrid-AI-Remote-DNS-Test-Fixed.conf`
- **用途：** AI / Google 域名强制代理并远程解析 DNS；中国 IP 和 Apple TV（`tv.apple.com`、`tv.applemusic.com`）直连；未命中规则的流量由代理兜底。
- **下载：** https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/profiles/Smart-Hybrid-AI-Remote-DNS-Test-Fixed.conf
- **安全说明：** 公开版本不包含 MITM CA 证书、私钥或口令。需要 MITM 时，请在设备上使用自己的私有证书；不要将证书密钥提交到仓库。
- 这是独立的手动导入配置；正式广告订阅文件仍为 `Module.sgmodule`。

## 本次精简与固定核对项

- 淘宝两条脚本分别命名为 `taobao-guide`、`taobao-poplayer`；脚本地址、匹配范围与处理逻辑不变。
- 主配置补充 `DOMAIN,tv.applemusic.com,DIRECT`，不扩大整个 Apple 域名的处理范围。
- DNS 地址保留 Cloudflare 主用、Google 备用，将转发参数简化为 `#proxy`，跟随手动选择的默认节点。
- 明确 `dns-direct-fallback-proxy = false`，直连解析失败时不自动改走代理；代价是这类失败不会借代理恢复。
- 不添加自动测速或自动切换节点。使用 Apple News 后，手动切回“配置”模式再检查直连。

每次更新需核对主配置、启用模块及当时在线规则集的组合：

1. Apple TV 专项域名（`tv.apple.com`、`tv.applemusic.com`、`hls-amt.itunes.apple.com`、`hls.itunes.apple.com`、`np-edge.itunes.apple.com`、`play-edge.itunes.apple.com`、`uts-api.itunes.apple.com`）没有被模块改成代理或拦截。
2. `apple-pay-gateway.apple.com`、`cn-apple-pay-gateway.apple.com` 仍为直连；设备私有配置保留支付网关的不解密排除项。公开配置不附带私有证书。
3. 脚本名称唯一，YouTube 去广告及旧“油管视频”策略引用没有重新引入。
4. 本次仓库静态核对只涵盖这份主配置、广告模块与读取时的在线列表。手机上其他启用模块、缓存和真实播放/支付请求需以设备记录为准；静态核对不能保证播放速度。
