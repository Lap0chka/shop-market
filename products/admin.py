from django.contrib import admin

from products.models import Basket, Products, ProductsCategori

admin.site.register(ProductsCategori)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quanity', 'category')
    fields = ('name', 'company', 'description', 'price', 'quanity', 'image', 'stripe_product_price_id', 'category')
    # readonly_fields = ()
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
