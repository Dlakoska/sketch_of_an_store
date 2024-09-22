
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class HomePageView(TemplateView):
    template_name = 'catalog/home.html'


class ContactPageView(TemplateView):
    template_name = 'catalog/contacts.html'

#
# def contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'имя: {name}, телефон: {phone}, сообщение:{message}')
#     return render(request, 'contacts.html')