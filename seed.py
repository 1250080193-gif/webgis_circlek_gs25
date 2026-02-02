import django
django.setup()
# Chay trong: python manage.py shell
# hoac dua vao management command

from gis_store.models import (
    ChuoiCuaHang, NhaCungCap, ThuongHieu, NhomSanPham, SanPham
)

# =========================
# Helper: get_or_create
# =========================
def get_cat(name: str) -> NhomSanPham:
    obj, _ = NhomSanPham.objects.get_or_create(ten=name)
    return obj

def get_brand(name: str | None) -> ThuongHieu | None:
    if not name:
        return None
    obj, _ = ThuongHieu.objects.get_or_create(ten=name)
    return obj

def get_sup(name: str) -> NhaCungCap:
    obj, _ = NhaCungCap.objects.get_or_create(ten=name, defaults={"ghi_chu": ""})
    return obj


# ---------------------------------------------------------
# 1. CHUOI CUA HANG
# ---------------------------------------------------------
chains_data = [
    {
        "ten": "Circle K",
        "mo_ta": "Take it easy. Chuoi cua hang tien loi mo cua 24/7, noi tieng voi do an che bien tai cho."
    },
    {
        "ten": "GS25",
        "mo_ta": "Lifestyle Platform. Chuoi cua hang tien loi Han Quoc, mang den trai nghiem am thuc Han Quoc."
    }
]

print("--- Dang tao Chuoi Cua Hang ---")
for item in chains_data:
    ChuoiCuaHang.objects.get_or_create(
        ten=item["ten"],
        defaults={"mo_ta": item["mo_ta"]}
    )


# ---------------------------------------------------------
# 2. NHA CUNG CAP
# ---------------------------------------------------------
suppliers_data = [
    {
        "ten": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "ghi_chu": "Don vi van hanh va cung cap doc quyen san pham che bien (Hot Food, Froster) cho Circle K."
    },
    {
        "ten": "GS Retail Vietnam",
        "ghi_chu": "Don vi van hanh GS25, nhap khau truc tiep hang nhan hieu Youus tu Han Quoc."
    },
    {
        "ten": "Suntory PepsiCo Viet Nam",
        "ghi_chu": "Cung cap: Pepsi, Sting, Aquafina, Tea+, 7Up."
    },
    {
        "ten": "Coca-Cola Viet Nam",
        "ghi_chu": "Cung cap: Coca-Cola, Sprite, Fanta, Dasani, Nutriboost."
    },
    {
        "ten": "Acecook Viet Nam",
        "ghi_chu": "Cung cap: Hao Hao, Mi ly Modern, ... "
    },
    {
        "ten": "Masan Consumer",
        "ghi_chu": "Cung cap: Omachi, Kokomi, Wake-up 247."
    },
    {
        "ten": "Cong ty TNHH Thuc Pham Orion Vina",
        "ghi_chu": "Cung cap: ChocoPie, Snack O'Star, Toonies."
    }
]

print("--- Dang tao Nha Cung Cap ---")
for item in suppliers_data:
    NhaCungCap.objects.get_or_create(
        ten=item["ten"],
        defaults={"ghi_chu": item["ghi_chu"]}
    )


# ---------------------------------------------------------
# 3. THUONG HIEU
# ---------------------------------------------------------
brands_list = [
    "Circle K Food",
    "GS25 Fresh",
    "Youus (Han Quoc)",
    "Hao Hao",
    "Modern",
    "Indomie",
    "Omachi",
    "Pepsi",
    "Coca-Cola",
    "Sting",
    "Aquafina",
    "Dasani",
    "O'Star",
    "Lay's",
    "TH True Milk",
    "Milo",
]

print("--- Dang tao Thuong Hieu ---")
for name in brands_list:
    ThuongHieu.objects.get_or_create(ten=name)


# ---------------------------------------------------------
# 4. NHOM SAN PHAM
# ---------------------------------------------------------
categories_list = [
    "Do an che bien nong (Hot Food)",
    "Do uong pha che (Barista/Froster)",
    "Mi an lien & Thuc pham dong hop",
    "Nuoc giai khat & Do uong lanh",
    "Snack & Banh keo",
    "Sua & Che pham tu sua",
    "Hoa my pham & Ca nhan",
]

print("--- Dang tao Nhom San Pham ---")
for name in categories_list:
    NhomSanPham.objects.get_or_create(ten=name)

print("HOAN THANH BUOC 1: Du lieu nen tang da san sang.")


# ---------------------------------------------------------
# 5. SAN PHAM
# ---------------------------------------------------------
ck_products = [
    {
        "ten": "Froster Cau Vong (Size L)",
        "nhom": "Do uong pha che (Barista/Froster)",
        "brand": "Circle K Food",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Do uong da bao nhieu tang huong vi."
    },
    {
        "ten": "Mi Tron Indomie Trung Op La Xuc Xich",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "Indomie",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Mi Indomie xao kho + trung op la + xuc xich."
    },
    {
        "ten": "Banh Bao Trung Muoi (Hap nong)",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "Circle K Food",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Banh bao nhan thit trung muoi."
    },
    {
        "ten": "Banh Mi Op La 2 Trung",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "Circle K Food",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Banh mi + 2 trung op la."
    },
    {
        "ten": "Ca Phe Bac Xiu Da (Ly lon)",
        "nhom": "Do uong pha che (Barista/Froster)",
        "brand": "Circle K Food",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Ca phe sua da phong cach Sai Gon."
    },
    {
        "ten": "Xoi La Chuoi (Thit Kho Tau)",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "Circle K Food",
        "ncc": "Cong ty TNHH Vong Tron Do (Red Circle)",
        "desc": "Xoi boc la chuoi."
    },
]

gs_products = [
    {
        "ten": "Tokbokki Xuc Xich Sot Cay (Ly)",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "GS25 Fresh",
        "ncc": "GS Retail Vietnam",
        "desc": "Banh gao cay Han Quoc sot gochujang."
    },
    {
        "ten": "Nuoc Ep Dua Hau Youus 230ml",
        "nhom": "Nuoc giai khat & Do uong lanh",
        "brand": "Youus (Han Quoc)",
        "ncc": "GS Retail Vietnam",
        "desc": "Nuoc ep nhap khau tu Han Quoc."
    },
    {
        "ten": "Sandwich Inkigayo",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "GS25 Fresh",
        "ncc": "GS Retail Vietnam",
        "desc": "Sandwich noi tieng Han Quoc."
    },
    {
        "ten": "Bap Rang Bo Vi Pho Mai Youus",
        "nhom": "Snack & Banh keo",
        "brand": "Youus (Han Quoc)",
        "ncc": "GS Retail Vietnam",
        "desc": "Snack bap rang bo nhap khau."
    },
    {
        "ten": "Lau Cha Ca Omok (Ly)",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "GS25 Fresh",
        "ncc": "GS Retail Vietnam",
        "desc": "Cha ca Han Quoc xien que."
    },
    {
        "ten": "Com Nam Tom Mayonnaise",
        "nhom": "Do an che bien nong (Hot Food)",
        "brand": "GS25 Fresh",
        "ncc": "GS Retail Vietnam",
        "desc": "Com nam tam giac kieu Han."
    },
]

common_products = [
    {
        "ten": "Mi Hao Hao Tom Chua Cay (Goi)",
        "nhom": "Mi an lien & Thuc pham dong hop",
        "brand": "Hao Hao",
        "ncc": "Acecook Viet Nam",
        "desc": ""
    },
    {
        "ten": "Mi Ly Modern Lau Thai Tom",
        "nhom": "Mi an lien & Thuc pham dong hop",
        "brand": "Modern",
        "ncc": "Acecook Viet Nam",
        "desc": ""
    },
    {
        "ten": "Nuoc Ngot Coca-Cola Zero 320ml",
        "nhom": "Nuoc giai khat & Do uong lanh",
        "brand": "Coca-Cola",
        "ncc": "Coca-Cola Viet Nam",
        "desc": ""
    },
    {
        "ten": "Nuoc Tang Luc Sting Dau 330ml",
        "nhom": "Nuoc giai khat & Do uong lanh",
        "brand": "Sting",
        "ncc": "Suntory PepsiCo Viet Nam",
        "desc": ""
    },
    {
        "ten": "Nuoc Tinh Khiet Aquafina 500ml",
        "nhom": "Nuoc giai khat & Do uong lanh",
        "brand": "Aquafina",
        "ncc": "Suntory PepsiCo Viet Nam",
        "desc": ""
    },
    {
        "ten": "Snack Khoai Tay O'Star Vi Kim Chi 63g",
        "nhom": "Snack & Banh keo",
        "brand": "O'Star",
        "ncc": "Cong ty TNHH Thuc Pham Orion Vina",
        "desc": ""
    },
    {
        "ten": "Sua Tuoi TH True Milk Co Duong 180ml",
        "nhom": "Sua & Che pham tu sua",
        "brand": "TH True Milk",
        "ncc": "Masan Consumer",
        "desc": ""
    },
]

print("--- Dang tao du lieu San Pham ---")
all_items = ck_products + gs_products + common_products

for item in all_items:
    nhom = get_cat(item["nhom"])
    ncc = get_sup(item["ncc"])
    th = get_brand(item.get("brand"))

    defaults = {
        "nhom_san_pham": nhom,
        "nha_cung_cap": ncc,
        "thuong_hieu": th,
    }

    # Neu SanPham co field mo_ta thi bat no len:
    # defaults["mo_ta"] = item.get("desc", "")

    obj, created = SanPham.objects.get_or_create(
        ten=item["ten"],
        defaults=defaults
    )
    print(("Da tao: " if created else "Da ton tai: ") + item["ten"])

print(f"HOAN THANH BUOC 2: Da xu ly {len(all_items)} san pham.")

# =========================================================
# PHAN BO SUNG: CUA HANG + GAN SAN PHAM + NHAN VIEN + KHUYEN MAI
# Dan tiep vao CUOI FILE gis_store/seed.py
# =========================================================

import random

from gis_store.models import (
    ChuoiCuaHang,
    CuaHang,
    SanPham,
    NhanVien,
    KhuyenMai,
    ThuongHieu,
)

# ----------------------------
# Lay object chuoi + san pham
# ----------------------------
ck_chain, _ = ChuoiCuaHang.objects.get_or_create(ten="Circle K", defaults={"mo_ta": ""})
gs_chain, _ = ChuoiCuaHang.objects.get_or_create(ten="GS25", defaults={"mo_ta": ""})
all_products = list(SanPham.objects.all())

def create_batch_stores(data_list, chain_obj):
    print(f"\n--- DANG TAO {chain_obj.ten.upper()} ({len(data_list)} CUA HANG) ---")
    created_count = 0

    for idx, item in enumerate(data_list, start=1):
        store, created = CuaHang.objects.get_or_create(
            ten=item["ten"],
            chuoi=chain_obj,
            dia_chi=item["dia_chi"],
            defaults={
                "dia_chi": item["dia_chi"],
                "quan_huyen": item["quan"],
                "vi_do": item["lat"],
                "kinh_do": item["lng"],
            },
        )

        if created:
            created_count += 1

            # Gan ngau nhien san pham (toi da 15)
            if all_products:
                k = min(len(all_products), 15)
                store.san_pham.set(random.sample(all_products, k=k))

        if idx % 5 == 0:
            print(f"  ... xu ly {idx}/{len(data_list)} cua hang")

    print(f"-> Hoan tat: tao moi {created_count} cua hang cho {chain_obj.ten}.")


# ======================================================================
# 1) DANH SACH CIRCLE K (HCMC)
# ======================================================================
ck_stores_data = [
    {"ten": "Circle K Viet Nam", "dia_chi": "915/40 ĐH34, Phước Kiển, Nhà Bè, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Nhà Bè", "lat": 10.713921524842874, "lng": 106.70106234841948},
    {"ten": "Circle K Viet Nam", "dia_chi": "944 Lê Văn Lương, Ấp 3, Nhà Bè, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Nhà Bè", "lat": 10.709305295684091, "lng": 106.70237449026769},
    {"ten": "Circle K Viet Nam", "dia_chi": "15 Số 3, Phú Mỹ, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.714218913680112, "lng": 106.73212757997005},
    {"ten": "Circle K Viet Nam", "dia_chi": "167 Phạm Hữu Lầu, Phường Mỹ Phước, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.704470794115853, "lng": 106.73259604295728},
    {"ten": "Circle K Viet Nam", "dia_chi": "Era Town Đức Khải, Phú Mỹ, Quận 7, Việt Nam", "quan": "Quận 7", "lat": 10.700353715903157, "lng": 106.73204081483146},
    {"ten": "Circle K Viet Nam", "dia_chi": "Thái Văn Lung, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.779408024062784, "lng": 106.70490591065492},
    {"ten": "Circle K Viet Nam", "dia_chi": "A67 Nguyễn Trãi, Phường Nguyễn Cư Trinh, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.766243477643815, "lng": 106.68786851215067},
    {"ten": "Circle K Viet Nam", "dia_chi": "257A Nguyễn Trãi, Phường Nguyễn Cư Trinh, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.764590294219525, "lng": 106.68760443856459},
    {"ten": "Circle K Viet Nam", "dia_chi": "167 Lê Thánh Tôn, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.773856008040006, "lng": 106.6989489929547},
    {"ten": "Circle K Viet Nam", "dia_chi": "44 Nguyễn Huệ, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.774146858365144, "lng": 106.70405387345443},
    {"ten": "Circle K Viet Nam", "dia_chi": "1 Bùi Viện, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.767646458804691, "lng": 106.6945896877393},
    {"ten": "Circle K Viet Nam", "dia_chi": "50 Bùi Viện, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.767402647975752, "lng": 106.69383092154868},
    {"ten": "Circle K Viet Nam", "dia_chi": "273 Đường Trần Bình Trọng, Phường 4, Quận 5, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 5", "lat": 10.761099781469689, "lng": 106.67947534026864},
    {"ten": "Circle K Viet Nam", "dia_chi": "45 Cao Thắng, Phường 3, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.77005503370447, "lng": 106.6819827385069},

    {"ten": "Circle K Bùi Thị Xuân", "dia_chi": "160 Bùi Thị Xuân, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.768613321248685, "lng": 106.6869995332389},
    {"ten": "Circle K Viet Nam", "dia_chi": "11 Nguyễn Văn Tráng, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.76992093215846, "lng": 106.69233857528418},

    {"ten": "Circle K (Bà Huyện Thanh Quan)", "dia_chi": "31 Bà Huyện Thanh Quan, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.775371641990047, "lng": 106.68977674846634},
    {"ten": "Circle K Viet Nam", "dia_chi": "171 nối liền/165-167-169 Hoàng Diệu, Phường 9, Quận 4, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 4", "lat": 10.762952033093377, "lng": 106.70333474484411},
    {"ten": "Circle K Viet Nam", "dia_chi": "22 Đ. Nguyễn Trường Tộ, Phường 12, Quận 4, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 4", "lat": 10.765799735771017, "lng": 106.70454445249631},
    {"ten": "Circle K Viet Nam", "dia_chi": "188 Nguyễn Thị Minh Khai, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.775771719932317, "lng": 106.69127120029219},
    {"ten": "Circle K Viet Nam", "dia_chi": "103 Trương Định, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.777743060111934, "lng": 106.68962936236365},

    {"ten": "Circle K Nguyễn Du", "dia_chi": "57 Nguyễn Du, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.779257007697646, "lng": 106.70035204328279},
    {"ten": "Circle K Viet Nam", "dia_chi": "15C Nguyễn Thị Minh Khai, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.78592532742179, "lng": 106.70111637513882},
    {"ten": "Circle K Viet Nam", "dia_chi": "L1-SH.01B, Landmark 1 720A, Nguyễn Hữu Cảnh, Vinhomes Tân Cảng, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Bình Thạnh", "lat": 10.786598032596347, "lng": 106.71017884907972},

    {"ten": "Circle K Nguyen Huu Cau", "dia_chi": "32 Nguyễn Hữu Cầu, Phường Tân Định, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.791181681283504, "lng": 106.69107642425759},
    {"ten": "Circle K Viet Nam", "dia_chi": "2 Trần Khắc Chân, Phường Tân Định, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.792226999526166, "lng": 106.69140608974133},

    {"ten": "Circle K Viet Nam", "dia_chi": "74 Nguyễn Cơ Thạch, An Lợi Đông, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thủ Đức", "lat": 10.771258853454016, "lng": 106.72436547270412},
    {"ten": "Circle K Viet Nam", "dia_chi": "No.03-SH01, Vinhomes Tân Cảng, Bình Thạnh, Việt Nam", "quan": "Bình Thạnh", "lat": 10.793702344238987, "lng": 106.72196487277583},

    {"ten": "Circle K Nguyễn Ảnh Thủ", "dia_chi": "144/5 Đ. Nguyễn Ảnh Thủ, Trung Mỹ Tây, Hóc Môn, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Hóc Môn", "lat": 10.858949068747146, "lng": 106.60937586486152},
    {"ten": "Circle K Viet Nam", "dia_chi": "27 Tôn Thất Tùng, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.770570828991254, "lng": 106.68779186415671},
    {"ten": "Circle K Viet Nam", "dia_chi": "271 Phạm Ngũ Lão, Phường Phạm Ngũ Lão, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.767994002239591, "lng": 106.6921385290345},
    {"ten": "CIRCLE K NGUYỄN KHẮC NHU", "dia_chi": "69 Nguyễn Khắc Nhu, Phường Cô Giang, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.763615744256448, "lng": 106.69296207505096},
    {"ten": "Circle K Viet Nam", "dia_chi": "65C Nguyễn Thái Học, Phường Cầu Ông Lãnh, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.766412327428094, "lng": 106.6961273030321},
    {"ten": "Circle K Viet Nam", "dia_chi": "273 Lê Thánh Tôn, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.771761718753638, "lng": 106.69565674095568},
    {"ten": "Circle K Nguyễn Công Trứ", "dia_chi": "162 Nguyễn Công Trứ, Phường Nguyễn Thái Bình, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.768841317607711, "lng": 106.70134126741988},
    {"ten": "Circle K Viet Nam", "dia_chi": "18 Lê Lai, Phường Bến Thành, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.771843849500712, "lng": 106.69728957122159},
    {"ten": "Circle K Viet Nam", "dia_chi": "42 Lê Lợi, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.77413303114628, "lng": 106.7004561319834},
    {"ten": "Circle K Nguyễn Huệ", "dia_chi": "47 Nguyễn Huệ, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.77283088985499, "lng": 106.70450397235474},
    {"ten": "Circle K Nguyễn Huệ", "dia_chi": "82 Nguyễn Huệ, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.775202983736813, "lng": 106.70284054294288},
    {"ten": "Circle K Lý Tự Trọng", "dia_chi": "45 Lý Tự Trọng, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.778627122043348, "lng": 106.70178311270827},
    {"ten": "Circle K Viet Nam", "dia_chi": "59 Đông Du, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.775469615783884, "lng": 106.70419712613567},
    {"ten": "Circle K Viet Nam", "dia_chi": "36 Hai Bà Trưng, Bến Nghé, Quận 1, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 1", "lat": 10.778299185512985, "lng": 106.70327998969472},
    {"ten": "Circle K Trần Não", "dia_chi": "119 Trần Não, khu phố 10, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thủ Đức", "lat": 10.79271449534919, "lng": 106.73084738162981},
    {"ten": "Circle K Viet Nam", "dia_chi": "Chung Cư Bộ Công An, 83 Đ. Số 3, Phường An Khánh, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thủ Đức", "lat": 10.79505054679644, "lng": 106.73641710593193},
    {"ten": "Circle K Thảo Điền", "dia_chi": "6 Thảo Điền, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thủ Đức", "lat": 10.802157250626763, "lng": 106.73837853419045},
    {"ten": "Circle K Viet Nam", "dia_chi": "Novaland The Sun Avenue, 28 Mai Chí Thọ, An Phú, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thủ Đức", "lat": 10.784942927370615, "lng": 106.74756225178163},
    {"ten": "Circle K 537 Nguyễn Duy Trinh", "dia_chi": "Phường Bình Trưng Tây, Quận 2, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 2", "lat": 10.78991922102415, "lng": 106.77061465224789},
    {"ten": "Circle K Viet Nam", "dia_chi": "374 Đ. Lê Văn Sỹ, Phường 14, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.787975448075589, "lng": 106.67796762357317},
    {"ten": "Circle K Viet Nam", "dia_chi": "62 Phạm Ngọc Thạch, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.786197796661169, "lng": 106.69220257953846},
    {"ten": "Circle K Viet Nam", "dia_chi": "43 Phạm Ngọc Thạch, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.784772091273261, "lng": 106.69331714732695},
    {"ten": "Circle K Viet Nam", "dia_chi": "139 Hai Bà Trưng, Phường 6, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.783061472772618, "lng": 106.69755586744603},
    {"ten": "Circle K Viet Nam", "dia_chi": "17 Cao Thắng, Phường 2, Quận 3, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 3", "lat": 10.76895639611068, "lng": 106.68309847654184},
    {"ten": "Circle K Viet Nam", "dia_chi": "106 Hoàng Diệu, Phường 13, Quận 4, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 4", "lat": 10.764061200484743, "lng": 106.7043047849558},
    {"ten": "Circle K Viet Nam", "dia_chi": "95I Bến Vân Đồn, Phường 9, Quận 4, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 4", "lat": 10.761552739595343, "lng": 106.70216602054192},
    {"ten": "Circle K Viet Nam", "dia_chi": "13 Đ. Tôn Đản, Phường 13, Quận 4, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 4", "lat": 10.761519683190455, "lng": 106.70781522988854},
    {"ten": "Circle K Viet Nam", "dia_chi": "37 Thuận Kiều, Phường 12, Quận 5, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 5", "lat": 10.756485982149917, "lng": 106.65812164416158},
    {"ten": "Circle K Nguyễn Kim", "dia_chi": "9 Nguyễn Kim, Phường 12, Quận 5, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 5", "lat": 10.756917483015028, "lng": 106.66293503591902},
    {"ten": "Circle K Viet Nam", "dia_chi": "290C An Dương Vương, Phường 4, Quận 5, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 5", "lat": 10.760266221710578, "lng": 106.68070889534262},
    {"ten": "Circle K Viet Nam", "dia_chi": "81 Đường Trần Bình Trọng, Phường 1, Quận 5, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 5", "lat": 10.754897855682849, "lng": 106.68156067870785},
    {"ten": "Circle K Viet Nam", "dia_chi": "4-6 Đường số 10, Phường 13, Quận 6, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 6", "lat": 10.751676014421287, "lng": 106.62842998985089},
    {"ten": "Circle K Viet Nam", "dia_chi": "18 Bình Phú, Phường 11, Quận 6, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 6", "lat": 10.744806840020471, "lng": 106.63090942941982},
    {"ten": "Circle K Viet Nam", "dia_chi": "5A Đ. Chợ Lớn, Phường 11, Quận 6, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 6", "lat": 10.745939052618134, "lng": 106.63483029469411},
    {"ten": "Circle K Hậu Giang", "dia_chi": "92 Đ. Hậu Giang, Phường 12, Quận 6, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 6", "lat": 10.749791445527016, "lng": 106.64616540842502},
    {"ten": "Circle K Viet Nam", "dia_chi": "Main gate - Cổng chính, 702 Nguyễn Văn Linh, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.729193146286212, "lng": 106.69286043761335},
    {"ten": "Circle K Viet Nam", "dia_chi": "139 Nguyễn Đức Cảnh, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.723994536391857, "lng": 106.70899394778229},
    {"ten": "Circle K Viet Nam", "dia_chi": "402 Hà Huy Tập, Tân Phú, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.726568125308116, "lng": 106.70825858143708},
    {"ten": "Circle K Viet Nam", "dia_chi": "C002 Phạm Thái Bường, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.727464897697123, "lng": 106.71054100893669},
    {"ten": "Circle K Viet Nam", "dia_chi": "15 Bùi Bằng Đoàn, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.729951004561581, "lng": 106.70858572981015},
    {"ten": "Circle K Viet Nam", "dia_chi": "Cảnh Viên 3, SC15, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.722263160992515, "lng": 106.72861428237839},
    {"ten": "Circle K Viet Nam", "dia_chi": "2 Nguyễn Khắc Viện, Tân Phú, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.728519152335556, "lng": 106.71992867601165},
    {"ten": "Circle K Viet Nam", "dia_chi": "12 Tân Trào, Tân Phú, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.729592320080332, "lng": 106.72334554031602},
    {"ten": "Circle K Viet Nam", "dia_chi": "58 Đ. Phạm Văn Nghị, Tân Phong, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.733285432518828, "lng": 106.7065064669082},
    {"ten": "Circle K Viet Nam", "dia_chi": "621 Đ. Nguyễn Thị Thập, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.740093292207296, "lng": 106.70158610432274},
    {"ten": "Circle K Viet Nam", "dia_chi": "459/8A Nguyễn Thị Thập, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.73989830555362, "lng": 106.70399462666099},
    {"ten": "Circle K Viet Nam", "dia_chi": "A24 Đ. D4, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.744887987331936, "lng": 106.6991173304861},
    {"ten": "Circle K Viet Nam", "dia_chi": "Sunrise City View, Tân Hưng, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.74600818568191, "lng": 106.70144804170751},
    {"ten": "Circle K Viet Nam", "dia_chi": "126 Đường Số 15, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.74554995483586, "lng": 106.70589345053025},
    {"ten": "Circle K Viet Nam", "dia_chi": "199 Số 17, Tân Quy, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.744798556010723, "lng": 106.71021361092437},
    {"ten": "Circle K Viet Nam", "dia_chi": "60 Đ. Lâm Văn Bền, Tân Thuận Tây, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.74878005283805, "lng": 106.71573623733892},
    {"ten": "Circle K Viet Nam", "dia_chi": "146 Đ. Lâm Văn Bền, Bình Thuận, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.743052854555833, "lng": 106.71579457846006},
    {"ten": "Circle K Viet Nam", "dia_chi": "45 Đ. Tân Mỹ, Tân Phú, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.736810793693198, "lng": 106.71832666521499},
    {"ten": "Circle K Viet Nam", "dia_chi": "485 Huỳnh Tấn Phát, Tân Thuận Đông, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.745347712978548, "lng": 106.72939127751557},
    {"ten": "Circle K Viet Nam", "dia_chi": "73-75 Trần Trọng Cung, Tân Thuận Đông, Quận 7, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 7", "lat": 10.743758722619496, "lng": 106.73308844422033},
    {"ten": "Circle K Viet Nam", "dia_chi": "A10/7 ấp 2, Bình Hưng, Bình Chánh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Bình Chánh", "lat": 10.727061998543348, "lng": 106.65573465734785},
    {"ten": "Circle K Viet Nam", "dia_chi": "811 Đ. Tạ Quang Bửu, Phường 5, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.736307602282782, "lng": 106.66973824031037},
    {"ten": "Circle K Viet Nam", "dia_chi": "Hẻm 42 Đường 643 Tạ Quang Bửu, Phường 4, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.738416420146912, "lng": 106.6764581841102},
    {"ten": "Circle K Viet Nam", "dia_chi": "277 Âu Dương Lân, Phường Rạch Ông, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.743100798527628, "lng": 106.68464925231353},
    {"ten": "Circle K Viet Nam", "dia_chi": "264–266 Âu Dương Lân, Phường Rạch Ông, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.743803820380206, "lng": 106.68404447744534},
    {"ten": "Circle K Viet Nam", "dia_chi": "141 Âu Dương Lân, Phường Rạch Ông, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.745638954997277, "lng": 106.68326845772755},
    {"ten": "Circle K Viet Nam", "dia_chi": "172 Nguyễn Thị Tần, Phường Rạch Ông, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.745488670027418, "lng": 106.68640820469406},
    {"ten": "Circle K Viet Nam", "dia_chi": "210 - 212 Cao Lỗ, Phường 4, Quận 8, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 8", "lat": 10.73777494630996, "lng": 106.67904053178249},
    {"ten": "Circle K Viet Nam", "dia_chi": "18 Tăng Nhơn Phú, Phước Long B, Quận 9, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 9", "lat": 10.829168317679112, "lng": 106.77345813072378},
    {"ten": "Circle K Viet Nam", "dia_chi": "295 Đ. Đỗ Xuân Hợp, Phước Long B, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thành phố Thủ Đức", "lat": 10.823212609849508, "lng": 106.7702276123061},
    {"ten": "Circle K Man Thiện", "dia_chi": "62 Man Thiện, Hiệp Phú, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thành phố Thủ Đức", "lat": 10.847403561860224, "lng": 106.78707580110316},
    {"ten": "Circle K Lê Văn Việt", "dia_chi": "449 Đ. Lê Văn Việt, Tăng Nhơn Phú A, Thủ Đức, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Thành phố Thủ Đức", "lat": 10.84548571300766, "lng": 106.79375937102041},
    {"ten": "Circle K Viet Nam", "dia_chi": "70 Đ. Đồng Nai, Phường 15, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.779201738703962, "lng": 106.6625416406255},
    {"ten": "Circle K Viet Nam", "dia_chi": "529 Sư Vạn Hạnh, Phường 12, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.77548449238365, "lng": 106.6673516818274},
    {"ten": "Circle K Viet Nam", "dia_chi": "Đại Học Bách Khoa - 268 Lý Thường Kiệt, Phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.772759837325939, "lng": 106.6585197168425},
    {"ten": "Circle K Viet Nam", "dia_chi": "525 Tô Hiến Thành, Phường 14, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.772270689728966, "lng": 106.66050709389363},
    {"ten": "Circle K Viet Nam", "dia_chi": "311 Nguyễn Tri Phương, Phường 8, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.761654717022866, "lng": 106.66830256978315},
    {"ten": "Circle K Viet Nam", "dia_chi": "178A Nguyễn Chí Thanh, Phường 2, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.760494899138367, "lng": 106.67116567004487},
    {"ten": "Circle K Viet Nam", "dia_chi": "297 Nguyễn Duy Dương, Phường 4, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.764382432889386, "lng": 106.67011997960779},
    {"ten": "Circle K Viet Nam", "dia_chi": "2H Trần Nhân Tôn, Phường 2, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.76164730896266, "lng": 106.675060193923},
    {"ten": "Circle K Viet Nam", "dia_chi": "704 Sư Vạn Hạnh, Phường 12, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.77150592982506, "lng": 106.66994475988234},
    {"ten": "Circle K Viet Nam", "dia_chi": "306 Cao Thắng, Phường 12, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.774965271557011, "lng": 106.67477388474924},
    {"ten": "Circle K Viet Nam", "dia_chi": "285/94 Hẻm 285 Cách Mạng Tháng Tám, Quận 10, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 10", "lat": 10.77690058604202, "lng": 106.67771567860835},
    {"ten": "Circle K Viet Nam", "dia_chi": "92B Đ. Hòa Bình, Phú Trung, Quận 11, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 11", "lat": 10.769215950896506, "lng": 106.6379570100426},
    {"ten": "Circle K Viet Nam", "dia_chi": "17K Dương Đình Nghệ, Phường 8, Quận 11, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 11", "lat": 10.760509943132266, "lng": 106.64982158794412},
    {"ten": "Circle K Viet Nam", "dia_chi": "58 Đ. Lữ Gia, Phường 15, Quận 11, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 11", "lat": 10.771094116686578, "lng": 106.65407207105132},
    {"ten": "Circle K Viet Nam", "dia_chi": "150 Nguyễn Thị Nhỏ, Phường 15, Quận 11, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 11", "lat": 10.773848647189473, "lng": 106.65315931167618},
    {"ten": "Circle K Viet Nam", "dia_chi": "319 Lý Thường Kiệt, Phường 15, Quận 11, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 11", "lat": 10.776899032681007, "lng": 106.65456608068754},
    {"ten": "Circle K Trung Mỹ Tây 1", "dia_chi": "15 Nguyễn Ảnh Thủ, Trung Mỹ Tây, Quận 12, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 12", "lat": 10.866354353759098, "lng": 106.61496539489127},
    {"ten": "Circle K Viet Nam", "dia_chi": "474 Trần Thị Năm, Tân Chánh Hiệp, Quận 12, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận 12", "lat": 10.872650110171392, "lng": 106.62238357804333},
    {"ten": "Circle K Nguyễn Chánh Sắt", "dia_chi": "171B Hoàng Hoa Thám, Phường Tân Bình, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.80591090454858, "lng": 106.64657520074633},
    {"ten": "Circle K Viet Nam", "dia_chi": "37 Đường số 9A, Khu dân cư Trung Sơn, Bình Chánh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Bình Chánh", "lat": 10.738563916302, "lng": 106.68986786906257},
    {"ten": "Circle K Viet Nam", "dia_chi": "Cao ốc Chung Cư SaiGon Mia, Đường số 9A, Bình Chánh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Bình Chánh", "lat": 10.733102190705328, "lng": 106.68921048276124},
    {"ten": "Circle K Viet Nam", "dia_chi": "36-38 Trần Thái Tông, Phường 15, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.818591368363347, "lng": 106.63313227895087},
    {"ten": "Circle K Viet Nam", "dia_chi": "135 Nguyễn Cửu Đàm, Tân Sơn Nhì, Quận Tân Phú, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Phú", "lat": 10.79998086022623, "lng": 106.6282052898905},
    {"ten": "Circle K Viet Nam", "dia_chi": "353A Tân Sơn Nhì, Quận Tân Phú, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Phú", "lat": 10.795888348395456, "lng": 106.63014936320437},
    {"ten": "Circle K Yên Thế", "dia_chi": "41 Yên Thế, Phường 2, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.812601323710336, "lng": 106.66826275954038},
    {"ten": "Circle K Phổ Quang", "dia_chi": "04 Phổ Quang, Phường 2, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.803331601781931, "lng": 106.66618984558117},
    {"ten": "Circle K Nguyễn Thái Bình", "dia_chi": "26 Nguyễn Thái Bình, Phường 4, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.799332971925256, "lng": 106.65624528197094},
    {"ten": "Circle K Quách Văn Tuấn", "dia_chi": "6 Quách Văn Tuấn, Phường 12, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.800633101209028, "lng": 106.65247187258461},
    {"ten": "Circle K Viet Nam", "dia_chi": "16 Ấp Bắc, Phường Tân Bình, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.800873469778658, "lng": 106.64155710566136},
    {"ten": "Circle K Đồng Đen", "dia_chi": "80 Đồng Đen, Phường Tân Bình, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.793728227579335, "lng": 106.64455569682528},
    {"ten": "Circle K Viet Nam", "dia_chi": "180 Nguyễn Hồng Đào, Phường Tân Bình, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.792035814617746, "lng": 106.64158098126529},
    {"ten": "Circle K Viet Nam", "dia_chi": "683A Âu Cơ, Tân Thành, Quận Tân Bình, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Bình", "lat": 10.789125483265808, "lng": 106.64003340774471},
    {"ten": "Circle K Vườn Lài", "dia_chi": "304 Vườn Lài, Phú Thọ Hoà, Quận Tân Phú, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Phú", "lat": 10.788166201483243, "lng": 106.6247285667174},
    {"ten": "Circle K Viet Nam", "dia_chi": "21 Thạch Lam, Quận Tân Phú, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Phú", "lat": 10.776318907296845, "lng": 106.63238638937814},
    {"ten": "Circle K Viet Nam", "dia_chi": "RS3 Richstar Residence, Hoà Bình, Quận Tân Phú, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Tân Phú", "lat": 10.772721459982721, "lng": 106.62689697656589},
    {"ten": "Circle K Viet Nam", "dia_chi": "633 TL10, Bình Trị Đông B, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.757986638710422, "lng": 106.61346027108429},
    {"ten": "Circle K Viet Nam", "dia_chi": "160 Đường số 19, Bình Trị Đông B, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.753432142225526, "lng": 106.6129583691167},
    {"ten": "Circle K Viet Nam", "dia_chi": "259 Đường số 7, Bình Trị Đông B, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.751493684801632, "lng": 106.61305975971003},
    {"ten": "Circle K Viet Nam", "dia_chi": "193 Đường số 1, Bình Trị Đông B, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.74833329119696, "lng": 106.61633254126637},
    {"ten": "Circle K Bến xe Miền Tây", "dia_chi": "395 Kinh Dương Vương, An Lạc, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.74071466411383, "lng": 106.61818557914934},
    {"ten": "Circle K Viet Nam", "dia_chi": "74 Đường số 1, Bình Trị Đông B, Quận Bình Tân, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Tân", "lat": 10.748523768495843, "lng": 106.61856212148409},
    {"ten": "Circle K Viet Nam", "dia_chi": "1 Đường số 1, Phường 5, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Gò Vấp", "lat": 10.824981567277183, "lng": 106.69362135162257},
    {"ten": "Circle K Viet Nam", "dia_chi": "188 Phan Văn Trị, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.814102166333063, "lng": 106.69534926163317},
    {"ten": "Circle K Nguyễn Xí", "dia_chi": "184A Nguyễn Xí, Phường 26, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.815230342397827, "lng": 106.70794710680784},
    {"ten": "Circle K Viet Nam", "dia_chi": "190 Phan Văn Trị, Phường 11, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.813301485827605, "lng": 106.69534023333973},
    {"ten": "Circle K Viet Nam", "dia_chi": "22L Vũ Huy Tấn, Phường 7, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.796044405363471, "lng": 106.69249366015055},
    {"ten": "Circle K Bùi Hữu Nghĩa", "dia_chi": "315B Bùi Hữu Nghĩa, Phường 1, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.799784593145638, "lng": 106.69942835560664},
    {"ten": "Circle K Viet Nam", "dia_chi": "609 Xô Viết Nghệ Tĩnh, Phường 26, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.810905400856635, "lng": 106.71338803972},
    {"ten": "Circle K Viet Nam", "dia_chi": "14 Ung Văn Khiêm, Phường 25, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.8094578016459, "lng": 106.71290490370535},
    {"ten": "Circle K Viet Nam", "dia_chi": "17 D5, Phường 25, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.806531235658136, "lng": 106.71351058565367},
    {"ten": "Circle K Viet Nam", "dia_chi": "197 Điện Biên Phủ, Phường 2, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.800210351702244, "lng": 106.70668610075523},
    {"ten": "Circle K Viet Nam", "dia_chi": "292 Điện Biên Phủ, Phường 17, Bình Thạnh, Thành phố Hồ Chí Minh, Việt Nam", "quan": "Quận Bình Thạnh", "lat": 10.799397092974557, "lng": 106.70685715523412},
    {"ten": "Circle K Viet Nam", "dia_chi": "113 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.80442436756612, "lng": 106.71570564182744},
    {"ten": "Circle K Viet Nam", "dia_chi": "27 Nguyễn Gia Trí, Phường 25, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.802282557508317, "lng": 106.71546649189023},
    {"ten": "Circle K Viet Nam", "dia_chi": "475 Điện Biên Phủ, Phường 25, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.801540200079494, "lng": 106.71446189325134},
    {"ten": "Circle K Viet Nam", "dia_chi": "74 Nguyễn Văn Thương, Phường 25, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.80187717905782, "lng": 106.71919740942653},
    {"ten": "Circle K Công Trường Tự Do", "dia_chi": "1 Công Trường Tự Do, Phường 19, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.792125882272659, "lng": 106.70902330817977},
    {"ten": "Circle K Viet Nam", "dia_chi": "92 Nguyễn Hữu Cảnh, Phường 22, Quận Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.790503189126118, "lng": 106.71858617940435},
    {"ten": "Circle K Viet Nam", "dia_chi": "720A Điện Biên Phủ, Vinhomes Tân Cảng, Bình Thạnh, TP.HCM", "quan": "Quận Bình Thạnh", "lat": 10.795112326971134, "lng": 106.72209314387317},

    {"ten": "Circle K Viet Nam", "dia_chi": "416 Phan Huy Ích, Phường 12, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.84209769350501, "lng": 106.6388344043623},
    {"ten": "Circle K Viet Nam", "dia_chi": "27 Phạm Văn Chiêu, Phường 8, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.844820420859163, "lng": 106.64089066006575},
    {"ten": "Circle K Viet Nam", "dia_chi": "309 Nguyễn Văn Khối, Phường 8, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.843409008448196, "lng": 106.65050801782208},
    {"ten": "Circle K Viet Nam", "dia_chi": "271 Lê Văn Thọ, Phường 8, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.844453853169862, "lng": 106.65695296197357},
    {"ten": "Circle K Viet Nam", "dia_chi": "190 Lê Văn Thọ, Phường 11, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.842361502290967, "lng": 106.65726852807792},
    {"ten": "Circle K Viet Nam", "dia_chi": "469 Thống Nhất, Phường 16, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.845570656944718, "lng": 106.66467058373988},
    {"ten": "Circle K Viet Nam", "dia_chi": "586–588 Quang Trung, Phường 11, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.83567779654522, "lng": 106.661840906225},
    {"ten": "Circle K Viet Nam", "dia_chi": "619 Lê Đức Thọ, Phường 16, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.847527960291215, "lng": 106.66870145722856},
    {"ten": "Circle K Viet Nam", "dia_chi": "184 Lê Đức Thọ, Phường 6, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.83663845002905, "lng": 106.68108117580447},
    {"ten": "Circle K Viet Nam", "dia_chi": "128 Lê Đức Thọ, Phường 6, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.834635067589021, "lng": 106.68171597863574},
    {"ten": "Circle K Viet Nam", "dia_chi": "67 Lê Đức Thọ, Phường 1, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.832008682220215, "lng": 106.68251012243434},
    {"ten": "Circle K Dương Quảng Hàm", "dia_chi": "Dương Quảng Hàm, Phường 5, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.832648781795902, "lng": 106.6859066437226},
    {"ten": "Circle K Viet Nam", "dia_chi": "29 Lê Lợi, Phường 1, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.820671343047856, "lng": 106.68734766504352},

    {"ten": "Circle K Emart", "dia_chi": "Phường 5, Quận Gò Vấp, TP.HCM", "quan": "Quận Gò Vấp", "lat": 10.823845937884547, "lng": 106.69214359362027},

    {"ten": "Circle K Phan Xích Long", "dia_chi": "502 Phan Xích Long, Phường 4, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.802813673932523, "lng": 106.6821106796099},
    {"ten": "Circle K Viet Nam", "dia_chi": "58–60 Hoa Cúc, Phường 7, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.7984455418253, "lng": 106.68916882116812},
    {"ten": "Circle K Viet Nam", "dia_chi": "220 Nguyễn Trọng Tuyển, Phường 8, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.797920967376657, "lng": 106.673741372315},
    {"ten": "Circle K Viet Nam", "dia_chi": "135 Lê Văn Sỹ, Phường 13, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.791658637080772, "lng": 106.67160229647817},
    {"ten": "Circle K Viet Nam", "dia_chi": "103 Trần Huy Liệu, Phường 11, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.793287714922167, "lng": 106.67781513633643},
    {"ten": "Circle K Viet Nam", "dia_chi": "44 Huỳnh Văn Bánh, Phường 15, Quận Phú Nhuận, TP.HCM", "quan": "Quận Phú Nhuận", "lat": 10.795086311545738, "lng": 106.68130650564632},
    
]

# ======================================================================
# 2) DANH SACH GS25 (HCMC)
# ======================================================================
gs_stores_data = [
    {"ten": "GS25", "dia_chi": "447 Tô Hiến Thành, Phường 14, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.774837539446306, "lng": 106.66258963153344},
    {"ten": "GS25 Hoàng Dư Khương", "dia_chi": "01 Hoàng Dư Khương, Phường 12, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.775227788093778, "lng": 106.67185283526224},
    {"ten": "GS25 Bà Hạt", "dia_chi": "172 Bà Hạt, Phường 9, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.766610370625989, "lng": 106.67102776471002},
    {"ten": "GS25 Cửu Long", "dia_chi": "44 Cửu Long, Cư xá Bắc Hải, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.781568546788272, "lng": 106.66237986471002},
    {"ten": "GS25 Thành Thái", "dia_chi": "81 Thành Thái, Phường 14, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.773326611899995, "lng": 106.66458508863558},
    {"ten": "GS25 Sư Vạn Hạnh", "dia_chi": "553 Sư Vạn Hạnh, Phường 12, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.77588193409698, "lng": 106.66704795244108},
    {"ten": "GS25 Viet Nam", "dia_chi": "106 Nguyễn Giản Thanh, Phường 15, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.783688770644691, "lng": 106.66266872360556},
    {"ten": "GS25 Vĩnh Viễn", "dia_chi": "30 Vĩnh Viễn, Phường 2, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.765274736107543, "lng": 106.6739531570311},
    {"ten": "GS25 Đồng Nai", "dia_chi": "37 Đồng Nai, Phường 15, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.782460593566766, "lng": 106.66071054721115},
    {"ten": "GS25 Viettel", "dia_chi": "Tòa nhà Viettel, Hẻm 285 Cách Mạng Tháng 8, Phường 12, Quận 10, TP.HCM", "quan": "Quận 10", "lat": 10.778332393611949, "lng": 106.67999602942002},

    {"ten": "GS25 Trương Định", "dia_chi": "24C Trương Định, Phường 6, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.778711529532137, "lng": 106.68892590968956},
    {"ten": "GS25 UEH Nguyễn Đình Chiểu", "dia_chi": "130 Nguyễn Đình Chiểu, Phường 6, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.783900170644905, "lng": 106.69502449415782},
    {"ten": "GS25 Nam Kỳ Khởi Nghĩa", "dia_chi": "155A Nam Kỳ Khởi Nghĩa, Phường 6, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.782063620216261, "lng": 106.6919920536656},
    {"ten": "GS25 Cách Mạng Tháng 8", "dia_chi": "598-600 Cách Mạng Tháng 8, Phường 11, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.786413649981403, "lng": 106.66577872605457},
    {"ten": "GS25 Trần Cao Vân", "dia_chi": "42 Trần Cao Vân, Phường 6, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.783111388067901, "lng": 106.69621363526223},
    {"ten": "GS25 Nguyễn Thị Minh Khai", "dia_chi": "454 Nguyễn Thị Minh Khai, Phường 5, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.768585470628146, "lng": 106.68444146471},
    {"ten": "GS25 Cao Thắng", "dia_chi": "25A Cao Thắng, Phường 2, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.769251705597895, "lng": 106.68279042360558},

    {"ten": "GS25 Hai Bà Trưng", "dia_chi": "138-142 Hai Bà Trưng, Phường Đa Kao, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.78441540548176, "lng": 106.69660219415779},
    {"ten": "GS25 More Building", "dia_chi": "520 Cách Mạng Tháng 8, Phường 11, Quận 3, TP.HCM", "quan": "Quận 3", "lat": 10.785536375126169, "lng": 106.66764401747112},
    {"ten": "GS25 Lê Thánh Tôn", "dia_chi": "2 Lê Thánh Tôn, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.78227858807062, "lng": 106.70597736471004},
    {"ten": "GS25 Nguyễn Công Trứ", "dia_chi": "79 Nguyễn Công Trứ, Phường Nguyễn Thái Bình, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.76949738811258, "lng": 106.70291689415778},
    {"ten": "GS25 Cống Quỳnh", "dia_chi": "189/09 Cống Quỳnh, Phường Nguyễn Cư Trinh, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.767297588119805, "lng": 106.6866948941578},
    {"ten": "GS25 Phó Đức Chính", "dia_chi": "41 Phó Đức Chính, Phường Nguyễn Thái Bình, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.768318288116445, "lng": 106.70077313526225},
    {"ten": "GS25 Hai Bà Trưng Bến Nghé", "dia_chi": "62 Hai Bà Trưng, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.777336168955559, "lng": 106.70439865182885},
    {"ten": "GS25 Trương Định Bến Thành", "dia_chi": "52 Trương Định, Phường Bến Thành, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.772554520034788, "lng": 106.69589069232103},
    {"ten": "GS25 Lý Tự Trọng", "dia_chi": "172 Lý Tự Trọng, Phường Bến Thành, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.77317484355821, "lng": 106.69579353464998},
    {"ten": "GS25 Phạm Ngọc Thạch", "dia_chi": "1A Phạm Ngọc Thạch, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.781374070642133, "lng": 106.69695543526224},
    {"ten": "GS25 Đề Thám", "dia_chi": "270 Đề Thám, Phường Phạm Ngũ Lão, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.768475288115921, "lng": 106.69360366471001},
    {"ten": "GS25 Trần Nhật Duật", "dia_chi": "49 Trần Nhật Duật, Phường Tân Định, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.793909329344137, "lng": 106.6895729242178},
    {"ten": "GS25 Phan Chu Trinh", "dia_chi": "41 Phan Chu Trinh, Phường Bến Thành, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.77254066794064, "lng": 106.69719672975691},
    {"ten": "GS25 Hồ Tùng Mậu", "dia_chi": "63 Hồ Tùng Mậu, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.771773429368372, "lng": 106.70383826471003},

    {"ten": "GS25 IBC Building", "dia_chi": "1A Công Trường Mê Linh, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.776083264272911, "lng": 106.70643962360558},
    {"ten": "GS25 Hai Bà Trưng Tân Định", "dia_chi": "254 Hai Bà Trưng, Phường Tân Định, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.788663285571138, "lng": 106.69111511992013},
    {"ten": "GS25 Aqua 1 Vinhomes", "dia_chi": "A1 Vinhomes Golden River, 2 Tôn Đức Thắng, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.786539046761058, "lng": 106.71086462360556},
    {"ten": "GS25 Tôn Đức Thắng", "dia_chi": "2A-4A Tôn Đức Thắng, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.778287305528712, "lng": 106.70657336471001},
    {"ten": "GS25 Deutsches Haus", "dia_chi": "20 Lê Văn Hưu, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.781963170642781, "lng": 106.70115286471002},
    {"ten": "GS25 Trần Quang Khải", "dia_chi": "116-118 Trần Quang Khải, Phường Tân Định, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.79227807065408, "lng": 106.69238236471003},
    {"ten": "GS25 Mplaza", "dia_chi": "39 Lê Duẩn, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.781594229357708, "lng": 106.70027886471033},
    {"ten": "GS25 Bùi Viện", "dia_chi": "240 Bùi Viện, Phường Phạm Ngũ Lão, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.765892846874001, "lng": 106.69086040581446},
    {"ten": "GS25 Lê Lai", "dia_chi": "78 Lê Lai, Phường Bến Thành, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.773205888100424, "lng": 106.69961130581447},
    {"ten": "GS25 Nowzone", "dia_chi": "235 Nguyễn Văn Cừ, Phường Nguyễn Cư Trinh, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.764480088129032, "lng": 106.68226446471002},

    {"ten": "GS25 Japanese Town", "dia_chi": "17/2 Lê Thánh Tôn, Phường Bến Nghé, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.780119864233146, "lng": 106.70458522360556},
    {"ten": "GS25 DH Hoa Sen", "dia_chi": "8 Nguyễn Văn Tráng, Phường Phạm Ngũ Lão, Quận 1, TP.HCM", "quan": "Quận 1", "lat": 10.770256364330274, "lng": 106.69249706471},
    {"ten": "GS25 Saigon Royal", "dia_chi": "34-35 Bến Vân Đồn, Phường 12, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.766866446868661, "lng": 106.70387953526223},
    {"ten": "GS25 Nguyễn Hữu Cảnh", "dia_chi": "135/57 Nguyễn Hữu Cảnh, Phường 22, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.79687292429312, "lng": 106.71764993784423},
    {"ten": "GS25 Đặng Thuỳ Trâm", "dia_chi": "98A Đặng Thuỳ Trâm, Phường 13, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.828436446531214, "lng": 106.70313120581444},
    {"ten": "GS25 Pearl Plaza", "dia_chi": "561A Điện Biên Phủ, Phường 25, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.798765, "lng": 106.713456},
    {"ten": "GS25 City Garden", "dia_chi": "59 Ngô Tất Tố, Phường 21, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.791234, "lng": 106.711234},
    {"ten": "GS25 Nguyễn Văn Thương", "dia_chi": "150 Nguyễn Văn Thương, Phường 25, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.802962446671067, "lng": 106.72010946471},
    {"ten": "GS25 Ung Văn Khiêm", "dia_chi": "226 Ung Văn Khiêm, Phường 25, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.805037295929095, "lng": 106.72105305735109},
    {"ten": "GS25 Huỳnh Đình Hai", "dia_chi": "38A Huỳnh Đình Hai, Phường 14, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.80453240532743, "lng": 106.69923886471001},
    {"ten": "GS25 Điện Biên Phủ UEF", "dia_chi": "141 Điện Biên Phủ, Phường 2, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.79743734670136, "lng": 106.70336242360558},
    {"ten": "GS25 D5 Bình Thạnh", "dia_chi": "47A D5, Phường 25, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.806273782139193, "lng": 106.71461759538228},
    {"ten": "GS25 Đại Học Hồng Bàng", "dia_chi": "215 Điện Biên Phủ, Phường 2, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.79980632933767, "lng": 106.70628933526226},
    {"ten": "GS25 Phan Văn Trị BT", "dia_chi": "188E Phan Văn Trị, Phường 11, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.813859587966746, "lng": 106.69537016471003},
    {"ten": "GS25 Phan Đăng Lưu", "dia_chi": "49L Phan Đăng Lưu, Phường 3, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.803221994662554, "lng": 106.69091028863559},

    {"ten": "GS25 Park 1 Vinhomes", "dia_chi": "720A Điện Biên Phủ, Vinhomes Tân Cảng, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.791538305427142, "lng": 106.72146959415781},
    {"ten": "GS25 Hutech", "dia_chi": "Ung Văn Khiêm, Phường 25, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.809454204319003, "lng": 106.71502283096454},
    {"ten": "GS25 Văn Lang University", "dia_chi": "69 Trục, Phường 13, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.827061970692244, "lng": 106.69902296471001},
    {"ten": "GS25 Bùi Hữu Nghĩa", "dia_chi": "270 Bùi Hữu Nghĩa, Phường 2, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.799045724357708, "lng": 106.69951965305334},
    {"ten": "GS25 Sunwah Pearl", "dia_chi": "90 Nguyễn Hữu Cảnh, Phường 22, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.788789711950777, "lng": 106.71770722360554},
    {"ten": "GS25 Opal Tower", "dia_chi": "92 Nguyễn Hữu Cảnh, Phường 22, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.789509046744787, "lng": 106.71828086471001},
    {"ten": "GS25 Bạch Đằng BT", "dia_chi": "145 Bạch Đằng, Phường 2, Bình Thạnh, TP.HCM", "quan": "Bình Thạnh", "lat": 10.802886174997607, "lng": 106.70855852299428},

    {"ten": "GS25 Saigon Royal Q4", "dia_chi": "35 Bến Vân Đồn, Phường 12, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.7668664, "lng": 106.7038795},
    {"ten": "GS25 Khánh Hội", "dia_chi": "262 Khánh Hội, Phường 5, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.759608953040583, "lng": 106.69870958832456},
    {"ten": "GS25 Đường Số 41 Q4", "dia_chi": "39 Đường số 41, Phường 9, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.758836910439117, "lng": 106.70063487461782},
    {"ten": "GS25 Tôn Đản", "dia_chi": "23 Tôn Đản, Phường 13, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.761363500504565, "lng": 106.70774132490254},
    {"ten": "GS25 REE Tower", "dia_chi": "9 Đoàn Văn Bơ, Phường 13, Quận 4, TP.HCM", "quan": "Quận 4", "lat": 10.764895394538556, "lng": 106.70259407583036},

    {"ten": "GS25 Trung Sơn", "dia_chi": "53 Đường 9A, Trung Sơn, Bình Chánh, TP.HCM", "quan": "Bình Chánh", "lat": 10.737964170594733, "lng": 106.68981203526224},
    {"ten": "GS25 Mizuki Park", "dia_chi": "Mizuki Park, Bình Hưng, Bình Chánh, TP.HCM", "quan": "Bình Chánh", "lat": 10.714084947156472, "lng": 106.66500100581446},
    {"ten": "GS25 Calla Garden", "dia_chi": "13C Nguyễn Văn Linh, Phong Phú, Bình Chánh, TP.HCM", "quan": "Bình Chánh", "lat": 10.712328429121635, "lng": 106.64549723087538},

    {"ten": "GS25 Cao Lỗ", "dia_chi": "196 Cao Lỗ, Phường 4, Quận 8, TP.HCM", "quan": "Quận 8", "lat": 10.738874636637032, "lng": 106.67845192176885},
    {"ten": "GS25 Phạm Đức Sơn", "dia_chi": "238 Phạm Đức Sơn, Phường 16, Quận 8, TP.HCM", "quan": "Quận 8", "lat": 10.724834805937176, "lng": 106.62295261133666},
    {"ten": "GS25 Diamond Lotus", "dia_chi": "49C Lê Quang Kim, Phường 8, Quận 8, TP.HCM", "quan": "Quận 8", "lat": 10.74794711008128, "lng": 106.67680383124156},
    {"ten": "GS25 Nguyễn Trãi Q5", "dia_chi": "706 Nguyễn Trãi, Phường 11, Quận 5, TP.HCM", "quan": "Quận 5", "lat": 10.753190429388672, "lng": 106.66153169415783},
    {"ten": "GS25 Nguyễn Chí Thanh Q5", "dia_chi": "133A Nguyễn Chí Thanh, Phường 9, Quận 5, TP.HCM", "quan": "Quận 5", "lat": 10.759237607148657, "lng": 106.66750409437138},
    {"ten": "GS25 Nguyễn Văn Cừ Q5", "dia_chi": "217A Nguyễn Văn Cừ, Phường 4, Quận 5, TP.HCM", "quan": "Quận 5", "lat": 10.762093347673172, "lng": 106.68272402509655},

    {"ten": "GS25 Bình Phú", "dia_chi": "3E Cư Xá Phú Lâm D, Quận 6, TP.HCM", "quan": "Quận 6", "lat": 10.739054052979524, "lng": 106.62928934078444},
    {"ten": "GS25 Hậu Giang Q6", "dia_chi": "18 Hậu Giang, Phường 12, Quận 6, TP.HCM", "quan": "Quận 6", "lat": 10.745597576381812, "lng": 106.63684162942008},
    {"ten": "GS25 Minh Phụng", "dia_chi": "174 Minh Phụng, Phường 6, Quận 6, TP.HCM", "quan": "Quận 6", "lat": 10.75212492584987, "lng": 106.6430559560667},
    {"ten": "GS25 Viva Q6", "dia_chi": "1472 Võ Văn Kiệt, Phường 1, Quận 6, TP.HCM", "quan": "Quận 6", "lat": 10.74335682857572, "lng": 106.64681131332004},

    {"ten": "GS25 Tạ Quang Bửu", "dia_chi": "852 Tạ Quang Bửu, Phường 5, Quận 8, TP.HCM", "quan": "Quận 8", "lat": 10.737046279159161, "lng": 106.67037859373006},
    {"ten": "GS25 Diamond Lotus Q8", "dia_chi": "49C Lê Quang Kim, Phường 8, Quận 8, TP.HCM", "quan": "Quận 8", "lat": 10.74794711008128, "lng": 106.67680383124156},

    {"ten": "GS25 3 Tháng 2 Q11", "dia_chi": "1339 Đường 3 Tháng 2, Quận 11, TP.HCM", "quan": "Quận 11", "lat": 10.757918256176369, "lng": 106.64934714007248},
    {"ten": "GS25 Nguyễn Thị Nhỏ", "dia_chi": "142 Nguyễn Thị Nhỏ, Quận 11, TP.HCM", "quan": "Quận 11", "lat": 10.773535303338113, "lng": 106.6531093932981},

    {"ten": "GS25 Tô Ký Q12", "dia_chi": "260 Tô Ký, Trung Mỹ Tây, Quận 12, TP.HCM", "quan": "Quận 12", "lat": 10.863521692230757, "lng": 106.61648931646357},
    {"ten": "GS25 Nguyễn Ảnh Thủ", "dia_chi": "52 Nguyễn Ảnh Thủ, Hiệp Thành, Quận 12, TP.HCM", "quan": "Quận 12", "lat": 10.879797673513888, "lng": 106.63551081923553},
    {"ten": "GS25 PiCity High Park", "dia_chi": "35 Đường N1, Quận 12, TP.HCM", "quan": "Quận 12", "lat": 10.86547372154861, "lng": 106.66360741784436},

    {"ten": "GS25 Âu Cơ", "dia_chi": "605 Âu Cơ, Phú Trung, Tân Phú, TP.HCM", "quan": "Tân Phú", "lat": 10.784097289210072, "lng": 106.64211904686273},
    {"ten": "GS25 Bình Long", "dia_chi": "418 Bình Long, Tân Quý, Tân Phú, TP.HCM", "quan": "Tân Phú", "lat": 10.788684488049606, "lng": 106.61732549415781},
    {"ten": "GS25 Văn Cao", "dia_chi": "130A Lê Vĩnh Hòa, Tân Phú, TP.HCM", "quan": "Tân Phú", "lat": 10.7867585119441, "lng": 106.62228069415782},

    {"ten": "GS25 Phạm Văn Chiêu", "dia_chi": "6C Phạm Văn Chiêu, Gò Vấp, TP.HCM", "quan": "Gò Vấp", "lat": 10.84504372928796, "lng": 106.64186706471001},
    {"ten": "GS25 Lê Đức Thọ GV", "dia_chi": "507 Lê Đức Thọ, Gò Vấp, TP.HCM", "quan": "Gò Vấp", "lat": 10.845573311799152, "lng": 106.67147328938024},
    {"ten": "GS25 Nguyễn Văn Công", "dia_chi": "498 Nguyễn Văn Công, Gò Vấp, TP.HCM", "quan": "Gò Vấp", "lat": 10.817818934626208, "lng": 106.67599746323415},

    {"ten": "GS25 Nguyễn Văn Trỗi", "dia_chi": "251 Nguyễn Văn Trỗi, Phú Nhuận, TP.HCM", "quan": "Phú Nhuận", "lat": 10.79650227690623, "lng": 106.67365362565914},
    {"ten": "GS25 Huỳnh Văn Bánh", "dia_chi": "511 Huỳnh Văn Bánh, Phú Nhuận, TP.HCM", "quan": "Phú Nhuận", "lat": 10.791494537490504, "lng": 106.6695043795582},

    {"ten": "GS25 Akari City", "dia_chi": "77 Võ Văn Kiệt, Bình Tân, TP.HCM", "quan": "Bình Tân", "lat": 10.718011799162191, "lng": 106.60740820294878},

    {"ten": "GS25 Trung Sơn NB", "dia_chi": "12 Nguyễn Hữu Thọ, Nhà Bè, TP.HCM", "quan": "Nhà Bè", "lat": 10.712289888299738, "lng": 106.70725033526224},

    {"ten": "GS25 Becamex Tower", "dia_chi": "Đại lộ Bình Dương, Thủ Dầu Một, Bình Dương", "quan": "Bình Dương", "lat": 10.976381686000932, "lng": 106.67058253564757},
    {"ten": "GS25 Đại Học Thủ Dầu Một", "dia_chi": "6 Trần Văn Ơn, Thủ Dầu Một, Bình Dương", "quan": "Bình Dương", "lat": 10.9757378838103, "lng": 106.67507282947938},
]

# Tao cua hang
create_batch_stores(ck_stores_data, ck_chain)
create_batch_stores(gs_stores_data, gs_chain)

print("\nHOAN THANH: Da tao xong danh sach cua hang.")


# ======================================================================
# PHAN 2: TAO NHAN VIEN
# ======================================================================
print("\n--- DANG TAO NHAN VIEN (TOI DA 10 / CUA HANG) ---")

import random
from gis_store.models import CuaHang, NhanVien

ho = ["Nguyen", "Tran", "Le", "Pham", "Huynh", "Hoang", "Phan", "Vu", "Vo", "Dang", "Bui", "Do"]
lot = ["Thi", "Van", "Minh", "Ngoc", "Thanh", "Duc", "Huu", "Gia", "Xuan", "Thu", "Tan"]
ten = ["An", "Binh", "Cuong", "Dung", "Em", "Giang", "Han", "Khanh", "Long", "Mai", "Nhung", "Phuc", "Quan", "Trang", "Uyen", "Vy"]

chuc_vu_list = [
    "Nhân viên bán hàng",
    "Nhân viên Part-time",
    "Nhân viên kho",
]

# ====== MẪU ĐỊA CHỈ CHI TIẾT (thật hơn) ======
quan_phuong_duong = {
    "Quận 1": {
        "Phường Bến Nghé": ["Lê Thánh Tôn", "Nguyễn Huệ", "Tôn Đức Thắng", "Đồng Khởi"],
        "Phường Bến Thành": ["Lê Lai", "Trương Định", "Lý Tự Trọng", "Phạm Ngũ Lão"],
        "Phường Nguyễn Thái Bình": ["Nguyễn Công Trứ", "Hồ Tùng Mậu", "Phó Đức Chính"],
    },
    "Quận 3": {
        "Phường 6": ["Nguyễn Đình Chiểu", "Trần Cao Vân", "Trương Định"],
        "Phường 5": ["Nguyễn Thị Minh Khai", "Cao Thắng", "Điện Biên Phủ"],
        "Phường 11": ["Cách Mạng Tháng Tám", "Nguyễn Văn Trỗi"],
    },
    "Quận 7": {
        "Tân Phong": ["Nguyễn Hữu Thọ", "Lê Văn Lương", "Nguyễn Văn Linh"],
        "Tân Quy": ["Đường Số 17", "Đường Số 79", "Nguyễn Thị Thập"],
        "Phú Mỹ": ["Huỳnh Tấn Phát", "Đào Trí", "Hoàng Quốc Việt"],
    },
    "Bình Thạnh": {
        "Phường 25": ["Ung Văn Khiêm", "D5", "Điện Biên Phủ"],
        "Phường 22": ["Nguyễn Hữu Cảnh", "Điện Biên Phủ"],
        "Phường 11": ["Phan Văn Trị", "Chu Văn An"],
    },
    "Tân Bình": {
        "Phường 12": ["Cộng Hòa", "Trường Chinh", "Hoàng Văn Thụ"],
        "Phường 11": ["Lý Thường Kiệt", "Bàu Cát"],
        "Phường 8": ["Cách Mạng Tháng Tám", "Lạc Long Quân"],
    },
    "Gò Vấp": {
        "Phường 7": ["Phan Văn Trị", "Nguyễn Oanh"],
        "Phường 16": ["Lê Đức Thọ", "Thống Nhất"],
        "Phường 5": ["Quang Trung", "Phạm Văn Chiêu"],
    },
    "Thủ Đức": {
        "Bình An": ["Lương Định Của", "Mai Chí Thọ"],
        "Hiệp Bình Chánh": ["Phạm Văn Đồng", "Quốc Lộ 13"],
        "Linh Trung": ["Kha Vạn Cân", "Hoàng Diệu 2"],
    },
}

def tao_sdt():
    # 09xxxxxxxx hoặc 03xxxxxxxx (nhìn giống số thật VN hơn)
    dau = random.choice(["09", "03", "07", "08", "05"])
    return dau + "".join(random.choices("0123456789", k=8))

def tao_email(ho_ten):
    slug = ho_ten.lower().replace(" ", "")
    return f"{slug}{random.randint(10,999)}@store.vn"

def tao_dia_chi_chi_tiet():
    quan = random.choice(list(quan_phuong_duong.keys()))
    phuong = random.choice(list(quan_phuong_duong[quan].keys()))
    duong = random.choice(quan_phuong_duong[quan][phuong])

    so_nha = random.randint(1, 399)
    # 30% có dạng hẻm cho giống thực tế
    if random.random() < 0.3:
        hem = random.randint(1, 300)
        dia_chi = f"{hem}/{so_nha} {duong}, {phuong}, {quan}, TP.HCM"
    else:
        dia_chi = f"{so_nha} {duong}, {phuong}, {quan}, TP.HCM"

    return dia_chi

all_stores = CuaHang.objects.all()
count_nv = 0

for store in all_stores:
    current = NhanVien.objects.filter(cua_hang=store).count()
    if current >= 10:
        continue

    # đảm bảo có cửa hàng trưởng
    if not NhanVien.objects.filter(cua_hang=store, chuc_vu="Cửa hàng trưởng").exists():
        name = f"{random.choice(ho)} {random.choice(lot)} {random.choice(ten)}"
        NhanVien.objects.create(
            cua_hang=store,
            ho_ten=name,
            chuc_vu="Cửa hàng trưởng",
            so_dien_thoai=tao_sdt(),
            email=tao_email(name),
            dia_chi=tao_dia_chi_chi_tiet(),
        )
        count_nv += 1
        current += 1

    # tạo thêm cho đủ 10
    for _ in range(10 - current):
        name = f"{random.choice(ho)} {random.choice(lot)} {random.choice(ten)}"
        NhanVien.objects.create(
            cua_hang=store,
            ho_ten=name,
            chuc_vu=random.choice(chuc_vu_list),
            so_dien_thoai=tao_sdt(),
            email=tao_email(name),
            dia_chi=tao_dia_chi_chi_tiet(),
        )
        count_nv += 1

print(f"-> Đã tạo {count_nv} nhân viên.")

# ======================================================================
# PHAN 3: TAO KHUYEN MAI + GAN VAO CUA HANG/THUONG HIEU
# ======================================================================
print("\n--- DANG TAO KHUYEN MAI ---")

km_ck_1, _ = KhuyenMai.objects.get_or_create(
    ten="Combo Than Thanh: Mi Tron + Pepsi",
    defaults={
        "mo_ta": "Mua 1 Mi tron Indomie + 1 Pepsi 320ml giam 5.000d. Ap dung toan he thong."
    },
)
km_ck_2, _ = KhuyenMai.objects.get_or_create(
    ten="Mua 2 Tang 1: Froster Cau Vong",
    defaults={"mo_ta": "Mua 2 ly Froster size L tang 1 ly size M."},
)

brand_indomie = ThuongHieu.objects.filter(ten__icontains="Indomie").first()
brand_pepsi = ThuongHieu.objects.filter(ten__icontains="Pepsi").first()
brand_ck = ThuongHieu.objects.filter(ten__icontains="Circle K").first()

if brand_indomie:
    km_ck_1.thuong_hieu.add(brand_indomie)
if brand_pepsi:
    km_ck_1.thuong_hieu.add(brand_pepsi)
if brand_ck:
    km_ck_2.thuong_hieu.add(brand_ck)

ck_stores = list(CuaHang.objects.filter(chuoi__ten="Circle K"))
km_ck_1.cua_hang.set(ck_stores)
km_ck_2.cua_hang.set(ck_stores[: max(1, len(ck_stores) // 2)])


km_gs_1, _ = KhuyenMai.objects.get_or_create(
    ten="Mua 1 Tang 1: Dong san pham Youus",
    defaults={"mo_ta": "Mua 1 tang 1 ap dung cho mot so san pham Youus."},
)
km_gs_2, _ = KhuyenMai.objects.get_or_create(
    ten="Combo Han Quoc: Tokbokki + Nuoc suoi",
    defaults={"mo_ta": "Giam 10% khi mua Tokbokki ly kem nuoc suoi Dasani."},
)

brand_youus = ThuongHieu.objects.filter(ten__icontains="Youus").first()
brand_gs = ThuongHieu.objects.filter(ten__icontains="GS25").first()

if brand_youus:
    km_gs_1.thuong_hieu.add(brand_youus)
if brand_gs:
    km_gs_2.thuong_hieu.add(brand_gs)

gs_stores = list(CuaHang.objects.filter(chuoi__ten="GS25"))
km_gs_1.cua_hang.set(gs_stores)
km_gs_2.cua_hang.set(gs_stores)

print("-> Da tao xong khuyen mai va gan vao cua hang/thuong hieu.")
print("\n=============================================")
print("CHUC MUNG! DU LIEU DA SEED DAY DU.")
print("=============================================")
