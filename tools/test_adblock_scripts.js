// Offline smoke tests for the three local response scripts.
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");

function apply(file, url, json) {
  const before = JSON.stringify(json);
  let result;
  const context = {
    $request: {url},
    $response: {body: before},
    $done: (value) => { result = value; }
  };
  vm.runInNewContext(fs.readFileSync(file, "utf8"), context, {timeout: 2000});
  assert.ok(result !== undefined, file + " must call $done");
  return result.body ? JSON.parse(result.body) : JSON.parse(before);
}

const jd = "scripts/jd_ads_only.js";
const jdURL = "https://api.m.jd.com/client.action?functionId=start&client=apple";
const origJD = {images: [{url: "ad.jpg"}], showTimesDaily: 9, cart: [101], login: {token: "untouched"}};
const outJD = apply(jd, jdURL, origJD);
assert.equal(outJD.images.length, 0);
assert.equal(outJD.showTimesDaily, 0);
assert.equal(outJD.cart[0], 101);
assert.equal(outJD.login.token, "untouched");
assert.equal(apply(jd, "https://api.m.jd.com/client.action?functionId=checkout", origJD).images.length, 1);

const fish = "scripts/xianyu_feed_ads.js";
const feedURL = "https://acs.m.goofish.com/gw/mtop.taobao.idlehome.home.nextfresh/1.0/";
const origFish = {data: {sections: [{data: {bizType: "AD"}}, {data: {bizType: "PRODUCT", item: 42}}]}, ret: ["SUCCESS"]};
const outFish = apply(fish, feedURL, origFish);
assert.equal(outFish.data.sections.length, 1);
assert.equal(outFish.data.sections[0].data.item, 42);
assert.equal(outFish.ret[0], "SUCCESS");
assert.equal(apply(fish, "https://acs.m.goofish.com/gw/mtop.trade.order.create/1.0/", origFish).data.sections.length, 2);

const bili = "scripts/bilibili_splash_cache.js";
const origBili = {data: {show: {item: 1}, list: [{image: "ad"}], max_time: 7, min_interval: 0, pull_interval: 0}, status: 200};
const outBili = apply(bili, "https://app.bilibili.com/x/v2/splash/list?x=1", origBili);
assert.equal(Object.prototype.hasOwnProperty.call(outBili.data, "show"), false);
assert.equal(outBili.data.list.length, 0);
assert.equal(outBili.data.max_time, 0);
assert.equal(outBili.data.pull_interval, 31536000);
assert.equal(outBili.status, 200);
assert.ok(Object.prototype.hasOwnProperty.call(apply(bili, "https://app.bilibili.com/x/v2/feed/index", origBili).data, "show"));

console.log("Ad response regression tests passed (JD/Goofish/Bilibili).");
