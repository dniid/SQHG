from django.urls import path
from admin import views

urlpatterns = [
    # ...
    path('admin/<int:pk>/excluir/', views.excluir_usuario, name='excluir_usuario'),
]
