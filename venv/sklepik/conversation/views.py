from django.contrib.auth.decorators import login_required  # Dekorator wymagający zalogowania użytkownika
from django.shortcuts import render, get_object_or_404, redirect  # Importowanie funkcji do renderowania, pobierania obiektu lub przekierowania

from item.models import Item  # Importowanie modelu Item
from .forms import ConversationMessageForm  # Importowanie formularza ConversationMessageForm
from .models import Conversation  # Importowanie modelu Conversation


@login_required  # Wymaga zalogowania użytkownika
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)  # Pobieranie przedmiotu na podstawie identyfikatora (jeśli nie istnieje, wygeneruj błąd 404)

    if item.created_by == request.user:
        return redirect('dashboard:index')  # Przekierowanie do innego widoku (np. panelu sterowania), jeśli użytkownik jest twórcą przedmiotu

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])  # Pobieranie rozmów dotyczących danego przedmiotu, do których należy użytkownik

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)  # Przekierowanie do szczegółów pierwszej rozmowy, jeśli istnieje

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)  # Tworzenie formularza na podstawie przesłanych danych

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)  # Tworzenie nowej rozmowy na podstawie przedmiotu
            conversation.members.add(request.user)  # Dodawanie użytkownika do członków rozmowy
            conversation.members.add(item.created_by)  # Dodawanie twórcy przedmiotu do członków rozmowy
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)  # Przekierowanie do widoku szczegółów przedmiotu
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form  # Przekazanie formularza do szablonu
    })


@login_required  # Wymaga zalogowania użytkownika
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])  # Pobieranie rozmów, do których należy użytkownik

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations  # Przekazanie rozmów do szablonu
    })


@login_required  # Wymaga zalogowania użytkownika
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)  # Pobieranie rozmowy na podstawie identyfikatora, do której należy użytkownik

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)  # Tworzenie formularza na podstawie przesłanych danych

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)  # Przekierowanie do widoku szczegółów rozmowy
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,  # Przekazanie rozmowy i formularza do szablonu
        'form': form
    })
