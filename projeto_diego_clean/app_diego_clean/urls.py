
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login, name="login"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logout/', views.logout_view, name='logout'),

]