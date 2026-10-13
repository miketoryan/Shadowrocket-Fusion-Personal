// 京东：保留正常购物、订单、登录和商品数据，只清理已知广告字段。
(function () {
  try {
    const url = String(($request && $request.url) || "");
    const raw = $response && $response.body;
    const m = /[?&]functionId=(start|welcomeHome|personinfoBusiness|myOrderInfo)(?:&|$)/.exec(url);
    if (!m || typeof raw !== "string" || !raw) return $done({});
    const data = JSON.parse(raw);
    if (!data || typeof data !== "object" || Array.isArray(data)) return $done({});
    let changed = false;
    const fn = m[1];

    if (fn === "start") {
      if (Array.isArray(data.images) && data.images.length) {
        data.images = [];
        changed = true;
      }
      if (typeof data.showTimesDaily === "number" && data.showTimesDaily !== 0) {
        data.showTimesDaily = 0;
        changed = true;
      }
    } else if (fn === "welcomeHome") {
      if (Array.isArray(data.floorList)) {
        const adTypes = new Set(["bottomXview", "float", "photoCeiling", "tabBarAtmosphere"]);
        const kept = data.floorList.filter(x => !(x && adTypes.has(x.type)));
        if (kept.length !== data.floorList.length) {
          data.floorList = kept;
          changed = true;
        }
      }
    } else if (fn === "personinfoBusiness") {
      for (const floors of [data.floors, data.others && data.others.floors]) {
        if (!Array.isArray(floors)) continue;
        for (const floor of floors) {
          if (!floor || floor.mId !== "basefloorinfo" || !floor.data) continue;
          for (const key of ["commonPopup", "commonPopup_dynamic", "floatLayer"]) {
            if (Object.prototype.hasOwnProperty.call(floor.data, key)) {
              delete floor.data[key];
              changed = true;
            }
          }
        }
      }
    } else if (fn === "myOrderInfo") {
      if (Array.isArray(data.floors)) {
        const kept = data.floors.filter(x => !(x && x.mId === "bannerFloor"));
        if (kept.length !== data.floors.length) {
          data.floors = kept;
          changed = true;
        }
      }
    }
    return $done(changed ? {body: JSON.stringify(data)} : {});
  } catch (_) {
    return $done({});
  }
})();
