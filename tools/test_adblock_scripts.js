// Offline response regressions; these do not emulate the phone's local cache.
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
assert.equal(outBili.data.pull_interval, 0);
assert.equal(outBili.status, 200);
assert.ok(Object.prototype.hasOwnProperty.call(apply(bili, "https://app.bilibili.com/x/v2/feed/index", origBili).data, "show"));

// Entire dedicated ad responses must be empty, even when the server changes shape.
for (const endpoint of ["list", "show", "brand/list", "event/list2"]) {
  for (const data of [
    {list: {show: [{image: "ad"}], preload: [{video: "ad"}]}},
    {new_payload: {campaign: {creative: "ad"}}, pull_interval: 31536000},
    [{image: "ad"}], null
  ]) {
    const url = "https://app.bilibili.com/x/v2/splash/" + endpoint + "?build=91800100";
    const result = apply(bili, url, {code: 0, data});
    assert.equal(result.code, 0);
    assert.equal(result.data.list.length, 0);
    assert.equal(result.data.pull_interval, 0);
    assert.equal(JSON.stringify(result).includes('"ad"'), false, endpoint + " leaked a creative");
  }
}
// Match only the four dedicated splash URLs, not lookalike paths or unrelated hosts.
for (const url of [
  "https://app.bilibili.com/x/v2/feed/index",
  "https://app.bilibili.com/x/v2/splash/listen",
  "https://example.com/x/v2/splash/list"
]) assert.deepEqual(apply(bili, url, origBili), origBili);

for (const raw of ["", "not-json", "null", "[]"]) {
  let output;
  vm.runInNewContext(fs.readFileSync(bili, "utf8"), {
    $request: {url: "https://app.bilibili.com/x/v2/splash/show"},
    $response: {body: raw},
    $done: value => { output = value; }
  }, {timeout: 2000});
  assert.equal(JSON.parse(output.body).code, 0);
  assert.equal(JSON.parse(output.body).data.list.length, 0);
}

console.log("Ad response regression tests passed (JD/Goofish/Bilibili).");



const safe = "scripts/json_ads_safe.js";
const doub = {splash_ad: {image: {url: "ad"}, id: 1}, normal: {id: 7}};
const dout = apply(safe, "https://api.douban.com/v2/feed", doub);
assert.deepEqual(dout.splash_ad, {}); assert.equal(dout.normal.id, 7);
const feed = {data:{items:[{id:1},{card_type:"ad",id:2}]}};
assert.equal(apply(safe, "https://app.bilibili.com/x/v2/feed/index?x=1", feed).data.items.length,1);
const amap = {data:{SplashScreenControl:{value:"ad"}, map:{value:42}}, code:0};
const amapout = apply("scripts/amap_splash_config.js", "https://m5.amap.com/ws/shield/frogserver/aocs/updatable/1?x=1", amap);
assert.equal(amapout.data.SplashScreenControl.value, ""); assert.equal(amapout.data.map.value,42);
const xyurl = "https://acs.m.goofish.com/gw/mtop.taobao.idlecommerce.splash.ads/2.0/";
const xy = {api:"mtop.taobao.idlecommerce.splash.ads",ret:["SUCCESS::调用成功"],data:{adMap:{a:1},cacheAd:[{id:9}],normal:{id:4}}};
const xyout=apply("scripts/xianyu_splash.js",xyurl,xy);
assert.deepEqual(xyout.data.adMap,{}); assert.equal(xyout.data.cacheAd.length,0); assert.equal(xyout.data.normal.id,4);
assert.deepEqual(apply("scripts/xianyu_splash.js",xyurl,{...xy,ret:["FAIL"]}),{...xy,ret:["FAIL"]});
assert.equal(apply(jd,"https://api.m.jd.com/client.action?client=apple&functionId=start",origJD).images.length,0);

// B站首页仅移除明确广告卡和广告横幅，保留普通内容与嵌套数据。
const biliFeed = {data:{items:[{id:1,card_type:'small_cover',nested:{is_ad:true}},{id:2,card_goto:'ad_web'},{id:3,is_ad:true},{id:4,card_type:'banner_v8',banner_item:[{type:'ad',id:'a'},{type:'normal',id:'b'}]}]}};
const feedClean=apply(safe,'https://app.bilibili.com/x/v2/feed/index?x=1',biliFeed);
assert.deepEqual(feedClean.data.items.map(x=>x.id),[1,4]);
assert.equal(feedClean.data.items[0].nested.is_ad,true);
assert.deepEqual(feedClean.data.items[1].banner_item,[{type:'normal',id:'b'}]);
assert.deepEqual(apply(safe,'https://app.bilibili.com/x/v2/feed/index/story?x=1',biliFeed),biliFeed);

function applyHtml(url,body) {
 let result; vm.runInNewContext(fs.readFileSync('scripts/wechat_article_ads.js','utf8'), {
   $request:{url},$response:{body},$done:x=>{result=x;}
 }, {timeout:2000});
 assert.ok(result !== undefined);return result.body === undefined ? body : result.body;
}
const article='<html><script>const t="<div id=\'js_bottom_ad_area\'>";</script><div id="main">正文<div>嵌套内容</div></div><div id="js_bottom_ad_area"><div>广告</div><div>第二层<div>嵌套</div></div></div><div id="related">推荐文章</div></html>';
const wx=applyHtml('https://mp.weixin.qq.com/s?__biz=test',article);
assert.ok(wx.includes('正文<div>嵌套内容</div>'));assert.ok(wx.includes('推荐文章'));assert.ok(!wx.includes('第二层'));
assert.equal(applyHtml('https://mp.weixin.qq.com/s?x=1','<div data-id="js_bottom_ad_area">正文</div>'),'<div data-id="js_bottom_ad_area">正文</div>');
assert.equal(applyHtml('https://mp.weixin.qq.com/s?x=1','<div id="js_bottom_ad_area"><div>正文'),'<div id="js_bottom_ad_area"><div>正文');
assert.equal(applyHtml('https://example.com/s?x=1',article),article);
