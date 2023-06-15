from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm
from django.contrib.auth import logout, authenticate


def logout_view(request):
    logout(request)
    return redirect('/login/')  # Przekierowanie na stronę logowania po wylogowaniu

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]# Pobranie 6 niezakupionych przedmiotów
    categories = Category.objects.all()# Pobranie wszystkich kategorii

    return render(request, 'core/index.html', {
        'categories': categories,# Przekazanie kategorii do szablonu
        'items': items,# Przekazanie przedmiotów do szablonu
    })

def contact(request):
    return render(request, 'core/contact.html')# Renderowanie szablonu kontaktu

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():# Sprawdzenie poprawności formularza rejestracji
            form.save()# Zapisanie nowego użytkownika

            return redirect('/login/')# Przekierowanie na stronę logowania po pomyślnej rejestracji
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form# Przekazanie formularza rejestracji do szablonu
    })