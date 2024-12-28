from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Brand


def index(request):
    return render(request, "index.html", context={"selected_products": Product.objects.filter(show=True).order_by("-id")})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def register(request):
    return render(request, "register.html")


def login(request):
    return render(request, "login.html")


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '404.html', status=500)


def all_categories_brands(request):
    return {"all_categories": Category.objects.filter(show=True).order_by("name"), "all_brands": Brand.objects.filter(show=True).order_by("name")}


def show_category(request, cat):
    selected_category = get_object_or_404(Category, slug=cat)
    selected_products = Product.objects.filter(category=selected_category)
    return render(request, "category.html", context={"selected_category": selected_category, "selected_products": selected_products})


def show_brand(request, brand):
    selected_brand = get_object_or_404(Brand, slug=brand)
    selected_products = Product.objects.filter(brand=selected_brand)
    return render(request, "brand.html", context={"selected_brand": selected_brand, "selected_products": selected_products})


def show_details(request, product):
    selected_product = get_object_or_404(Product, slug=product)
    return render(request, "details.html", context={"selected_product": selected_product})
