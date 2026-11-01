// 高德：仅清理启动图层配置中的已知开屏字段。
// 2026-11-01 日志：m5.amap.com/ws/shield/frogserver/aocs/updatable/1。
// 参考 R-Store 的 amap.js 相关 SplashScreenControl 处理方式。
// 不影响导航、路线、POI、收藏、天气或账号功能。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    if (!/^https?:\\/\\/m\\d+\\.amap\\.com\\/ws\\/shield\\/frogserver\\/aocs\\/updatable\\/1(?:\\?|$)/.test(url)) {
      return $done({});
    }
    const raw = $response && $response.body;
    if (typeof raw !== "string" || !raw) {
      console.log("amap_splash_config no_body");
      return $done({});
    }
    const obj = JSON.parse(raw);
    if (!obj || typeof obj !== "object" || !obj.data ||
        typeof obj.data !== "object" || Array.isArray(obj.data)) {
      console.log("amap_splash_config invalid_shape");
      return $done({});
    }
    const keys = ["SplashScreenControl", "splashscreen", "splashview_config"];
    let changed = 0;
    for (const key of keys) {
      if (!Object.prototype.hasOwnProperty.call(obj.data, key)) continue;
      const original = obj.data[key];
      if (original === null) continue;
      obj.data[key] = { status: 1, version: "", value: "" };
      changed++;
    }
    console.log("amap_splash_config splash_fields_cleared=" + changed);
    return $done(changed ? { body: JSON.stringify(obj) } : {});
  } catch (_) {
    console.log("amap_splash_config parse_error");
    return $done({});
  }
})();
