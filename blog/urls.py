from django.urls import path
from . import views

urlpatterns = [
    # Leave the path empty string '' so this acts as the homepage
    path('', views.blog_index, name='blog_index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    
    # API endpoint for listing all posts in JSON format
    path('api/posts/', views.api_post_list, name='api_post_list'),
    
    path('register/', views.register, name='register'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
]