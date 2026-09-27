// 闲鱼开屏广告：只处理已验证的启动广告接口，保留正常 MTOP 响应结构。
(function () {
  const url = ($request && $request.url) || "";
  const body = ($response && $response.body) || "";

  const routes = {
    "mtop.taobao.idlecommerce.splash.ads": "2.0",
    "mtop.taobao.idlecommerce.splash.async.ads": "1.0",
    "mtop.idle.idleadv.scene.restore": "1.0",
    "mtop.idle.idleadv.app.launch.report": "1.0"
  };

  try {
    const match = /^https:\/\/(?:g-)?acs\.m\.goofish\.com\/gw\/(mtop\.taobao\.idlecommerce\.splash\.(?:async\.)?ads|mtop\.idle\.idleadv\.(?:scene\.restore|app\.launch\.report))\/([\d.]+)\/?(?:\?|$)/.exec(url);
    if (!match || routes[match[1]] !== match[2]) return $done({});

    const api = match[1];

    if (api === "mtop.idle.idleadv.scene.restore") {
      return $done({
        body: JSON.stringify({
          api,
          data: { trackParams: { stageMatch: "false" } },
          ret: ["SUCCESS::调用成功"],
          v: "1.0"
        })
      });
    }

    if (api === "mtop.idle.idleadv.app.launch.report") {
      return $done({
        body: JSON.stringify({
          api,
          data: { attributeSuccess: "false" },
          ret: ["SUCCESS::调用成功"],
          v: "1.0"
        })
      });
    }

    const obj = JSON.parse(body);
    if (!obj || typeof obj !== "object" || Array.isArray(obj) ||
        obj.api !== api || !Array.isArray(obj.ret) ||
        !obj.ret.some(x => typeof x === "string" && x.indexOf("SUCCESS::") === 0) ||
        !obj.data || typeof obj.data !== "object" || Array.isArray(obj.data)) {
      return $done({});
    }

    // 不直接 reject：保留成功响应，只清空开屏广告字段，减少重试/备用广告链路。
    obj.data.adMap = {};
    if (Object.prototype.hasOwnProperty.call(obj.data, "dspList")) obj.data.dspList = [];

    return $done({ body: JSON.stringify(obj) });
  } catch (_) {
    // 返回结构异常时保持原样，避免影响闲鱼正常业务。
    return $done({});
  }
})();
