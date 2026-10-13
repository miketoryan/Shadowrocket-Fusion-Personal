// 闲鱼：只移除明确标识为广告的信息流区块，保留商品、搜索与账户字段。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    const raw = $response && $response.body;
    if (typeof raw !== "string" || !raw) return $done({});
    const allowed = [
      "mtop.taobao.idlehome.home.nextfresh",
      "mtop.taobao.idle.local.home",
      "mtop.taobao.idle.home.whale.modulet"
    ];
    if (!allowed.some(endpoint => url.includes("/gw/" + endpoint + "/"))) return $done({});
    const body = JSON.parse(raw);
    if (!body || typeof body !== "object" || !body.data || typeof body.data !== "object") return $done({});
    let changed = false;
    function filterSections(container) {
      if (!container || !Array.isArray(container.sections)) return;
      const filtered = container.sections.filter(section => {
        if (!section || typeof section !== "object") return true;
        const marker = section.data && section.data.bizType;
        return marker !== "AD" && section.bizType !== "AD";
      });
      if (filtered.length !== container.sections.length) {
        container.sections = filtered;
        changed = true;
      }
    }
    filterSections(body.data);
    filterSections(body.data.container);
    return $done(changed ? {body: JSON.stringify(body)} : {});
  } catch (_) {
    return $done({});
  }
})();
