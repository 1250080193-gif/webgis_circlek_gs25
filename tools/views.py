import math
import re
import time
import unicodedata
import requests

from django.http import JsonResponse
from django.db.models import Q
from django.core.cache import cache

from gis_store.models import CuaHang


# ============================================================
# CONFIG
# ============================================================
ALIASES = {
    "CIRCLEK": ["CIRCLEK", "CIRCLE K", "CIRCLE_K", "CIRCLE-K", "Circle K"],
    "GS25": ["GS25", "GS 25", "Gs25"],
}

DEFAULT_CENTER = (10.7769, 106.7009)  # TP.HCM
VN_COUNTRY_CODE = "vn"
CACHE_TTL = 60 * 60 * 24  # 24h
NONE_SENTINEL = "__NONE__"

CONTACT_EMAIL = "student@example.com"
NOMINATIM_RETRIES = 2
NOMINATIM_TIMEOUT = 12


# ============================================================
# BASIC HELPERS
# ============================================================
def _headers():
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
        q |= Q(chuoi__ten__iexact=b)
    return q


def _parse_latlon(text: str):
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
        vi_do__gte=lat - dlat, vi_do__lte=lat + dlat,
        kinh_do__gte=lon - dlon, kinh_do__lte=lon + dlon
    )


def _store_dict(s: CuaHang, extra=None):
    d = {
        "id": s.id,
        "name": s.ten,                 # giữ key cũ "name" cho frontend/map
        "brand": s.chuoi.ten,
        "address_db": s.dia_chi,
        "district": s.quan_huyen,
        "lat": float(s.vi_do),
        "lon": float(s.kinh_do),
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
# NORMALIZE INPUT
# ============================================================
def _normalize_raw_query(raw: str) -> str:
    if not raw:
        return ""
    parts = [x.strip() for x in raw.splitlines() if x.strip()]
    q = ", ".join(parts) if parts else raw.strip()
    q = re.sub(r"\s+", " ", q).strip()

    q = re.sub(r"(?i)^\s*(circle\s*k|circlek|gs25)\s+", "", q).strip()
    q = re.sub(r"(?i)\b(tìm|search|near|gần)\b", "", q).strip()

    q = re.sub(r"(?i)\bTP\.\b", "TP", q)
    q = re.sub(r"(?i)\bQ\.\b", "Q", q)
    q = re.sub(r"(?i)\bP\.\b", "P", q)

    q = re.sub(r"(?i)\bF\s*(\d+)\b", r"Phường \1", q)
    q = re.sub(r"(?i)\bD\s*(\d+)\b", r"Quận \1", q)

    q = re.sub(r"(?i)\bQ\s*(\d+)\b", r"Quận \1", q)
    q = re.sub(r"(?i)\bP\s*(\d+)\b", r"Phường \1", q)

    q = re.sub(r"(?i)\bDistrict\s*(\d+)\b", r"Quận \1", q)
    q = re.sub(r"(?i)\bWard\s*(\d+)\b", r"Phường \1", q)

    q = re.sub(r"\s*,\s*", ", ", q)
    q = re.sub(r"(, )+", ", ", q).strip(" ,")
    return q


def _ensure_hcm_vn(q: str) -> str:
    if not q:
        return ""

    q = re.sub(r"(?i)\bTP\b\.?$", "Thành phố Hồ Chí Minh", q).strip()

    low = q.lower()
    has_vn = ("việt nam" in low) or ("vietnam" in low)
    has_hcm = ("hồ chí minh" in low) or ("ho chi minh" in low) or ("hcm" in low) or ("hcmc" in low)
    has_district = bool(re.search(r"(?i)\bquận\s*\d+\b", q))

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
    if "Thành phố Hồ Chí Minh" in v1:
        variants.append(v1.replace("Thành phố Hồ Chí Minh", "Ho Chi Minh City"))
        variants.append(v2.replace("Thanh pho Ho Chi Minh", "Ho Chi Minh City"))

    seen = set()
    out = []
    for v in variants:
        vv = re.sub(r"\s+", " ", v).strip()
        if vv and vv not in seen:
            seen.add(vv)
            out.append(vv)
    return out


# ============================================================
# NOMINATIM
# ============================================================
def _call_nominatim_search_safe(query: str, use_countrycodes=True):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "jsonv2", "limit": 1, "addressdetails": 1}
    if use_countrycodes:
        params["countrycodes"] = VN_COUNTRY_CODE

    try:
        r = requests.get(url, params=params, headers=_headers(), timeout=NOMINATIM_TIMEOUT)
        status = r.status_code
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
        for _ in range(NOMINATIM_RETRIES + 1):
            res, err = _call_nominatim_search_safe(v, use_countrycodes=True)
            if res:
                _cache_set(cache_key, res)
                return res, None, variants
            if err:
                last_err = err
                had_http_error = True

            res, err = _call_nominatim_search_safe(v, use_countrycodes=False)
            if res:
                _cache_set(cache_key, res)
                return res, None, variants
            if err:
                last_err = err
                had_http_error = True

            if isinstance(last_err, dict) and last_err.get("status") == 429:
                time.sleep(0.4)

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
# TOOL 1: FILTER BY BRAND (chuỗi)
# ============================================================
def stores_by_brand(request):
    brand = _normalize_brand(request.GET.get("brand", ""))
    qs = CuaHang.objects.select_related("chuoi").all()
    if brand:
        qs = qs.filter(_brand_q(brand))

    stores = [_store_dict(s) for s in qs]
    return JsonResponse({"tool": "filter_by_brand", "brand": brand or "ALL", "count": len(stores), "stores": stores})


# ============================================================
# TOOL 2: STORES IN RADIUS (UPDATED: filter brand)
# ============================================================
def stores_in_radius(request):
    try:
        lat = float(request.GET.get("lat"))
        lon = float(request.GET.get("lon"))
        radius_km = float(request.GET.get("radius_km", 1))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Required: lat, lon. Optional: radius_km, brand"}, status=400)

    brand = _normalize_brand(request.GET.get("brand", ""))  # ✅ thêm
    if radius_km <= 0:
        return JsonResponse({"error": "radius_km must be > 0"}, status=400)

    qs0 = CuaHang.objects.select_related("chuoi").all()
    if brand:
        qs0 = qs0.filter(_brand_q(brand))
    qs = _bbox_filter(qs0, lat, lon, radius_km)

    result = []
    for s in qs:
        d = _haversine_km(lat, lon, float(s.vi_do), float(s.kinh_do))
        if d <= radius_km:
            result.append(_store_dict(s, {"distance_km": round(d, 3)}))

    result.sort(key=lambda x: x["distance_km"])

    return JsonResponse({
        "tool": "search_in_radius",
        "brand": brand or "ALL",
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "count": len(result),
        "stores": result,
    })


# ============================================================
# TOOL 3: SMART SEARCH (UPDATED: return stores list)
# ============================================================
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def smart_search(request):
    # ✅ BẮT BUỘC đặt ở đầu hàm
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    # ==== LẤY JSON BODY ====
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = {}

    ten = data.get("ten", "").strip()
    dia_chi = data.get("dia_chi", "").strip()
    quan = data.get("quan", "").strip()
    lat = data.get("lat")
    lng = data.get("lng")

    # ==== BRAND ====
    brand = _normalize_brand(ten) or "CIRCLEK"

    # ==== MAX KM ====
    try:
        max_km = float(data.get("max_km", 0.2))
    except (TypeError, ValueError):
        max_km = 0.2

    if max_km <= 0:
        max_km = 0.2


    # ==== XÁC ĐỊNH VỊ TRÍ ====

    mode = "latlon"
    hit = None
    geocode_err = None
    variants = []

    # Nếu có lat/lng → dùng luôn
    use_client = False

    if lat not in (None, "") and lng not in (None, ""):
        try:
            lat = float(lat)
            lng = float(lng)
            use_client = True
        except:
            lat = None
            lng = None


    # Không có lat/lng → geocode bằng địa chỉ
    if not use_client and dia_chi:

        hit, geocode_err, variants = _forward_geocode(dia_chi)

        if hit:
            lat = float(hit["lat"])
            lng = float(hit["lon"])
            mode = "address"
        else:
            lat, lng = DEFAULT_CENTER
            mode = "address"

    # Không có gì cả → default
    else:
        lat, lng = DEFAULT_CENTER
        mode = "default"


    # ==== REVERSE GEOCODE ====

    road = suburb = city = display_address = ""

    geo = _reverse_geocode(lat, lng)

    if geo:
        road, suburb, city, display_address = _extract_road_display(geo)
    else:
        display_address = dia_chi or "TP.HCM (mặc định)"


    # ==== LỌC CỬA HÀNG ====

    candidates = _bbox_filter(
        CuaHang.objects
        .select_related("chuoi")
        .filter(_brand_q(brand)),
        lat,
        lng,
        max_km
    )

    stores_list = []

    for s in candidates:

        d = _haversine_km(
            lat,
            lng,
            float(s.vi_do),
            float(s.kinh_do)
        )

        if d <= max_km:

            stores_list.append(
                _store_dict(
                    s,
                    {"distance_km": round(d, 3)}
                )
            )


    stores_list.sort(key=lambda x: x["distance_km"])

    store_data = stores_list[0] if stores_list else None


    # ==== MESSAGE ====

    if stores_list:
        msg = f"Tìm thấy {len(stores_list)} {brand} trong {max_km} km."
        ok = True
        suggested = None
    else:
        msg = f"Không có {brand} trong {max_km} km."
        ok = False
        suggested = _suggest_next_km(max_km)


    # ==== RESPONSE ====

    return JsonResponse({

        "tool": "smart_search",
        "ok": ok,
        "mode": mode,

        "input": {
            "ten": ten,
            "dia_chi": dia_chi,
            "quan": quan,
            "lat": lat,
            "lng": lng,
            "brand": brand,
            "max_km": max_km
        },

        "geocode": {
            "hit": hit,
            "variants_tried": variants[:8],
            "error": geocode_err,
        } if mode == "address" else None,

        "location": {
            "lat": lat,
            "lon": lng,
            "road": road,
            "suburb": suburb,
            "city": city,
            "display_address": display_address,
        },

        "store": store_data,
        "count": len(stores_list),
        "stores": stores_list[:200],
        "message": msg,
        "suggested_max_km": suggested,
    })
