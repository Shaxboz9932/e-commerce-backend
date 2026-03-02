from django.contrib import admin
from wishlist.models import WishlistItem


class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "created_at"]

admin.site.register(WishlistItem, WishlistAdmin)
