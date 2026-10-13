// B站开屏与本地缓存预防：仅修改 splash 响应，不触碰视频、登录或封面。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    if (!/^https?:\/\/app\.bilibili\.com\/x\/v2\/splash\/(?:list|show)(?:\?|$)/.test(url)) return $done({});
    const raw = $response && $response.body;
    if (typeof raw !== "string" || !raw) return $done({});
    const obj = JSON.parse(raw);
    if (!obj || !obj.data || typeof obj.data !== "object") return $done({});
    let changed = false;
    if (Array.isArray(obj.data.show) && obj.data.show.length) {
      obj.data.show = [];
      changed = true;
    }
    if (Array.isArray(obj.data.list)) {
      if (obj.data.list.length) {
        obj.data.list = [];
        changed = true;
      }
    } else if (obj.data.list && typeof obj.data.list === "object" && Array.isArray(obj.data.list.show) && obj.data.list.show.length) {
      obj.data.list.show = [];
      changed = true;
    }
    // Prevent previously delivered start-screen creatives being repeatedly preloaded.
    if (changed) {
      if (typeof obj.data.max_time === "number") obj.data.max_time = 0;
      if (typeof obj.data.pull_interval === "number") obj.data.pull_interval = 31536000;
      if (typeof obj.data.min_interval === "number") obj.data.min_interval = 31536000;
    }
    return $done(changed ? {body: JSON.stringify(obj)} : {});
  } catch (_) {
    return $done({});
  }
})();
