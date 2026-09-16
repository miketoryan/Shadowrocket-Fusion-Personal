# Interface source maintenance

> `SYNCED` sources passed repository, section and unlock-risk checks. `BLOCKED` sources do not modify the module.

## Safe auto-sync

| App/source | State | Detail | URL |
|---|---|---|---|
| QQ News / app2smile | **SYNCED** | 1 lines; 0 new MITM hosts; sha256 dbc36baa324c | https://raw.githubusercontent.com/app2smile/rules/master/module/qqnews.sgmodule |
| Tieba / app2smile | **SYNCED** | 3 lines; 0 new MITM hosts; sha256 7c7f1752ff2e | https://raw.githubusercontent.com/app2smile/rules/master/module/tieba.sgmodule |

## Report-only watch

> `CHANGED` means a watched source changed. It is never auto-merged.

| App/source | State | HTTP | Last commit | URL | Note |
|---|---|---:|---|---|---|
| fmz200 Shadowrocket ad collection | **unchanged** | 206 | 2026-09-10 | https://raw.githubusercontent.com/fmz200/wool_scripts/main/Shadowrocket/module/blockAds.srmodule | Report only. Whole-file auto-merge is forbidden because it mixes ad removal with unlock/crack content. |
| ddgksf Weibo Ads | **unchanged** | 206 | 2025-12-12 | https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/WeiboAds.conf | Report only. Quantumult X format requires conversion and review. |
| ddgksf Cainiao Ads | **unchanged** | 206 | 2025-12-12 | https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/AdBlock/CainiaoAds.conf | Report only. Quantumult X format requires conversion and review. |
