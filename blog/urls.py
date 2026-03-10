from django.urls import path
from . import views

urlpatterns = [
    # Leave the path empty string '' so this acts as the homepage
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # New API endpoint for listing all posts in JSON format
    path('api/posts/', views.api_post_list, name='api_post_list'),
]