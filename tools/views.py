import math
import re
import time
import unicodedata
import requests

from django.http import JsonResponse
from django.db.models import Q
from django.core.cache import cache

from gis_store.models import Store


# ============================================================
# CONFIG
# ============================================================
ALIASES = {
    "CIRCLEK": ["CIRCLEK", "CIRCLE K", "CIRCLE_K", "CIRCLE-K"],
    "GS25": ["GS25", "GS 25"],
}

# Fallback center: TP.HCM
DEFAULT_CENTER = (10.7769, 106.7009)

VN_COUNTRY_CODE = "vn"
CACHE_TTL = 60 * 60 * 24  # 24h
NONE_SENTINEL = "__NONE__"

# Nominatim policy friendly (đổi email thật của bạn)
CONTACT_EMAIL = "student@example.com"

# Retry nhẹ nếu mạng chập chờn / rate limit
NOMINATIM_RETRIES = 2
NOMINATIM_TIMEOUT = 12


# ============================================================
# BASIC HELPERS
# ============================================================
def _headers():
    # Nominatim khuyến nghị User-Agent có contact
    return {
        "User-Agent": f"webgis_project/1.0 (student project; contact: {CONTACT_EMAIL})",
        "Accept-Language": "vi,en;q=0.8",
        "Referer": "http://127.0.0.1:8000/",
    }


def _cache_get(key):
    return cache.get(key)


def _cache_set(key, value, seconds=CACHE_TTL):
    cache.set(key, value, seconds)


def _strip_accents(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", s)


def _normalize_brand(raw: str) -> str:
    b = (raw or "").strip().upper()
    if b in ALIASES:
        return b
    for key, arr in ALIASES.items():
        if b in [x.upper() for x in arr]:
            return key
    return ""


def _brand_q(brand_key: str):
    q = Q()
    for b in ALIASES.get(brand_key, []):
        q |= Q(brand__iexact=b)
    return q


def _parse_latlon(text: str):
    """
    Accept:
      "10.7,106.6"
      "10.7 106.6"
      "10.7;106.6"
      "Lat: 10.7 Lon: 106.6"
    """
    if not text:
        return None
    t = text.strip()

    m = re.search(
        r"(?i)\blat(?:itude)?\b\D*(-?\d+(?:\.\d+)?)\D+"
        r"\blon(?:gitude)?\b\D*(-?\d+(?:\.\d+)?)",
        t
    )
    if m:
        lat = float(m.group(1))
        lon = float(m.group(2))
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon

    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*[,; ]\s*(-?\d+(?:\.\d+)?)\s*$", t)
    if not m:
        return None
    lat = float(m.group(1))
    lon = float(m.group(2))
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return lat, lon
    return None


def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def _bbox_filter(qs, lat, lon, radius_km):
    dlat = radius_km / 111.0
    dlon = radius_km / (111.0 * max(math.cos(math.radians(lat)), 1e-6))
    return qs.filter(
        latitude__gte=lat - dlat, latitude__lte=lat + dlat,
        longitude__gte=lon - dlon, longitude__lte=lon + dlon
    )


def _store_dict(s: Store, extra=None):
    d = {
        "id": s.id,
        "name": s.name,
        "brand": s.brand,
        "address_db": getattr(s, "address", "") or "",
        "lat": float(s.latitude),
        "lon": float(s.longitude),
    }
    if extra:
        d.update(extra)
    return d


def _suggest_next_km(km: float):
    steps = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
    for s in steps:
        if km < s:
            return s
    return None


# ============================================================
# NORMALIZE USER INPUT (chịu nhiều kiểu nhập)
# ============================================================
def _normalize_raw_query(raw: str) -> str:
    if not raw:
        return ""

    # join multi-lines
    parts = [x.strip() for x in raw.splitlines() if x.strip()]
    q = ", ".join(parts) if parts else raw.strip()
    q = re.sub(r"\s+", " ", q).strip()

    # remove leading brand words
    q = re.sub(r"(?i)^\s*(circle\s*k|circlek|gs25)\s+", "", q).strip()
    q = re.sub(r"(?i)\b(tìm|search|near|gần)\b", "", q).strip()

    # unify abbreviations
    q = re.sub(r"(?i)\bTP\.\b", "TP", q)
    q = re.sub(r"(?i)\bQ\.\b", "Q", q)
    q = re.sub(r"(?i)\bP\.\b", "P", q)

    # English style: F13 / D4
    q = re.sub(r"(?i)\bF\s*(\d+)\b", r"Phường \1", q)
    q = re.sub(r"(?i)\bD\s*(\d+)\b", r"Quận \1", q)

    # VN short: Q4 / P13
    q = re.sub(r"(?i)\bQ\s*(\d+)\b", r"Quận \1", q)
    q = re.sub(r"(?i)\bP\s*(\d+)\b", r"Phường \1", q)

    # District/Ward words
    q = re.sub(r"(?i)\bDistrict\s*(\d+)\b", r"Quận \1", q)
    q = re.sub(r"(?i)\bWard\s*(\d+)\b", r"Phường \1", q)

    # clean commas
    q = re.sub(r"\s*,\s*", ", ", q)
    q = re.sub(r"(, )+", ", ", q).strip(" ,")

    return q


def _ensure_hcm_vn(q: str) -> str:
    """
    Nếu có Quận/Phường mà thiếu TP.HCM thì thêm TP.HCM.
    Nếu thiếu Việt Nam thì thêm Việt Nam.
    Xử lý "..., TP" ở cuối.
    """
    if not q:
        return ""

    # "TP" at end => assume HCM (vì project của bạn đang ở HCM)
    q = re.sub(r"(?i)\bTP\b\.?$", "Thành phố Hồ Chí Minh", q).strip()

    low = q.lower()
    has_vn = ("việt nam" in low) or ("vietnam" in low)
    has_hcm = ("hồ chí minh" in low) or ("ho chi minh" in low) or ("hcm" in low) or ("hcmc" in low)
    has_district = bool(re.search(r"(?i)\bquận\s*\d+\b", q))

    # map hcm forms -> chuẩn
    q = re.sub(r"(?i)\bTP\s*HCM\b", "Thành phố Hồ Chí Minh", q)
    q = re.sub(r"(?i)\bTPHCM\b", "Thành phố Hồ Chí Minh", q)
    q = re.sub(r"(?i)\bHCMC\b", "Thành phố Hồ Chí Minh", q)
    q = re.sub(r"(?i)\bHCM\b", "Thành phố Hồ Chí Minh", q)
    q = re.sub(r"(?i)\bSài Gòn\b|\bSai Gon\b", "Thành phố Hồ Chí Minh", q)

    low2 = q.lower()
    has_hcm2 = ("hồ chí minh" in low2) or ("ho chi minh" in low2)

    if has_district and not has_hcm2:
        q = f"{q}, Thành phố Hồ Chí Minh"

    if not has_vn:
        q = f"{q}, Việt Nam"

    return q.strip()


def _make_geocode_variants(raw_q: str):
    base = _normalize_raw_query(raw_q)
    if not base:
        return []

    v1 = _ensure_hcm_vn(base)
    v2 = _strip_accents(v1)

    variants = [v1, v2]

    # English city variant
    if "Thành phố Hồ Chí Minh" in v1:
        variants.append(v1.replace("Thành phố Hồ Chí Minh", "Ho Chi Minh City"))
        variants.append(v2.replace("Thanh pho Ho Chi Minh", "Ho Chi Minh City"))

    # remove duplicates
    seen = set()
    out = []
    for v in variants:
        vv = re.sub(r"\s+", " ", v).strip()
        if vv and vv not in seen:
            seen.add(vv)
            out.append(vv)
    return out


# ============================================================
# NOMINATIM (an toàn, có retry, không cache NONE khi lỗi)
# ============================================================
def _call_nominatim_search_safe(query: str, use_countrycodes=True):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
    }
    if use_countrycodes:
        params["countrycodes"] = VN_COUNTRY_CODE

    try:
        r = requests.get(url, params=params, headers=_headers(), timeout=NOMINATIM_TIMEOUT)
        status = r.status_code

        # nếu bị chặn / rate limit -> trả err để caller biết (đừng cache NONE)
        if status != 200:
            return None, {"status": status, "body": r.text[:200], "query": query}

        arr = r.json()
        return (arr[0] if arr else None), None
    except Exception as e:
        return None, {"exception": str(e), "query": query}


def _forward_geocode(raw_q: str):
    variants = _make_geocode_variants(raw_q)
    if not variants:
        return None, None, variants

    cache_key = f"geo_fwd:{variants[0].lower()}"
    cached = _cache_get(cache_key)
    if cached == NONE_SENTINEL:
        return None, None, variants
    if isinstance(cached, dict):
        return cached, None, variants

    last_err = None
    had_http_error = False

    for v in variants:
        for attempt in range(NOMINATIM_RETRIES + 1):
            res, err = _call_nominatim_search_safe(v, use_countrycodes=True)
            if res:
                _cache_set(cache_key, res)
                return res, None, variants
            if err:
                last_err = err
                had_http_error = True

            # fallback without countrycodes
            res, err = _call_nominatim_search_safe(v, use_countrycodes=False)
            if res:
                _cache_set(cache_key, res)
                return res, None, variants
            if err:
                last_err = err
                had_http_error = True

            # backoff nhẹ nếu bị 429
            if isinstance(last_err, dict) and last_err.get("status") == 429:
                time.sleep(0.4)

    # Chỉ cache NONE nếu không có lỗi HTTP/exception (tức là 200 nhưng rỗng thật)
    if not had_http_error:
        _cache_set(cache_key, NONE_SENTINEL)

    return None, last_err, variants


def _call_nominatim_reverse_safe(lat: float, lon: float):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"format": "jsonv2", "lat": lat, "lon": lon, "zoom": 18, "addressdetails": 1}
    try:
        r = requests.get(url, params=params, headers=_headers(), timeout=NOMINATIM_TIMEOUT)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def _reverse_geocode(lat: float, lon: float):
    cache_key = f"geo_rev:{round(lat,6)}:{round(lon,6)}"
    cached = _cache_get(cache_key)
    if isinstance(cached, dict):
        return cached
    res = _call_nominatim_reverse_safe(lat, lon)
    if res:
        _cache_set(cache_key, res)
        return res
    return None


def _extract_road_display(geo_json: dict):
    display = (geo_json or {}).get("display_name", "") or ""
    addr = (geo_json or {}).get("address", {}) or {}
    road = addr.get("road") or addr.get("pedestrian") or addr.get("neighbourhood") or ""
    suburb = addr.get("suburb") or addr.get("quarter") or ""
    city = addr.get("city") or addr.get("town") or addr.get("state") or ""
    return road, suburb, city, display


# ============================================================
# TOOL 0: DEBUG GEOCODE
# ============================================================
def debug_geocode(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"error": "Required: q"}, status=400)

    latlon = _parse_latlon(q)
    if latlon:
        return JsonResponse({"mode": "latlon", "input": q, "latlon": {"lat": latlon[0], "lon": latlon[1]}})

    hit, err, variants = _forward_geocode(q)
    return JsonResponse({"mode": "address", "input": q, "variants": variants, "hit": hit, "error": err})


# ============================================================
# TOOL 1: FILTER BY BRAND
# ============================================================
def stores_by_brand(request):
    brand = _normalize_brand(request.GET.get("brand", ""))
    qs = Store.objects.all()
    if brand:
        qs = qs.filter(_brand_q(brand))

    stores = [_store_dict(s) for s in qs]
    return JsonResponse({"tool": "filter_by_brand", "brand": brand or "ALL", "count": len(stores), "stores": stores})


# ============================================================
# TOOL 2: STORES IN RADIUS
# ============================================================
def stores_in_radius(request):
    try:
        lat = float(request.GET.get("lat"))
        lon = float(request.GET.get("lon"))
        radius_km = float(request.GET.get("radius_km", 1))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Required: lat, lon. Optional: radius_km"}, status=400)

    if radius_km <= 0:
        return JsonResponse({"error": "radius_km must be > 0"}, status=400)

    qs = _bbox_filter(Store.objects.all(), lat, lon, radius_km)

    result = []
    for s in qs:
        d = _haversine_km(lat, lon, float(s.latitude), float(s.longitude))
        if d <= radius_km:
            result.append(_store_dict(s, {"distance_km": round(d, 3)}))

    result.sort(key=lambda x: x["distance_km"])

    return JsonResponse({
        "tool": "search_in_radius",
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "count": len(result),
        "stores": result,
    })


# ============================================================
# TOOL 3: SMART SEARCH  (LUÔN TRẢ VỀ TỌA ĐỘ ĐỂ MAP HIỆN)
# ============================================================
def smart_search(request):
    raw_q = (request.GET.get("q") or "").strip()
    if not raw_q:
        # vẫn trả fallback để map không "chết"
        lat, lon = DEFAULT_CENTER
        return JsonResponse({
            "tool": "smart_search",
            "ok": False,
            "message": "Bạn chưa nhập địa chỉ. Đang hiển thị vị trí mặc định (TP.HCM).",
            "location": {"lat": lat, "lon": lon, "display_address": "TP.HCM (mặc định)"},
            "store": None,
            "suggested_max_km": None,
        })

    brand = _normalize_brand(request.GET.get("brand", "CIRCLEK")) or "CIRCLEK"
    try:
        max_km = float(request.GET.get("max_km", 0.2))
    except ValueError:
        max_km = 0.2
    if max_km <= 0:
        max_km = 0.2

    # 1) lat/lon mode
    latlon = _parse_latlon(raw_q)
    mode = "latlon" if latlon else "address"

    geocode_err = None
    variants = []
    hit = None

    if latlon:
        lat, lon = latlon
    else:
        hit, geocode_err, variants = _forward_geocode(raw_q)
        if hit:
            lat, lon = float(hit["lat"]), float(hit["lon"])
        else:
            # FAIL nhưng vẫn trả fallback để map chắc chắn hiện
            lat, lon = DEFAULT_CENTER

    # 2) reverse (nếu có)
    road = suburb = city = display_address = ""
    geo = _reverse_geocode(lat, lon)
    if geo:
        road, suburb, city, display_address = _extract_road_display(geo)
    else:
        display_address = "TP.HCM (mặc định)" if (lat, lon) == DEFAULT_CENTER else ""

    # 3) tìm cửa hàng gần nhất trong max_km (nếu có tọa độ)
    candidates = _bbox_filter(Store.objects.filter(_brand_q(brand)), lat, lon, max_km)

    best = None
    best_d = 10**9
    for s in candidates:
        d = _haversine_km(lat, lon, float(s.latitude), float(s.longitude))
        if d < best_d:
            best_d, best = d, s

    store_data = None
    suggested = None

    if best and best_d <= max_km:
        store_data = _store_dict(best, {"distance_km": round(best_d, 4)})
        store_msg = f"Tìm thấy {brand} gần nhất trong {max_km} km."
    else:
        store_msg = f"Không có {brand} trong {max_km} km."
        suggested = _suggest_next_km(max_km)

    # 4) message tổng hợp
    if mode == "address" and not hit:
        msg = (
            "Không định vị được địa chỉ bạn nhập (có thể do viết tắt/lỗi hoặc bị chặn Nominatim). "
            "Hệ thống đang hiển thị vị trí mặc định (TP.HCM). "
            + store_msg
        )
        ok = False
    else:
        msg = "Đã định vị. " + store_msg
        ok = True

    return JsonResponse({
        "tool": "smart_search",
        "ok": ok,
        "mode": mode,
        "input": {"q": raw_q, "brand": brand, "max_km": max_km},
        "geocode": {
            "hit": hit,
            "variants_tried": variants[:8],
            "error": geocode_err,
        } if mode == "address" else None,
        "location": {
            "lat": lat,
            "lon": lon,
            "road": road,
            "suburb": suburb,
            "city": city,
            "display_address": display_address,
        },
        "store": store_data,
        "message": msg,
        "suggested_max_km": suggested,
    })
