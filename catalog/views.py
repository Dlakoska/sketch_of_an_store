from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product,
               'title': 'Главная'}
    return render(request, 'product_detail.html', context)


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(f'name: {name}, email: {email}')
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'имя: {name}, телефон: {phone}, сообщение:{message}')
    return render(request, 'contacts.html')