from django.shortcuts import render, redirect, get_object_or_404
from .models import Admin

def excluir_usuario(request, pk):
    admin = get_object_or_404(Admin, pk = pk)
    if request.method == 'POST':
        admin.delete()
        return redirect('list')
    return render(request, 'Admin/list.html')
