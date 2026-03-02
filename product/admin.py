from django.contrib import admin
from .models import Category, Brand, Product, ProductImage

admin.site.register(Category)
admin.site.register(Brand)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price']
    list_display_links = ['id', 'title']
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
