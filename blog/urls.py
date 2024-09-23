from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreatView, BlogUpdateView, BlogDeleteView


app_name = BlogConfig.name

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', BlogCreatView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/update', BlogUpdateView.as_view(), name='update'),
    path('blogs/<int:pk>/delete', BlogDeleteView.as_view(), name='delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
