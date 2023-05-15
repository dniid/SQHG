from django.shortcuts import render, redirect, get_object_or_404

from .forms import UsuarioForm
from .models import Admin

def excluir_usuario(request, pk):
    id = get_object_or_404(id, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('list')
    return render(request, 'admin/list.html')

