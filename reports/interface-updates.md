# Upstream sources and ad-interface review (2026-10-13)

## Active module integration

- **fmz200/wool_scripts** exact ad domains: used by the new `safe-sync.yml`; filtered only to precise `DOMAIN,REJECT` patterns with `safe_ad_domain()` and source size/count guards. First daily sync imported 10 new ad-only domains. Does not auto-import scripts or MITM.
- **JD**: reviewed fmz200 JD module and zirawell JD cleanup logic; implemented local `scripts/jd_ads_only.js` with narrower scope.
- **China Unicom**: reviewed fmz200 and letswish; imported only targeted ad API paths, excluding account and configuration endpoints.
- **Goofish**: reviewed fmz200/zirawell; implemented local `scripts/xianyu_feed_ads.js` with only explicit ad-marker filtering; preserved existing narrow splash script.
- **Bilibili cached splash**: reviewed blackmatrix7 startup approach and former app2smile script; implemented local `scripts/bilibili_splash_cache.js` preserving splash-data removal while handling preload intervals.

## Previously audited sources (historical record)

The former controlled updater report (438 exact → 83 safe, pinned Bilibili JSON/proto, umetrip, baidupan) describes `tools/fusion.py`, which is no longer invoked by the CI workflow because its legacy schema does not match the current published module. Keep the old code for reference only; `Module.sgmodule` and `reports/status.md` are authoritative.

## Protection

Daily safe sync never imports broad `DOMAIN-SUFFIX`, scripts, HTTPS interception lists, rewrite code, Apple routing, YouTube rewriting, or private credentials. Validation runs before any publication. A successful offline check does not prove ads are absent from an App's already existing local cache.
