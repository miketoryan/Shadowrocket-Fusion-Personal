# Shadowrocket Fusion Personal

这是我的 Shadowrocket 广告屏蔽模块仓库。当前以 **联网稳定优先**，`Module.sgmodule` 是唯一正式使用版本。

## 当前规则版本

当前 `Module.sgmodule` 为“核心稳定版综合修正版”，在核心稳定版基础上保留广谱广告拦截，并增加/修正了高德地图、爱思全能版、微信公众号、腾讯手机助手/手机管家、网易云、闲鱼、住这儿、航旅纵横等定向规则。

已删除日志中确认失效的 `jd.js` 与 `umetrip_ads.js`，并移除容易产生大量 SSL verify failed 的 `api.m.jd.com` MITM。

## 更新方式

- **仓库优先**：以后规则有修改，先更新本仓库的 `Module.sgmodule`。
- 手机端不再手工替换整份模块，只需要在 Shadowrocket 中更新订阅。
- GitHub Actions 只负责检查 `Module.sgmodule` 的基本结构和已知失效脚本，不再自动合并上游规则，也不会自动覆盖人工确认的版本。
- 旧的 `tools/fusion.py`、`sources.json` 等文件仅作为历史/开发资料，不参与当前手机订阅的生成。

## Shadowrocket 订阅地址

```text
https://raw.githubusercontent.com/miketoryan/Shadowrocket-Fusion-Personal/main/Module.sgmodule
```

在 Shadowrocket 中使用上面的链接添加模块。以后仓库更新后，在模块页面点击更新即可获取最新规则。

## 当前维护原则

1. 优先根据实际日志补规则，不盲目扩大 MITM。
2. 能用域名级 `REJECT` 解决的，不增加 HTTPS 解密。
3. 对微信、银行、支付、京东等敏感链路尽量保守处理。
4. 不为了“去广告”修改会员状态、解锁功能或大规模重排 App UI。
5. 出现联网异常时优先回滚新增 MITM / Script，而不是继续叠加规则。
