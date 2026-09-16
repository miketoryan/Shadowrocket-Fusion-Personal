/* Baidu Netdisk ads-only cleanup. Never changes membership or SVIP fields. */
if (!$response.body) {
  $done({});
} else {
  const body = JSON.parse($response.body);
  const adSwitches = [
    "bdnc_commerce_video_ad_area_pad",
    "business_ad_config_area",
    "enterprise_banner_area",
    "enterprise_bottom_banner",
    "home_card_area",
    "new_user_card",
    "public_guide_config",
    "public_home_config",
    "push_active_area",
    "splash_advertise_fetch_config_area",
    "splash_advertise_type_area",
    "thrid_ad_buads_service",
    "thrid_ad_funads_service",
    "universal_card_area"
  ];

  for (const key of adSwitches) {
    const list = body?.[key]?.cfg_list;
    if (!Array.isArray(list)) continue;
    for (const item of list) {
      if (Object.prototype.hasOwnProperty.call(item, "switch")) item.switch = "0";
      if (Object.prototype.hasOwnProperty.call(item, "open")) item.open = "0";
    }
  }

  $done({body: JSON.stringify(body)});
}
