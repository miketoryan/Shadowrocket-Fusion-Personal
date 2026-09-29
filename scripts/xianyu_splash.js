// 闲鱼广告链路：清理专属 HTTPDNS，随后只处理已验证的启动广告接口。
(function () {
  const url = String(($request && $request.url) || "");
  const headers = ($request && $request.headers) || {};
  const ua = String(headers["User-Agent"] || headers["user-agent"] || "");
  const body = String(($response && $response.body) || "");

  try {
    if (isAmdc(url, ua)) {
      return $done(cleanAmdc(body));
    }

    const routes = {
      "mtop.taobao.idlecommerce.splash.ads": "2.0",
      "mtop.taobao.idlecommerce.splash.async.ads": "1.0",
      "mtop.idle.idleadv.scene.restore": "1.0",
      "mtop.idle.idleadv.app.launch.report": "1.0"
    };

    const match = /^https:\/\/(?:g-)?acs\.m\.goofish\.com\/gw\/(mtop\.taobao\.idlecommerce\.splash\.(?:async\.)?ads|mtop\.idle\.idleadv\.(?:scene\.restore|app\.launch\.report))\/([\d.]+)\/?(?:\?|$)/.exec(url);
    if (!match || routes[match[1]] !== match[2]) return $done({});

    const api = match[1];

    if (api === "mtop.idle.idleadv.scene.restore") {
      return $done({ body: JSON.stringify({
        api,
        data: { trackParams: { stageMatch: "false" } },
        ret: ["SUCCESS::调用成功"],
        v: "1.0"
      })});
    }

    if (api === "mtop.idle.idleadv.app.launch.report") {
      return $done({ body: JSON.stringify({
        api,
        data: { attributeSuccess: "false" },
        ret: ["SUCCESS::调用成功"],
        v: "1.0"
      })});
    }

    const obj = JSON.parse(body);
    if (!obj || typeof obj !== "object" || Array.isArray(obj) ||
        obj.api !== api || !Array.isArray(obj.ret) ||
        !obj.ret.some(x => typeof x === "string" && x.indexOf("SUCCESS::") === 0) ||
        !obj.data || typeof obj.data !== "object" || Array.isArray(obj.data)) {
      return $done({});
    }

    obj.data.adMap = {};
    if (Object.prototype.hasOwnProperty.call(obj.data, "dspList")) obj.data.dspList = [];
    return $done({ body: JSON.stringify(obj) });
  } catch (_) {
    return $done({});
  }

  function isAmdc(u, agent) {
    return /^http:\/\/(?:amdc\.m\.taobao\.com|(?:\d{1,3}\.){3}\d{1,3})(?::\d+)?\/amdc\/mobileDispatch\?/i.test(u) &&
      /(?:^|[?&])appkey=12431167(?:&|$)/.test(u) &&
      /(?:闲鱼|%E9%97%B2%E9%B1%BC)\//i.test(agent);
  }

  function cleanAmdc(raw) {
    const decoded = decodePayload(raw);
    const payload = decoded.value;
    if (!payload || typeof payload !== "object" || !payload.dns) return {};

    const targets = new Set(["acs.m.goofish.com", "g-acs.m.goofish.com"]);
    let changed = false;

    if (Array.isArray(payload.dns)) {
      const before = payload.dns.length;
      payload.dns = payload.dns.filter(entry => {
        if (!entry || typeof entry !== "object") return true;
        const host = String(entry.host || entry.domain || entry.hostname || "").toLowerCase();
        return !targets.has(host);
      });
      changed = payload.dns.length !== before;
    } else if (typeof payload.dns === "object") {
      for (const key of Object.keys(payload.dns)) {
        if (!targets.has(String(key).toLowerCase())) continue;
        delete payload.dns[key];
        changed = true;
      }
    }

    if (!changed) return {};
    const json = JSON.stringify(payload);
    return { body: decoded.base64 ? toBase64Utf8(json) : json };
  }

  function decodePayload(raw) {
    const t = raw.trim();
    if (t.startsWith("{") || t.startsWith("[")) return { value: JSON.parse(raw), base64: false };
    return { value: JSON.parse(fromBase64Utf8(t)), base64: true };
  }

  function fromBase64Utf8(s) {
    const bin = atob(s);
    let esc = "";
    for (let i = 0; i < bin.length; i++) {
      esc += "%" + bin.charCodeAt(i).toString(16).padStart(2, "0");
    }
    return decodeURIComponent(esc);
  }

  function toBase64Utf8(s) {
    const enc = encodeURIComponent(s).replace(/%([0-9A-F]{2})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
    return btoa(enc);
  }
})();
