from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login' ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout' ),
    path('upload/', views.upload_image, name='upload'),
    #path('result/', views.display_result, name='display_result' ),
    path('match/', views.match_found, name='match_found'),
    path('nomatch/', views.match_not_found, name='match_not_found'),
]