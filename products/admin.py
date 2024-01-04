from django.contrib import admin

from products.models import Basket, Products, ProductsCategori, ProductSize, ProductImage

admin.site.register(ProductsCategori)

@admin.register(ProductImage)
class ProductsImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


@admin.register(ProductSize)
class ProductsSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size_name')


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Количество пустых форм для добавления новых размеров


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quanity', 'category')
    # readonly_fields = ()
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline, ProductImageInline]



class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
