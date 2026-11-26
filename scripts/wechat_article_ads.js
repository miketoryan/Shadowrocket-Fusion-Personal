// 仅移除公众号文章已知的 js_bottom_ad_area 容器；遇到模糊结构保持原文。
(function () {
  try {
    const url = String(($request && $request.url) || ""), body = $response && $response.body;
    if (!/^https?:\/\/mp\.weixin\.qq\.com\/s(?:\?|$)/.test(url) || typeof body !== "string") return $done({});
    const tokens = /<!--[\s\S]*?-->|<(script|style|textarea)\b(?:[^>"']|"[^"]*"|'[^']*')*>[\s\S]*?<\/\1\s*>|<\/?div\b(?:[^>"']|"[^"]*"|'[^']*')*>/gi;
    const attrs = /\s+([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
    let match, start = -1, depth = 0, end = -1;
    while ((match = tokens.exec(body))) {
      const tag = match[0];
      if (/^<!--|^<(?:script|style|textarea)\b/i.test(tag)) continue;
      if (start < 0 && !/^<\/div/i.test(tag)) {
        let a, id = null; attrs.lastIndex = 4;
        while ((a = attrs.exec(tag))) if (a[1].toLowerCase() === "id") { if (id !== null) return $done({}); id = a[2] ?? a[3] ?? a[4] ?? ""; }
        if (id === "js_bottom_ad_area") { start = match.index; depth = 1; }
      } else if (start >= 0) {
        if (/^<\/div\b/i.test(tag)) depth--;
        else if (!/\/\s*>$/.test(tag)) depth++;
        if (depth === 0) { end = tokens.lastIndex; break; }
      }
    }
    if (start < 0 || end < 0) return $done({});
    return $done({body: body.slice(0, start) + body.slice(end)});
  } catch (_) { return $done({}); }
})();
