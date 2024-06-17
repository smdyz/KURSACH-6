from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_published

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogView.as_view(), name='home'),
    path('record/new/', BlogCreateView.as_view(), name='create_record'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view_record'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_record'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_record'),
    path('published/<int:pk>/', toggle_published, name='change_published'),
]