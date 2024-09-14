from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_list, product_detail, contacts, home

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('catalog/<int:pk>/', product_detail, name='product_detail'),
    path('contacts/', contacts, name='contacts')

]
# urlpatterns = [
#     ,
#     path('contacts/', contacts, name='contacts')
# ]
