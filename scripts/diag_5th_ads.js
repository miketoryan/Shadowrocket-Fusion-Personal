// Temporary diagnostic script for 住这儿 ad API.
// Logs the real response so we can learn the exact success/empty-data schema.
// It does not modify the response.

const url = ($request && $request.url) ? $request.url : "";
const status = ($response && ($response.statusCode || $response.status)) || "";
const headers = ($response && $response.headers) || {};
const contentType = headers["Content-Type"] || headers["content-type"] || "";
let body = ($response && $response.body) || "";

// Keep PacketTunnel logs readable while preserving enough structure for diagnosis.
if (body.length > 12000) body = body.slice(0, 12000) + "...[truncated]";
console.log(`[DIAG_5TH_ADS] url=${url} status=${status} content-type=${contentType} body=${body}`);

$done({});
