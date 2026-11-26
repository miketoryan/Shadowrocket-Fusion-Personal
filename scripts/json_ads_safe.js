// 有限处理已知广告字段；解析失败或未发现字段时保留原响应。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    const body = $response && $response.body;
    if (typeof body !== "string" || !body) return $done({});
    const obj = JSON.parse(body);
    let changed = false;
    const bili = /^https?:\/\/app\.bilibili\.com\/x\/v2\/feed\/index(?:\?|$)/.test(url);
    const allowed = /^https?:\/\/(?:api\.douban\.com|api\.xiaoyuzhoufm\.com|home\.umetrip\.com)(?:\/|$)/.test(url);
    if (!bili && !allowed) return $done({});
    function walk(node, depth) {
      if (!node || typeof node !== "object" || depth > 30) return;
      if (Array.isArray(node)) {
        if (bili) {
          for (let i = node.length - 1; i >= 0; i--) {
            const item = node[i];
            if (item && typeof item === "object" && item.card_type === "ad") { node.splice(i, 1); changed = true; }
          }
        }
        for (const item of node) walk(item, depth + 1);
        return;
      }
      for (const key of Object.keys(node)) {
        const value = node[key];
        if (allowed && ["ads", "advertise"].includes(key) && Array.isArray(value) && value.length) { node[key] = []; changed = true; }
        else if (allowed && ["ad_info", "adInfo", "splash_ad", "advertise"].includes(key) && value && typeof value === "object" && !Array.isArray(value) && Object.keys(value).length) { node[key] = {}; changed = true; }
        else walk(value, depth + 1);
      }
    }
    // B站首页推荐只处理 data.items，不递归删除嵌套业务数据。
    if (bili) {
      const data = obj && obj.data;
      if (data && Array.isArray(data.items)) {
        const kept = data.items.filter(item => {
          if (!item || typeof item !== "object") return true;
          const kind = typeof item.card_goto === "string" ? item.card_goto.toLowerCase() : "";
          return item.card_type !== "ad" && item.is_ad !== true &&
            !/^ad(?:$|_|-)/.test(kind) && !/^vertical_ad(?:$|_)/.test(kind);
        });
        if (kept.length !== data.items.length) { data.items = kept; changed = true; }
        for (const item of kept) {
          if (!item || !Array.isArray(item.banner_item)) continue;
          const banners = item.banner_item.filter(x => !(x && typeof x === "object" && x.type === "ad"));
          if (banners.length !== item.banner_item.length) { item.banner_item = banners; changed = true; }
        }
      }
    } else walk(obj, 0);
    return $done(changed ? {body: JSON.stringify(obj)} : {});
  } catch (_) { return $done({}); }
})();
