from django.contrib import admin

# Register your models here.
from .models import (
    ThuongHieu,
    NhaCungCap,
    NhomSanPham,
    SanPham,
    ChuoiCuaHang,
    CuaHang,
    NhanVien,
    KhuyenMai,
)
@admin.register(ChuoiCuaHang)
class ChuoiCuaHangAdmin(admin.ModelAdmin):
    list_display = ("ten",)

    class Media:
        js = ("admin/image_preview.js",)
@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ("ten", "thuong_hieu", "nha_cung_cap", "nhom_san_pham")
    list_filter = ("thuong_hieu", "nha_cung_cap", "nhom_san_pham")
    class Media:
        js = ("admin/image_preview.js",)
        
@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    
    class Media:
        js = ("admin/image_preview.js",)
        
admin.site.register(ThuongHieu)
admin.site.register(NhaCungCap)
admin.site.register(NhomSanPham)


admin.site.register(CuaHang)

admin.site.register(KhuyenMai)

# from django.contrib.auth.models import User, Group
# admin.site.unregister(User)
# admin.site.unregister(Group)

from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
