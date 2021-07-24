from django.contrib import admin

from .models import Ingredient, Recipe, Tag, Amount

admin.site.register(Ingredient)

admin.site.register(Recipe)

admin.site.register(Tag)

admin.site.register(Amount)