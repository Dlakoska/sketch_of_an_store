from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ContactPageView, HomePageView, ProductListView


app_name = CatalogConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('catalog/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactPageView.as_view(), name='contacts')

]
# urlpatterns = [
#     ,
#     path('contacts/', contacts, name='contacts')
# ]
