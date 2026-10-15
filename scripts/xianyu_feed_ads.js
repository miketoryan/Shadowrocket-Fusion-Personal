// 闲鱼：只移除明确标识为广告的信息流区块，保留商品、搜索与账户字段。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    const raw = $response && $response.body;
    if (typeof raw !== "string" || !raw) return $done({});
    const allowed = [
      "mtop.taobao.idlehome.home.nextfresh",
      "mtop.taobao.idle.local.home",
      "mtop.taobao.idle.home.whale.modulet",
      "mtop.taobao.idlemtopsearch.search"
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

    // 闲鱼搜索广告与普通商品混排：只删除有明确广告标记的卡片。
    if (url.includes("/gw/mtop.taobao.idlemtopsearch.search/") &&
        Array.isArray(body.data.resultList)) {
      const adLabels = /^(?:ad|ads|advert|advertisement|promotion|sponsored)$/i;
      const filtered = body.data.resultList.filter(item => {
        if (!item || typeof item !== "object") return true;
        const data = item.data && typeof item.data === "object" ? item.data : {};
        const args = data.item && data.item.main &&
          data.item.main.clickParam && data.item.main.clickParam.args;
        const markers = [item.bizType, data.bizType, args && args.item_type];
        return !markers.some(v => typeof v === "string" && adLabels.test(v.trim()));
      });
      if (filtered.length !== body.data.resultList.length) {
        body.data.resultList = filtered;
        changed = true;
      }
    }

    return $done(changed ? {body: JSON.stringify(body)} : {});
  } catch (_) {
    return $done({});
  }
})();
