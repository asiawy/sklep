from django.contrib.auth.decorators import login_required  # Dekorator wymagający zalogowania użytkownika
from django.db.models import Q  # Q obiekt do złożonych zapytań warunkowych
from django.shortcuts import render, get_object_or_404, redirect  # Importowanie funkcji do renderowania, pobierania obiektu lub przekierowania

from .forms import NewItemForm, EditItemForm  # Importowanie formularzy
from .models import Category, Item  # Importowanie modeli

#WYSZUKAJ
def items(request):
    query = request.GET.get('query', '')  # Pobieranie wartości parametru zapytania 'query'
    category_id = request.GET.get('category', 0)  # Pobieranie wartości parametru zapytania 'category'
    categories = Category.objects.all()  # Pobieranie wszystkich kategorii
    items = Item.objects.filter(is_sold=False)  # Pobieranie przedmiotów, które nie zostały jeszcze sprzedane

    if category_id:
        items = items.filter(category_id=category_id)  # Filtrowanie przedmiotów według wybranej kategorii

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))  # Filtrowanie przedmiotów zawierających zapytanie w nazwie lub opisie

    return render(request, 'item/items.html', {
        'items': items,  # Przekazanie przedmiotów do szablonu
        'query': query,  # Przekazanie wartości zapytania do szablonu
        'categories': categories,  # Przekazanie kategorii do szablonu
        'category_id': int(category_id)  # Przekazanie wartości identyfikatora kategorii do szablonu
    })

#SZCZEGÓLY RZECZY
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)  # Pobieranie przedmiotu na podstawie identyfikatora (jeśli nie istnieje, wygeneruj błąd 404)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]  # Pobieranie powiązanych przedmiotów

    return render(request, 'item/detail.html', {
        'item': item,  # Przekazanie przedmiotu do szablonu
        'related_items': related_items  # Przekazanie powiązanych przedmiotów do szablonu
    })

#DODAWANIE NOWYCH
@login_required  # Wymaga zalogowania użytkownika
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)  # Tworzenie formularza na podstawie przesłanych danych

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user  # Ustawianie aktualnie zalogowanego użytkownika jako twórcę przedmiotu
            item.save()

            return redirect('item:detail', pk=item.id)  # Przekierowanie do widoku szczegółów przedmiotu
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Dodaj nowe',  # Przekazanie formularza i tytułu do szablonu
    })
#EDYCJA RZECZY

@login_required  # Wymaga zalogowania użytkownika
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)  # Pobieranie przedmiotu na podstawie identyfikatora i sprawdzanie, czy został utworzony przez aktualnie zalogowanego użytkownika

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)  # Tworzenie formularza na podstawie przesłanych danych i istniejącego przedmiotu

        if form.is_valid():
            form.save()  # Zapisywanie zmian w formularzu

            return redirect('item:detail', pk=item.id)  # Przekierowanie do widoku szczegółów przedmiotu
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edycja',  # Przekazanie formularza i tytułu do szablonu
    })

#USUWANIE
@login_required  # Wymaga zalogowania użytkownika
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)  # Pobieranie przedmiotu na podstawie identyfikatora i sprawdzanie, czy został utworzony przez aktualnie zalogowanego użytkownika
    item.delete()  # Usuwanie przedmiotu

    return redirect('dashboard:index')  # Przekierowanie do innego widoku (np. panelu sterowania)
