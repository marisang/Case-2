from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logout/', views.logout_view, name='logout'),
    path('adicionar-servico/', views.adicionar_servico, name='adicionar_servico'),
    path('editar-servico/', views.editar_servico, name='editar_servico'),
    path('remover-servico/', views.remover_servico, name='remover_servico'),
]
