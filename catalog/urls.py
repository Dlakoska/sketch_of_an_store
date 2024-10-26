from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (ProductDetailView, ContactPageView, HomePageView,
                           ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryListView)
from django.views.decorators.cache import cache_page

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('catalog/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('contacts/', ContactPageView.as_view(), name='contacts'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('categories/', CategoryListView.as_view(), name='category_list')

]
