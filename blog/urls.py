import logging
from django import urls
from django.urls import path
from django.contrib.auth.views import  LogoutView
from . import views 
from django.conf import settings


urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path ('login/', views.login_request, name='login'),
    path('register', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('editarperfil/', views.editarPerfil, name='editarperfil'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('miperfil/', views.miperfil, name='miperfil'),
        
]


