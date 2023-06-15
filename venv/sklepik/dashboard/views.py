from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from item.models import Item

@login_required # Wymaga logowania użytkownika
def index(request):
    items = Item.objects.filter(created_by=request.user)# Pobranie przedmiotów stworzonych przez zalogowanego użytkownika

    return render(request, 'dashboard/index.html', {
        'items': items,# Przekazanie przedmiotów do szablonu
    })