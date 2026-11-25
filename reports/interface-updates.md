# 上游变化与持续待审核清单

最近检查：2026-11-25 22:37（北京时间）；结果：**有变化待审核**。

首次运行建立完整基线，清单包含尚未采用的历史存量，不代表当天新增；后续比较新增、删除及内容哈希。待审核项目会持续保留，不会因第二天没有新变化而消失。来源规则被删除时，不会擅自删除本地人工规则。

完整条目、来源、原因、增删和脚本哈希均见 [upstream-review.json](upstream-review.json)。下方每类最多预览 30 项，JSON 不截断。

## AND（39 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,-ad-),(DOMAIN-SUFFIX,byteimg.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,-ttam-),(DOMAIN-SUFFIX,ibyteimg.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,ads),(DOMAIN-KEYWORD,-normal-lq),(DOMAIN-SUFFIX,zijieapi.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,ads),(DOMAIN-KEYWORD,normal),(DOMAIN-SUFFIX,zijieapi.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api),(DOMAIN-KEYWORD,-access-),(DOMAIN-SUFFIX,pangle.io)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api),(DOMAIN-KEYWORD,-dual-event-),(DOMAIN-SUFFIX,pangle.io)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api),(DOMAIN-KEYWORD,-log-),(DOMAIN-SUFFIX,pangle.io)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api),(DOMAIN-KEYWORD,pangolin),(DOMAIN-SUFFIX,sgsnssdk.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api100-core-quic-),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api100-normal-quic-),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api100-normal-quic-aweme-),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api100-quic-core-),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,api100-quic-normal-),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,frontier-aweme-),(AND,((OR,((DOMAIN-KEYWORD,-ipa.),(DOMAIN-KEYWORD,-ipainner.),(DOMAIN-KEYWORD,-origin.),(DOMAIN-KEYWORD,-ipainner-))),(OR,((DOMAIN-SUFFIX,snssdk.com),(DOMAIN-SUFFIX,amemv.com)))))),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,frontier100-aweme),(DOMAIN-SUFFIX,amemv.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,if),(DOMAIN-KEYWORD,-analytics.bytescm.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,if),(DOMAIN-KEYWORD,-cdn-tos.bytescm.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,lf),(DOMAIN-KEYWORD,-analytics.bytescm.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,lf),(DOMAIN-KEYWORD,-short.bytetos.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,ma5-normal-),(DOMAIN-SUFFIX,zijieapi.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,pangolin),(DOMAIN-SUFFIX,sgsnssdk.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,polaris5-normal-),(DOMAIN-SUFFIX,zijieapi.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,s),(DOMAIN-KEYWORD,-fe-scm.pglstatp-toutiao.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,sf),(DOMAIN-KEYWORD,-be-pack.pglstatp-toutiao.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,sf),(DOMAIN-KEYWORD,-fe-tos.pglstatp-toutiao.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,sf),(DOMAIN-KEYWORD,-static.i18n-pglstatp.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,sf),(DOMAIN-KEYWORD,-ttcdn-tos.pstatp.com)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,ssdk-),(DOMAIN-SUFFIX,pangle.io)),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,tnc),(AND,((OR,((DOMAIN-KEYWORD,-bjlgy),(DOMAIN-KEYWORD,-alisc),(DOMAIN-KEYWORD,-aliec),(DOMAIN-KEYWORD,-alisg))),(OR,((DOMAIN-SUFFIX,snssdk.com),(DOMAIN-SUFFIX,isnssdk.com),(DOMAIN-SUFFIX,toutiaoapi.com),(DOMAIN-SUFFIX,bytedance.com),(DOMAIN-SUFFIX,zijieapi.com)))))),REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `AND,((DOMAIN-KEYWORD,v),(DOMAIN-KEYWORD,-be-pack.pglstatp-toutiao.com)),REJECT`

## DOMAIN（324 项待审核）

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,39d83s.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,a-remad.qm989.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,a.wkanx.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,aaid.umeng.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,aaid.uyunad.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,aboard.apilocate.amap.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,access.open.uc.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,acs4baichuan.m.taobao.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,activity-ag.awemeughun.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,ad.api.moji.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adashxgc.ut.taobao.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adbehavior.wsa.ximalaya.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adbehavior.ximalaya.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adc.hpplay.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adeng.hpplay.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adm.10jqka.com.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adm0.autoimg.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adm1.autoimg.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adm2.autoimg.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adm3.autoimg.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,ads.youtube.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adsfile.bssdlbig.kugou.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adsfs.oppomobile.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adshows.21cn.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,adv-adlog.variflight.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,advertising.apple.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,aid.m.taobao.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,al.autohome.com.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,ali-stats.jpush.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN,als.baidu.com,REJECT`

## DOMAIN-KEYWORD（104 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,-ad-sign.byteimg.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,-ad.byteoversea.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,-tos.pstatp.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,XiaoQiang,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,a.wkanx.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,a3.bytecdn.cn,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,a3.pstatp.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adash.man.aliyuncs.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adform,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adm3.autoimg.cn,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adproxy.autohome.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adservice.kugou.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adsfilebssdlbig.ali.kugou.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,adshare.toutiao.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,android.bugly.qq.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,ap.51y5.net,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,api-access.pangolin-sdk-toutiao,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,api-access.pangolin-sdk-toutiao.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,api.freed.so,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,apiinit.amap.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,apimg.qunliao.info,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,app.51y5.net,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,applogapi.autohome.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,asiad.byteactivity,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,av1.xdrig.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,bds.snssdk.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,bj.imp.voiceads.cn,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,c-hzgt2.getui.com,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,c.51y5.net,REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `DOMAIN-KEYWORD,c.wkanx.com,REJECT`

## DOMAIN-SUFFIX（2162 项待审核）

- **fmz200-exact-ad-domains** — 域名或规则参数需要审核

  `DOMAIN-SUFFIX,-normal-lq.zijieapi.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,0.r.msn.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1.hao123.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1.letvlive.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1.qtmojo.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1.wps.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,10086.cn.baidu.cdn.yiwk.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,123.sogou.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1a-1791.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1rtb.net,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,1sapp.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,2.letvlive.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,2016.sina.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,31.media.tumblr.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,33.autohome.com.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,360baidus.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,360shopping.com.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,3dm.huya.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,3dns-2.adobe.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,3dns-3.adobe.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,3rd.t.sohu.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,4dvertible.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,58.xgo.com.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,58mingri.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,58mingtian.cn,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,73.sinawap.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,8.jrj.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,888.tv.sohu.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,92x.tumblr.com,REJECT`

- **fmz200-exact-ad-domains** — 受保护域名或未经审核的后缀规则

  `DOMAIN-SUFFIX,a.9game.cn,REJECT`

## IP-CIDR（33 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,101.124.19.122/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,101.227.200.11/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,101.227.200.28/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,101.227.97.240/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,101.36.166.16/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,103.41.167.237/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,114.119.160.0/21,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,114.132.165.205/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,115.236.121.195/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,115.236.121.51/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,117.71.105.23/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,117.92.229.188/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,118.89.204.198/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,120.222.240.171/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,120.240.95.37/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,120.27.235.201/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,121.196.197.147/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,122.229.29.89/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,122.229.8.47/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,124.192.153.42/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,180.76.76.200/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,180.96.2.114/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,203.107.1.1/24,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,203.107.63.154/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,211.161.101.110/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,218.94.207.205/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,47.110.187.87/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,47.56.131.76/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,47.97.215.55/32,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR,47.99.42.29/32,REJECT,no-resolve`

## IP-CIDR6（2 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR6,2402:4e00:1200:ed00:0:9089:6dac:96b6/128,REJECT,no-resolve`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `IP-CIDR6,2402:db40:5100:1011::5/128,REJECT,no-resolve`

## MITM（4 项待审核）

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `hostname = %APPEND% gab.122.gov.cn, ad.12306.cn, api.21jingji.com, tianqi.2345.com, ad.life.360.cn, gateway.36kr.com, evs.500.com, api.u51.com, vip7.fzwdyy.cn, *.qyfxgd.cn, *.weilai555.com, *.ecoliving168.com, *.58cdn.com.cn, app.58.com, aes.acfun.cn, api-new.app.acfun.cn, gw.aihuishou.com, api.bjxkhc.com, b2baifanfan.baidu.com, manager.aiqiangua.com, list-app-m.i4.cn, mapi.txcmapp.com, icc.one, acs.m.taobao.com, heic.alicdn.com, guide-acs.m.taobao.com, poplayer.template.alibaba.com, api.alipan.com, member.alipan.com, api-cslp-emt.amazon.cn, www.ahzs10000.com, interface.aomiapp.com, sso.ifanr.com, www.onstar.com.cn, api.shanghaionstar.com, -i.vip.iqiyi.com, *.iqiyi.com, cache.bydauto.com.cn, aimg.babytreeimg.com, plough.babytree.com, mapiweb.babytree.com, go.babytree.com, www.baidu.com, fcvbjbcebos.baidu.com, cover.baidu.com, baichuan.baidu.com, api*.tuisong.baidu.com, afd.baidu.com, mobads.baidu.com, issuecdn.baidupcs.com, update.pan.baidu.com, sa*.tuisong.baidu.com, m.baidu.com, sofire.baidu.com, r6.mo.baidu.com, res.mi.baidu.com, mime.baidu.com, mbd.baidu.com, dss0.bdstatic.com, tb1.bdstatic.com, tb2.bdstatic.com, ss0.bdstatic.com, gss0.bdstatic.com, newclient.map.baidu.com, pan.baidu.com, ndstatic.cdn.bcebos.com, staticsns.cdn.bcebos.com, fc-video.cdn.bcebos.com, rp.hpplay.cn, tiebac.baidu.com, appwk.baidu.com, mres.aibank.com, www.banyuetanapp.com, cdnmobibank.bankofbeijing.com.cn, apps.api.ke.com, gateway.shouqiev.com, channel.beitaichufang.com, iapi.bishijie.com, pan-api.bitqiu.com, manga.bilibili.com, i*.hdslb.com, www.binance.info, www.yingwangtech.net, www.binance.com, social.blued.cn, bd-api.kuwo.cn, h5app.kuwo.cn, bodianimgcdn.kuwo.cn, api.boohee.com, bohe.sfo-tx-shanghai-01.saas.sensorsdata.cn, lego.boohee.com, status.boohee.com, api.sfacg.com, lens.leoao.com, res.pizzahut.com.cn, cdn-xyk-app.bankofbeijing.com.cn, grpc.biliapi.net, app.bilibili.com, api.bilibili.com, api.live.bilibili.com, line3-h5-mobile-api.biligame.com, app-gw.csdn.net, gw.csdn.net, api.caijingmobile.com, api3.cls.cn, cn-acs.m.cainiao.com, amdc.m.taobao.com, wrapper.cyapi.cn, api.caiyunapp.com, starplucker.cyapi.cn, gg.caixin.com, ptmpcap.caocaokeji.cn, cap.caocaokeji.cn, fintechappdr.cgws.com, 182.92.244.70, ad.myfriday.cn, ios-api.lucklyworld.com, learn.chaoxing.com, pic1.chelaile.net.cn, api.chelaile.net.cn, atrace.chelaile.net.cn, web.chelaile.net.cn, cdn.*.chelaileapp.cn, gw.chuangkit.com, app.hbooker.com, beta-api.crunchyroll.com, js-ad.ayximgs.com, ap.dongdianqiu.com, se-api.djiits.com, dudian-oss.oss-cn-shenzhen.aliyuncs.com, imagepc.ctaiot.com, delivery-api.imdada.cn, sdk.alibaba.com.ailbaba.me, adservice.sigmob.cn, ssp.dzh.com.cn, e.dangdang.com, api.dangdang.com, mapi.dangdang.com, appdmkj.5idream.net, app.dewu.com, cdn.poizon.com, capis*.didapinche.com, adx-cn.anythinktech.com, www.didapinche.com, pt-starimg.didistatic.com, omgup*.xiaojukeji.com, res.xiaojukeji.com, common.diditaxi.com.cn, hd.xiaojukeji.com, freight.xiaojukeji.com, daijia.kuaidadi.com, ct.xiaojukeji.com, conf.diditaxi.com.cn, as.xiaojukeji.com, img.ddrk.me, ddrk.me, app.95598pay.com, 103.37.155.60, *.dianping.com, img.meituan.net, p.meituan.com, rms.meituan.com, www.dpfile.com, awp-assets.meituan.net, s3plus.meituan.net, p*.meituan.net, ddplus.meituan.net, api.gaoqingdianshi.com, cdn.dianshihome.com, app-v1.ecoliving168.com, img.admobile.top, webcdn.m.qq.com, *.pglstatp-toutiao.com, api.htp.ad-scope.com.cn, appgw.ddpai.com, init.sms.mob.com, apphw.ddpai.com, maicai.api.ddxq.mobi, gw.api.ddxq.mobi, user.api.ddxq.mobi, gw.alicdn.com, img.alicdn.com, dxy.com, dq.dxy.cn, app.ceair.com, api.gamer.com.tw, ump.sz.creditcard.ecitic.com, m.creditcard.ecitic.com, api.douban.com, daoyu.sdo.com, rtbapi.douyucdn.cn, staticlive.douyucdn.cn, capi.douyucdn.cn, douyucdn.cn, elemecdn.com, fuss10.elemecdn.com, cube.elemecdn.com, www1.elecfans.com, nr-op.elemecdn.com, cdn-evone-ceph.echargenet.com, pic.edaijia.cn, static.95508.com, gateway-api.dushu365.com, l*.51fanli.net, *.pangolin-sdk-toutiao.com, *.pangolin-sdk-toutiao.*, *.pstatp.com, *.pstatp.com.*, *.pglstatp-toutiao.com.*, gurd.snssdk.com, gurd.snssdk.com.*, i-lq.snssdk.com, i-lq.snssdk.com.*, *default.ixigua.com, api.flydigi.com, app.flymodem.com.cn, tiku.fenbi.com, fm.fenqile.com, external.fcbox.com, dsp.fcbox.com, consumer.fcbox.com, rtm.fcbox.com, dsa-mfp.fengshows.cn, api.fengshows.com, ecloud.tppension.cntaiping.com, apis.folidaymall.com, api*.futunn.com, app.variflight.com, m*.amap.com, optimus-ads.amap.com, amap-aos-info-nogw.amap.com, mobile.cebbank.com, yghsh.cebbank.com, mps.95508.com, gha.ghac.cn, gsp.gacmotor.com, zone.guiderank-app.com, cdn.133.cn, jt.rsscc.com, jp.rsscc.com, prom.mobile.gome.com.cn, api.gongkaoleida.com, yun.tuitiger.com, mi.gdt.qq.com, open.e.kuaishou.com, pagead2.googlesyndication.com, kano.guahao.cn, app.wy.guahao.com, awg.enmonster.com, aag.enmonster.com, guanyu.longfor.com, mbank.grcbank.com, dl.app.gtja.com, dl*.app.gtja.com, v.icbc.com.cn, pv.elife.icbc.com.cn, elife.icbc.com.cn, fuwu.nhsa.gov.cn, gugongmini.dpm.org.cn, m.prod.app.hsbcfts.com.cn, emisdatacenteraws.hafoo.com, hmbaby.simshine.cn, *.townmalls.cn, www.haixue.com, service.haiersmarthomes.com, gfp.veta.naver.com, api.hanju.koudaibaobao.com, home.umetrip.com, discardrp.umetrip.com, startup.umetrip.com, oss.umetrip.com, m.ibuscloud.com, ads.iconntech.com, smkmp.96225.com, api.haohaozhu.cn, notch.qdaily.com, app3.qdaily.com, open.fitdays.cn, hfapp-service.qweather.net, promote-trx.helipay.com, acs-m.freshippo.com, api.hengdianfilm.com, fbchina.flipchina.cn, api.touker.com, static.creditcard.hxb.com.cn, cmsapi.wifi8.com, cmsfile.wifi8.com, interface.hstong.com, res.hongyibo.com.cn, api4.bybutter.com, appapi.huazhu.com, hweb-hotel.huazhu.com, hweb-manager.huazhu.com, mcsp.cloudpnr.com, saas-ad.cloudpnr.com, api.huomao.com, games.mobileapi.hupu.com, du.hupucdn.com, i*.hoopchina.com.cn, goblin.hupu.com, api-ad-product.huxiu.com, cdn.wup.huya.com, business.msstatic.com, cdnfile1.msstatic.com, live-ads.huya.com, api-one-wscn.awtmt.com, api.wallstreetcn.com, napi.ithome.com, www.i3zh.com, mbank5.jsbchina.cn, cdn.jlbank.com.cn, yunbusiness.ccb.com, g.alicdn.com, waimai-guide.ele.me, api.m.jd.com, dns.jd.com, router-app-api.jdcloud.com, m.360buyimg.com, bdsp-x.jd.com, dsp-x.jd.com, ms.jr.jd.com, appconf.mail.163.com, support.you.163.com, jdread-api.jd.com, www.gcores.com, explorer.tratao.com, *.kakamobi.cn, smart.789.image.mucang.cn, richmanrules.ksedt.com, api.jxedt.com, richmanapi.jxedt.com, img.gdoil.cn, api.tipsoon.com, s.jiediankeji.com, img.jiemian.com, api.sogaha.cn, p*.pstatp.com, jad-api.jin10.com, jiucaigongshe.oss-cn-beijing.aliyuncs.com, dict-mobile.iciba.com, mobile-pic.cache.iciba.com, service.iciba.com, *.kingsoft-office-service.com, api-access.pangolin-sdk-toutiao.com, api.coolapk.com, www.coolapk.com, res.kfc.com.cn, bp-api.bestv.com.cn, bp-api.bestv.cn, api.vistopia.com.cn, open3.vistastory.com, api.gotokeep.com, kad.gotokeep.com, static1.keepcdn.com, pocketuni.net, p.kuaidi100.com, video-dsp.pddpic.com, t-dsp.pinduoduo.com, images.pinduoduo.com, api.kkmh.com, az4-api.ksapisrv.com, az4-api-idc.ksapisrv.com, az2-api.ksapisrv.com, az2-api-idc.ksapisrv.com, apissl.gifshow.com, apissl.ksapisrv.com, az2-api-js.gifshow.com, az2-live.ksapisrv.com, audiobookpay.kuwo.cn, mgxhtj.kuwo.cn, nmobi.kuwo.cn, searchrecterm.kuwo.cn, musicpay.kuwo.cn, vip1.kuwo.cn, www.oschina.net, open-cms-api.uc.cn, open-cms-api.quark.cn, cdn-oss.00bang.cn, api.00bang.cn, mobile.laichon.com, shop.laichon.com, mobile-api.imlaidian.com, api.laifeng.com, gmp.lakala.com, wallet.lakala.com, tk.lanjiyin.com.cn, tagit.hyhuo.com, 118.178.214.118, dapis.mting.info, display.wting.info, ios.lantouzi.com, tbgapplet.carlsberg.asia, dl-cu-hz.lechange.cn, api.club.lenovo.cn, abcapi.lenovoimage.com, api-ac.liepin.com, api-wanda.liepin.com, a.line.me, ad.line-scdn.net, w.line.me, gw.line.naver.jp, lan.line.me, buy.line.me, crs-event.line.me, obs.line-scdn.net, d.line-scdn.net, scdn.line-apps.com, sch.line.me, static.line-scdn.net, nelo2-col.linecorp.com, uts-front.line-apps.com, cix.line-apps.com, legy.line-apps.com, ec-bot-obs.line-scdn.net, app.aa-ab.com, ad.lofter.com, lofter.lf127.net, order-app-api.lbdj.com, plt.yorentown.com, lawsonapi.yorentown.com, www.iyingdi.cn, www.1314zhilv.com, api.internetofcity.cn, www.cmbc.com.cn, rs.creditcard.cmbc.com.cn, dispatcher.camera360.com, mada-travel.17u.cn, ebk.17u.cn, app.api.versa-ai.com, static01.versa-ai.com, qimg.cdnmama.com, mapi.mafengwo.cn, creditcardapp.bankcomm.cn, creditcardapp.bankcomm.com, creditcard.bankcomm.cn, creditcard.bankcomm.com, sfo.mddcloud.com.cn, mob.mddcloud.com.cn, toblog.ctobsnssdk.com, mobads-pre-config.cdn.bcebos.com, sdk1xyajs.data.kuiniuca.com, conf-darwin.xycdn.com, *.ubixioe.com, open.taou.com, h3.open.taou.com, mangaapi.manhuaren.com, *mangaapi.manhuaren.*, *.mgtv.com, app.missevan.com, p0.pipi.cn, api.mcd.cn, api.bevol.com, j-image.missfresh.cn, capi.mwee.cn, mea.meitudata.com, adui.tg.meitu.com, flowplus.meituan.net, cdb.meituan.com, peisongapi.meituan.com, x.seeyouyima.com, axxd.xmseeyouyima.com, config-service.seeyouyima.com, b-api.ins.miaopai.com, ggc.miguvideo.com, public-deliver9.miguvideo.com, display*-sc.miguvideo.com, recommend-dy.miguvideo.com, app-sc.miguvideo.com, common-sc.miguvideo.com, ggx*.miguvideo.com, ggic*.miguvideo.com, home.mi.com, api.mgzf.com, midc.cdn-static.abchina.com.cn, enjoy.cdn-static.abchina.com, 3g.csair.com, blog.nilbt.com, www.nfmovies.com, api.nj.nbtv.cn, gateway.benewtech.cn, ntt-app.benewtech.cn, oxadmin.cp.com.cn, v3.wufazhuce.com, app.api.d3yuiw4.com, api.21ec74.com, slapi.oray.net, supportda.ofo.com, ma.ofo.com, activity2.api.ofo.com, 103.91.210.141, adapi.izuiyou.com, pss.txffp.com, appapi.caiyicloud.com, api.pinduoduo.com, api.yangkeduo.com, mobile.yangkeduo.com, iobs.pingan.com.cn, hcz-member.pingan.com.cn, cdn.sdb.com.cn, pacdn.m.stock.pingan.com, mobile.1qianbao.com, image.spdbccc.com.cn, j1.pupuapi.com, image.pushplus.plus, www.pushplus.plus, lban.spdb.com.cn, wap.spdb.com.cn, adpai.thepaper.cn, access.mypikpak.com, appapi.51job*.com, cupid.51job*.comhostname, adproxy.autohome.com.cn, app2.autoimg.cn, mobile-consumer-sapp.chery.cn, fmapp.chinafamilymart.com.cn, facade-api.black-unique.com, us.l.qq.com, y.gtimg.cn, music.y.qq.com, m.qianbao.qq.com, qidian.qpic.cn, mage.if.qidian.com, magev6.if.qidian.com, webapi.qmai.cn, miniapp.qmai.cn, open.e.kuaishou.cn, api-access.pangolin-sdk-toutiao-b.com, api-access.pangolin-sdk-toutiao1.com, api-cfg.wtzw.com, p1-lm.adukwai.com, lf-cdn-tos.bytescm.com, webcast-open.douyin.com, beta-luna.douyin.com, ether-pack.pangolin-sdk-toutiao.com, api-access.pangolin-sdk-toutiao?.com, sf*-fe-tos.pglstatp-toutiao.com, api.qbb6.com, open.qyer.com, media.qyer.com, a.qiumibao.com, iqushangwang.8quan.com, qde.qunar.com, homefront.qunar.com, client.qunar.com, capi.lkcoffee.com, ecapi.lkcoffee.com, m.lkcoffee.com, img0*.luckincoffeecdn.com, oneapph5.dongfeng-nissan.com.cn, app.peopleapp.com, stat.peopleapp.com, adstatic.peopleapp.com, dyncdn.me, gql.reddit.com, gql-fed.reddit.com, api.rr.tv, cms.daydaycook.com.cn, api.daydaycook.com.cn, app.meruki.cn, app.homeinns.com, api.mos.csvw.com, mapi.sfbest.com, ccsp-egmas.sf-express.com, ucmp.sf-express.com, mcs-mimp-web.sf-express.com, homepage-api.smzdm.com, haojia-api.smzdm.com, app-api.smzdm.com, user-api.smzdm.com, article-api.smzdm.com, qianbao.smzdm.com, s-api.smzdm.com, haojia.m.smzdm.com, api-sams.walmartmobile.cn, apis.lifeweek.com.cn, api.huachenjie.com, ad.shunchangzhixing.com, zlsdk.1rtb.net, api.gameplus.qq.com, ios.sspai.com, editor.sm.cn, ecard.shenzhentong.com, img01.10101111cdn.com, www.ymm56.com, sh-gateway.shihuo.cn, static.shihuocdn.cn, gw-passenger.01zhuanche.com, img.yun.01zhuanche, ut2.shuqistat.com, dsp.toutiao.com, sf3-be-pack.pglstatp-toutiao.com, sq.sljkj.com, ocean.shuqireader.com, img-tailor.11222.cn, message.shuqireader.com, feedback.uc.cn, *.shuqireader.com, 101.91.69.26, service.4gtv.tv, mapi.sichuanair.com, business-cdn.shouji.sogou.com, ios.sogou.com, android.sogou.com, h5api.sginput.qq.com, *.souhu.com, wxs-weixin.sd.zhumanggroup.com, 47.110.187.87, ssp.soulapp.cn, chat-live.soulapp.cn, api-chat.soulapp.cn, api-account.soulapp.cn, api-global.soulapp.me, api-a.soulapp.cn, api-pay.soulapp.cn, gateway-mobile-gray.soulapp.cn, post.soulapp.cn, api-user.soulapp.cn, *-spclient.spotify.com, spclient.wg.spotify.com, api.sodalife.xyz, api.bwton.com, szdmobile.suzhou.gov.cn, mpcs.suning.com, image.suning.com, luckman.suning.com, mrobot.pconline.com.cn, mrobot.pcauto.com.cn, agent-count.pconline.com.cn, ga-album-cdnqn.52tt.com, www.tailgdd.com, alt-r.my.com, imgx.jampp.com, bid.adview.cn, api.taptapdada.com, btrace.qq.com, api2.helper.qq.com, *.beacon.qq.com, lives.l.qq.com, imgcache.qq.com, mtteve.beacon.qq.com, vv.video.qq.com, qt.qq.com, 3gimg.qq.com, splashqqlive.gtimg.com, qzonestyle.gtimg.cn, discuz.gtimg.cn, bla.gtimg.com, mmgr.gtimg.com, bk.bingo.qq.com, static.gameplus.qq.com, 4gimg.map.qq.com, otheve.beacon.qq.com, r.inews.qq.com, news.ssp.qq.com, ccmsupport-sz.tenpay.com, sports3.gtimg.com, images.client.vip.xunlei.com, api-shoulei-ssl.xunlei.com, chl.tf.cn, wechat.tf.cn, cgbank.oss-cn-shenzhen.aliyuncs.com, tfsmy.chengdu.gov.cn, tft-app.cdtft.cn, ams-cdn.cdtft.cn, www.tsytv.com.cn, j5.dfcfw.com, appactive.1234567.com.cn, t1.market.xiaomi.com, api.cloud.189.cn, api.ncarzone.com, ossgw.alicdn.com, zconfig.alibabausercontent.com, *.ly.com, *.17usoft.com, *.17u.cn, mobilehotelapi.elong.com, quic-tcmapi.elong.com, truthsocial.com, *.i18n-pglstatp.com, mkt-gateway.tuhu.cn, cl-gateway.tuhu.cn, gateway.tuhu.cn, m.pvp.xoyo.com, client.tujia.com, m.tuniu.com, adm.10jqka.com.cn, iphone.ac.qq.com, stat.10jqka.com.cn, top-widgets-api.xiaozujian.com, api-marketing.zhinengxiyifang.cn, adsoss.zhinengxiyifang.cn, ads.zhinengxiyifang.cn, pubads.g.doubleclick.net, pagead2.googleadservices.com, app02.vgtime.com, img0*.benlailife.com, qiye.gaoding.com, ipv4.music.163.com, interface.music.163.com, interface3.music.163.com, interface9.music.163.com, god.gameyw.netease.com, app-conf.ds.163.com, kaola-haitao.oss.kaolacdn.com, sp.kaola.com, gw.kaola.com, *.music.126.net, img1.126.net, www.icourse163.org, nex.163.com, g1.163.com, client.mail.163.com, c.m.163.com, interface*.music.163.com, easyreadfs.nosdn.127.net, p.du.163.com, m.you.163.com, yanxuan.nosdn.127.net, dict.youdao.com, api-overmind.youdao.com, cdke.youdao.com, dictvip-business.youdao.com, dsp-impr2.youdao.com, impservice.dictapp.youdao.com, oral.youdao.com, oimage*.ydstatic.com, api.wmpvp.com, snailsleep.net, b.appsimg.com, mapi.appvipshop.com, ios.wps.cn, wanciwangdata.oss-cn-beijing.aliyuncs.com, recite.perfectlingo.com, misc-api-prd-mx.wandafilm.com, osg-static.sgcc.com.cn, osg-service.sgcc.com.cn, mp.weixin.qq.com, weixin110.qq.com, security.wechat.com, api.wfdata.club, overseas.weico.cc, thor.weidian.com, cds.wifi188.com, vue3-api.zhixiny.cn, api.51credit.com, img.wukongtv.com, api-release.wuta-cam.com, res-release.wuta-cam.com, *.pipiapps.com, *.fuliapps.com, *.xiangjiaoapps.com, *.xiangxiangapps.com, m.ctrip.com, ma-adx.ctrip.com, wcprd.hilton.com.cn, file.cibfintech.com, apiwz.midukanshu.com, upload-bbs.mihoyo.com, cstore-en-public-tx.seewo.com, edit.sinaapp.com, app.chinahxzq.com.cn, client-api-v2.oray.com, lchttpapi.xczim.com, pzoap.moedot.net, vapp.tmuyun.com, res1.hubcloud.com.cnhostname, mobileapi.xiamenair.com, acs.m.goofish.com, g-acs.m.goofish.com, info.mina.xiaoaisound.com, marketing-aibox.v.mitvos.com, api.xbxxhz.com, shcss.suning.com, web2.realtech-inc.com, sdk.1rtb.net, gw.xiaocantech.com, smarket.dian.so, file.dian.so, xhtz.oss-cn-guangzhou.aliyuncs.com, mpos-pic.helipay.com, mgesq.api.mgtv.com, *.hitv.com, app-api.niu.com, api.petkit.cn, myusmile.online, wemallh5.usmile.com, www.myusmile.online, api.psy-1.com, lcen.xiaote.net, ad.xiaotucc.com, mapi.xiaotucc.com, portal-portm.meituan.com, mall.meituan.com, xxyx-client-api.xiaoxiaoyouxuan.com, statistic.live.126.net, www.xiaoxiongmeishu.com, spamblocker-api.zeekstudio.com, api.xiaoyi.com, api.xiaoyuzhoufm.com, edith.xiaohongshu.com, www.xiaohongshu.com, ci.xiaohongshu.com, rec.xiaohongshu.com, so.xiaohongshu.com, edith.rnote.com, www.rnote.com, ci.rnote.com, so.rnote.com, rec.rnote.com, api.jr.mi.com, api.m.mi.com, api-miprint.hannto.com, api.indeedpower.com, api-mifit*.huami.com, shopapi.io.mi.com, gslbali.ximalaya.com, search.ximalaya.com, searchwsa.ximalaya.com, mobile.ximalaya.com, mobilehera.ximalaya.com, mobwsa.ximalaya.com, m.ximalaya.com, mwsa.ximalaya.com, app.xinpianchang.com, bgw.xinyue.qq.com, operationapi.fosunhanig.com, api*.sparke.cn, static.xyzq.cn, static.api.m.panda.tv, api.xueqiu.com, open.xueqiu.com, stock.xueqiu.com, 39.103.79.14, 39.106.97.84, 47.95.49.75, 101.201.62.20, 101.201.62.26, 101.201.175.228, 124.250.48.3, 182.92.145.50, 182.92.251.113, portal-xunyou.qingcdn.com, imeclient.openspeech.cn, e-static.aia.com.cn, api2.yaduo.com, www.cntv.cn, cdn.cmgadx.com, mobile-api2011.elong.com, webboot.zhangyue.com, saad.ms.zhangyue.net, app.yinxiang.com, i.ys7.com, oneapp-api.faw-vw.com, www.vgtime.com, *.gamersky.com, service.busi.inke.cn, static.psbc.com, mcc.psbc.com, static.mobile-bank.psbc.com, d.psbc.com, pipi.4kya.com, m.yap.yahoo.com, patient-api.suh.cn, userpms-api.suh.cn, venus.yhd.com, a.sinopecsales.com, ocrifs.ejoy.sinopec.com, api.yikaobang.com.cn, api.17kjs.com, compus.xiaofubao.com, mapi-app.bestpay.com.cn, api.ycapp.yiche.com, cheyouapi.ycapp.yiche.com, ad.ysepay.com, ads.ysepay.com, api.winbull8.com, hz.yxzq.com, api5.youonbike.com, api.yonghuivip.com, new-app-api.ylyk.com, gongdu.youshu.cc, img.dailmo.com, img.allahall.com, app.zhoudamozi.com, *.googlevideo.com, youtubei.googleapis.com, api.ulife.group, acs.youku.com, push.m.youku.com, un-acs.youku.com, *.yuxueyuan.cn, xyst.yuanfudao.com, nnapp.cloudbae.cn, gw3.ykccn.com, restapi.iyunmai.com, m.airchina.com.cn, mlife.jf365.boc.cn, openapi.boc.cn, amemv.com, musical.com, snssdk.com, tiktokv.com, xyz.cnki.net, app.10099.com.cn, wap.bank.ecitic.com, imcs.citicbank.com, ecssmobile.e-chinalife.com, webappcfg.paas.cmbchina.com, mbmodule-openapi.paas.cmbchina.com, marketing.cmschina.com, client.app.coc.10086.cn, app.10086.cn, mcmm.caiyun.feixin.10086.cn, mrp.mcloud.139.com, ad.mcloud.139.com, middle.yun.139.com, cloud.189.cn, zt-app.go189.cn, m.client.10010.com, m1.ad.10010.com, res.mall.10010.cn, e.weather.com.cn, zgrb.epicc.com.cn, apicloud.zol.com.cn, c.zhangle.com, live.inst-service.htsc.com, geetest.htsc.com, 119.29.29.*, djcapp.game.qq.com, quanguo.mygolbs.com, wx.mygolbs.com, ossweb-img.qq.com, mlol.qt.qq.com, mbasecc.bas.cmbchina.com, mbasecc.bcs.cmbchina.com, intellicc.bas.cmbchina.com, intellicc.bcs.cmbchina.com, beehiveapi.58.com, portal.zjzwfw.gov.cn, app-izz.zhengzhou.gov.cn, apio.zhengqi100.com, zua.zhidiantianxia.cn, preprod.cdzghome.com, api.zhihu.com, www.zhihu.com, appcloud2.zhihu.com, m-cloud.zhihu.com, zhuanlan.zhihu.com, link.zhihu.com, direct.z-bank.com, hdgateway.zto.com, minipro.95504.net, sichuan.95504.net, app.badmintoncn.com, fastbuyer.zbj.com, z.onewo.com, app.zhuanzhuan.com, zjdr666.com, ztoread.ziroom.com, api.izuiyou.com, syh.zybang.com, www.zybang.com, ih2.ireader.com, book.img.ireader.com`

- **app2smile QQ News** — 参考上游变化；不自动导入脚本或解密配置

  `hostname = %APPEND% news.ssp.qq.com, r.inews.qq.com`

- **app2smile Tieba** — 参考上游变化；不自动导入脚本或解密配置

  `hostname = %APPEND% tiebac.baidu.com`

- **ddgksf Weibo Ads** — 参考上游变化；不自动导入脚本或解密配置

  `hostname = api.weibo.*, *.api.weibo.*, mapi.weibo.*, *.uve.weibo.com, new.vip.weibo.cn, boot.biz.weibo.com`

## Map Local（800 项待审核）

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http:\/\/.+\.gamersky\.com\/.+\/adSystem\/ad\/.+ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http:\/\/59\.82\.113\.10\/amdc\/mobileDispatch\?appkey=213807& data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http:\/\/ad\.shunchangzhixing\.com\/getAd data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http:\/\/ebk\.17u\.cn\/tctrafficappversionadmin\/api\/getLatestVersionApp data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http:\/\/res1\.hubcloud\.com\.cn data-type=text data=" "`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http?:\/\/.*\.pglstatp-toutiao\.com data-type=text data=" "`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http?:\/\/tianqi\.2345\.com\/api\/content\/getContentFeeds\.php data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^http[s]?:\/\/magev6\.if\.qidian\.com\/argus\/api\/v1\/bookshelf\/refresh data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(?:\w+-spclient|spclient\.wg)\.spotify\.com(?::443)?\/pendragon\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(?:gmp|wallet)\.lakala\.com\/(?:gmp\/openapi\/v2\/resource_space\/getResourceSpace|m\/(?:a\/lama\/mgt\/activity\/biz\/query\/byMerInfo|lama\/mgt\/activity\/(?:bank|biz)\/query\/list)) data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(h3\.)?open\.taou\.com\/maimai\/adshow\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(h3\.)?open\.taou\.com\/maimai\/go_gossip_darwin\/external\/v2\/query_flow_cards\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(h3\.)?open\.taou\.com\/maimai\/pay\/v5\/check_gift\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(live|livewsa)\.ximalaya\.com\/lamia\/v1\/subscribe\/status$ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/app-skin-service\/skin\/setting\/info\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/business-sale-promotion-guide-mobile-web\/popup\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/discovery-feed\/v\d\/scene\/listen\/refresh\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/firework-portal\/v\d+\/sync\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/mobile-playpage\/playpage\/recommendContentV\d\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/mobile-playpage\/playpage\/recommend\/resource\/allocation\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/mobile-user\/v\d\/purchased\/recommend\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/social-web\/follow-stream\/category\/\d+$ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/subscribe\/v\d\/subscribe\/recommend\? data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/subscribe\/v\d\/subscribe\/tagAlbumList$ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(mobile|mobilehera|mobwsa)\.ximalaya\.com\/track-feed\/v\d\/chase\/recommend\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(m|mwsa)\.ximalaya\.com\/community\/square\/v\d\/stream\? data-type=text data="{"data":{"cards":[{"content":{},"type":"RECOMMENDS"}]},"ret":0}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(m|mwsa)\.ximalaya\.com\/x-web-activity\/signIn\/getHomePageSignInInfo\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/(search|searchwsa)\.ximalaya\.com\/hub\/(guideWord|hotWord)V\d\/ data-type=text data="{}" header="Content-Type:application/json"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/a\.line\.me\/er\/l.*\/v\d\/event\/image data-type=tiny-gif`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `^https:\/\/a\.line\.me\/er\/lads\/v\d\/ei\? data-type=tiny-gif`

## Other（3 项待审核）

- **ddgksf Weibo Ads** — 参考上游变化；不自动导入脚本或解密配置

  `host, adstrategy.biz.weibo.com, reject`

- **ddgksf Weibo Ads** — 参考上游变化；不自动导入脚本或解密配置

  `host, sdkapp.uve.weibo.com, direct`

- **ddgksf Weibo Ads** — 参考上游变化；不自动导入脚本或解密配置

  `host-suffix, api.touch-moblie.com, reject`

## RULE-SET（1 项待审核）

- **app2smile Tieba** — 参考上游变化；不自动导入脚本或解密配置

  `RULE-SET,https://raw.githubusercontent.com/app2smile/rules/master/rule/tieba-ad.list,REJECT-DROP`

## Script（344 项待审核）

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `12306 = type=http-request, pattern=^https?:\/\/ad\.12306\.cn\/ad\/ser\/getAdList, script-path=https://raw.githubusercontent.com/kokoryh/Script/master/js/12306.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `51job = type=http-response, pattern=^https?:\/\/cupid\.51job(app)?\.com\/open\/noauth\/recommend\/job-tab-dynamic, script-path=https://raw.githubusercontent.com/zirawell/R-Store/main/Res/Scripts/AntiAd/51job.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `51信用卡管家 = type=http-response, pattern=^https?:\/\/api\.u51\.com\/generic-config-gateway\/api\/v\d\/guanjia\/me-tab2\/config, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/51card.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `51信用卡管家 = type=http-response, pattern=^https?:\/\/api\.u51\.com\/liabilitygateway\/api\/v\d\/homepage\/liabilityline, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/51card.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `555影视广告 = type=http-response, pattern=^https?:\/\/[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+){1,3}(:\d+)?\/api\/v\d\/movie\/index_recommend, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/555Ad.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_foll = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/user\/follow\/users\/mixed\/get, script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_fx = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/link\/page\/discovery\/resource\/show, script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_home = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/(homepage\/block\/page|link\/page\/rcmd\/(resource\/show|block\/resource\/multi\/refresh)), script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20, argument=PRGG="{PRGG}"&PRRK="{PRRK}"&PRDRD="{PRDRD}"&PRSCVPT="{PRSCVPT}"&PRST="{PRST}"&PRRR="{PRRR}"&HMPR="{HMPR}"&PRMST="{PRMST}"&PRCN="{PRCN}"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_mian = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/(batch|v\d\/resource\/comment\/floor\/get), script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_mybarad = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/link\/position\/show\/resource, script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `NetEaseCloudMusic_tab = type=http-response, pattern=^https?:\/\/(ipv4|interface\d?)\.music\.163\.com\/e?api\/link\/home\/framework\/tab, script-path=https://raw.githubusercontent.com/Keywos/rule/main/script/wy/js/wyres.js, requires-body=true, binary-body-mode=true, timeout=20, argument="[{{{MY}}},{{{DT}}},{{{FX}}}]"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Protobuf = type=http-response, pattern=^https:\/\/(?:\w+-spclient|spclient\.wg)\.spotify\.com(?::443)?\/(?:bootstrap|user-customization-service), script-path=https://raw.githubusercontent.com/001ProMax/Surge/refs/heads/main/Script/Spotify.Crack.Dev.js, requires-body=true, binary-body-mode=true, timeout=3, argument="[{{{tab}}},{{{useractivity}}}]"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/app-api\.smzdm\.com\/util\/loading, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/app-api\.smzdm\.com\/util\/update, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/article-api\.smzdm\.com\/publish\/get_bubble, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/haojia-api\.smzdm\.com\/home\/list, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/homepage-api\.smzdm\.com\/v3\/home, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/qianbao\.smzdm\.com\/v\d\/app\/home, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `Smzdm = type=http-response, pattern=^https?:\/\/user-api\.smzdm\.com\/vip\/bottom_card_list, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/smzdm/Smzdm.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `UnblockURLinWeChat-解除微信链接限制 = type=http-response, pattern=^https\:\/\/(weixin110\.qq|security.wechat)\.com\/cgi-bin\/mmspamsupport-bin\/newredirectconfirmcgi\?, script-path=https://raw.githubusercontent.com/zZPiglet/Task/master/asset/UnblockURLinWeChat.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `bilibili.airborne = type=http-request, pattern=^https:\/\/(grpc\.biliapi\.net|app\.bilibili\.com)\/bilibili\.community\.service\.dm\.v1\.DM\/DmSegMobile$, script-path=https://raw.githubusercontent.com/kokoryh/Sparkle/refs/heads/master/dist/bilibili.protobuf.request.js, requires-body=true, binary-body-mode=true, timeout=10, argument=[{{{logLevel}}}]`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `bilibili.live = type=http-response, pattern=^https:\/\/api\.live\.bilibili\.com\/xlive\/(app-interface\/v2\/index\/feed|app-room\/v1\/index\/getInfoBy(Room|User))\?, script-path=https://raw.githubusercontent.com/kokoryh/Sparkle/refs/heads/master/dist/bilibili.json.js, requires-body=true`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `bilibili.protobuf = type=http-response, pattern=^https:\/\/(grpc\.biliapi\.net|app\.bilibili\.com)\/bilibili\.(app\.(show\.v1\.Popular\/Index|dynamic\.v2\.Dynamic\/DynAll|view(unite)?\.v1\.View\/(View|ViewProgress|RelatesFeed)|playurl\.v1\.PlayURL\/PlayView|playerunite\.v1\.Player\/PlayViewUnite)|polymer\.app\.search\.v1\.Search\/SearchAll|community\.service\.dm\.v1\.DM\/DmView|main\.community\.reply\.v1\.Reply\/MainList|pgc\.gateway\.player\.v2\.PlayURL\/PlayView)$, script-path=https://raw.githubusercontent.com/kokoryh/Sparkle/refs/heads/master/dist/bilibili.protobuf.response.js, requires-body=true, binary-body-mode=true, argument="[{displayUpList}, {purifyComment}, {{{sponsorBlock}}}, {{{logLevel}}}]"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `bilibili.request = type=http-request, pattern=^https:\/\/(grpc\.biliapi\.net|app\.bilibili\.com)\/bilibili\.(app\.viewunite\.v1\.View\/View|main\.community\.reply\.v1\.Reply\/MainList)$, script-path=https://raw.githubusercontent.com/kokoryh/Sparkle/refs/heads/master/dist/bilibili.protobuf.request.js, requires-body=true, binary-body-mode=true, timeout=10, argument="[{purifyComment}, {{{logLevel}}}]"`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `blued登录后个人界面广告 = type=http-response, pattern=^https?:\/\/social\.blued\.cn\/users\/.+\/more\/ios\?v=2, script-path=https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/blued.js, requires-body=true, timeout=60`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `http-response ^https:\/\/api\.zhihu\.com\/search\/recommend_query\/v2\? "recommend_queries":\{.+\} "recommend_queries":{}`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `http-response ^https:\/\/grpc\.biliapi\.net\/bilibili\.app\.(interface\.v1\.(Teenagers\/ModeStatus|Search\/DefaultWords)|view\.v1\.View\/TFInfo|viewunite\.v1\.View\/ViewEndPage)$ header-add 'grpc-status' '0'`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `http-response ^https?:\/\/47\.100\.65\.202\/api\/mobile\/index\.php\?version=\d&mobile=yes&module=basicdata&type=forumlist adv fmz200`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `http-response ^https?:\/\/adservice\.sigmob\.cn\/extconfig false true`

- **fmz200-exact-ad-domains** — 脚本、响应处理或 HTTPS 解密范围需要审核

  `http-response ^https?:\/\/api\.m\.jd\.com\/client\.action\?functionId=lite_SmartPush pushData fmz200`

## Script body（4 项待审核）

- **app2smile-bilibili-json** — 上游脚本内容尚未审核；不自动替换本地脚本

  `https://raw.githubusercontent.com/app2smile/rules/master/js/bilibili-json.js`

- **app2smile-bilibili-proto** — 上游脚本内容尚未审核；不自动替换本地脚本

  `https://raw.githubusercontent.com/app2smile/rules/master/js/bilibili-proto.js`

- **zirawell-umetrip-ads** — 上游脚本内容尚未审核；不自动替换本地脚本

  `https://raw.githubusercontent.com/zirawell/R-Store/main/Res/Scripts/AntiAd/umetrip.js`

- **fmz200-taobao-script** — 上游脚本内容尚未审核；不自动替换本地脚本

  `https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/myBlockAds.js`

## URL Rewrite（530 项待审核）

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^(http:\/\/www\.vgtime\.com\/app\/topic\/\d+\.jhtml\?.*?&close_ad=)false(&page=\d&sign=\w+&timestamp=\d+&font_size=\d$) $1true$2 302`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http:\/\/101\.42\.130\.147\/httpdns\/resolve\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http:\/\/106\.55\.220\.18:8053\/httpdns\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http:\/\/139\.196\.12\.179:8053\/httpdns\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http:\/\/54\.222\.159\.138:8053\/httpdns\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http:\/\/x\.seeyouyima\.com\/adx\/staticstics\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^http?:\/\/(discardrp|startup)\.umetrip\.com\/gateway\/api\/umetrip\/native - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/(?:\w+-spclient|spclient\.wg)\.spotify\.com(?::443)?\/artistview\/v1\/artist\/(.*)&platform=iphone https://spclient.wg.spotify.com/artistview/v1/artist/$1&platform=ipad header`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/acs\.m\.goofish\.com\/gw\/mtop\.taobao\.idle\.playboy\.recommend\/1\.0 - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/ad\.line-scdn\.net\/0h - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/api-access\.pangolin-sdk-toutiao\d?\.com\/api\/ad\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/api\.zhihu\.com\/ab\/api\/v1\/products\/zhihu\/platforms\/ios\/config - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/api\.zhihu\.com\/unlimited\/go\/my_card - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/app\.flymodem\.com\.cn\/Appapi\/Public\/welecome - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/axxd\.xmseeyouyima\.com\/ad\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/axxd\.xmseeyouyima\.com\/ad_statistics\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/axxd\.xmseeyouyima\.com\/pregetad\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/axxd\.xmseeyouyima\.com\/v1\/getad\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/buy\.line\.me\/api\/graphql\?variables - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/cix\.line-apps\.com\/R4\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/dl-cu-hz\.lechange\.cn\/oms-online\/advertisementPush - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/dsp\.fcbox\.com\/adSearch\/get\? - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/dudian-oss\.oss-cn-shenzhen\.aliyuncs\.com\/dlabel\/1\/startpage - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/ether-pack\.pangolin-sdk-toutiao\.com\/union\/endcard\/ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/external\.fcbox\.com\/wxgw\/post\/suggestion\/query - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/gae2-spclient\.spotify\.com:443\/ad - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/god\.gameyw\.netease\.com\/v\d\/ad - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/gw\.line\.naver\.jp\/ext\/lgfp\/lad\/v1$ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/gw\.line\.naver\.jp\/lass\/api\/v1\/ads$ - reject`

- **fmz200-exact-ad-domains** — 广告接口路径或动作需要审核

  `^https:\/\/gw\.line\.naver\.jp\/tr\/event$ - reject`

## URL-REGEX（14 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^http:\/\/p\d+-be-pack-sign\.pglstatp-toutiao\.com\/(ad-app-package|web\.business\.image)\/",REJECT`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/a\.line\.me\/cs\/v\d\/oa$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/a\.line\.me\/lass\/api\/v\d\/ads$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/a\.line\.me\/oa\/v\d\/e$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/crs-event\.line\.me\/v\d\/imp",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/obs\.line-scdn\.net\/0h.+\/(o|m)\d+x\d+$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/obs\.line-scdn\.net\/0h.+\/\d+p\.mp4$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/obs\.line-scdn\.net\/0hGH\d",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/scdn\.line-apps\.com\/lan\/document\/pageEvent\/line\/ios\/",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/scdn\.line-apps\.com\/lan\/image\/line\/bannerImageEvent\/",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/sch\.line\.me\/api\/v\d\/ads$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/uts-front\.line-apps\.com\/event$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/uts-front\.line-apps\.com\/settings$",REJECT-DROP`

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `URL-REGEX,"^https:\/\/w\.line\.me\/adp\/api\/ad\/v\d\/",REJECT-DROP`

## USER-AGENT（1 项待审核）

- **fmz200-exact-ad-domains** — 不属于可自动导入的规则类型

  `USER-AGENT,"AVOS*",REJECT`

