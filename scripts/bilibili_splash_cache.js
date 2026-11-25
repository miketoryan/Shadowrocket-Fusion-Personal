// Dedicated Bilibili splash endpoints contain startup ads only.
// Replace the complete ad payload so unfamiliar nested fields cannot retain creatives.
(function () {
  try {
    const url = String(($request && $request.url) || "");
    if (!/^https?:\/\/app\.bilibili\.com\/x\/v2\/splash\/(?:list|show|brand\/list|event\/list2)(?:\?|$)/.test(url)) return $done({});
    let obj;
    try {
      obj = JSON.parse(($response && $response.body) || "{}");
    } catch (_) {
      obj = {};
    }
    if (!obj || typeof obj !== "object" || Array.isArray(obj)) obj = {};
    obj.code = 0;
    obj.message = "0";
    obj.data = {list: [], max_time: 0, min_interval: 0, pull_interval: 0};
    // Do not tell the app to retain its previous splash configuration for a year.
    console.log("bili_splash_empty v20261125 " + url.split("?")[0]);
    return $done({body: JSON.stringify(obj)});
  } catch (_) {
    return $done({});
  }
})();

