from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'description',)
    list_filter = ('category',)


@admin.register(Version)
class Version(admin.ModelAdmin):
    list_display = ('name', 'product', 'version_number')
    list_filter = ('product',)
