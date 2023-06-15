from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255) # Pole przechowujące nazwę kategorii

    class Meta:
        ordering = ('name',) # Kolejność sortowania kategorii po nazwie
        verbose_name_plural = 'Categories' # Nazwa dla wielu kategorii

    def __str__(self):
        return self.name # Zwraca reprezentację tekstową kategorii (jej nazwę)


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE) # Klucz obcy do kategorii, relacja jeden do wielu
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name # Zwraca reprezentację nazwe