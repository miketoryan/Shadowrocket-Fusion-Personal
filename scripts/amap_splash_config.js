// 高德启动图层：清除已知开屏控制字段（不修改地图和导航数据）。
// 证据：2026-11-01 日志 m5.amap.com/ws/shield/frogserver/aocs/updatable/1。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    if (!/^https?:\/\/m\d+\.amap\.com\/ws\/shield\/frogserver\/aocs\/updatable\/1(?:\?|$)/.test(url)) {
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
    // 仅处理上游现有去广告脚本确认的三个启动图层字段。
    const keys = ["SplashScreenControl", "splashscreen", "splashview_config"];
    let changed = 0;
    for (const key of keys) {
      if (!Object.prototype.hasOwnProperty.call(obj.data, key)) continue;
      if (obj.data[key] === null) continue;
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