// 住这儿广告接口：保持 HTTP 200 与原 JSON 结构，仅返回空广告列表。
// 日志实证原响应结构：{"code":200,"message":"成功","result":{"data":[...]}}
const body = JSON.stringify({
  code: 200,
  message: "成功",
  result: { data: [] }
});
$done({ body });
