from django import forms
from django.contrib import admin
from .models import Category, Product, Brand



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    list_display_links = ("name", )
    readonly_fields = ("id",)
    fields = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name", )}
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    list_display_links = ("name", )
    readonly_fields = ("id",)
    fields = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name", )}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "id")
    list_display_links = ("title", )
    readonly_fields = ("id",)
    fields = ("id", "title", "brand", "description", "category", "price", "image", "slug")
    prepopulated_fields = {"slug": ("title", "category", "brand", "price")}
    search_fields = ("title", "brand", "category", "description")
