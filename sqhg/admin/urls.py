from django.urls import path
from Admin import views

urlpatterns = [
    # ...
    path('Admin/<int:pk>/excluir/', views.excluir_usuario, name='excluir_usuario'),
]
