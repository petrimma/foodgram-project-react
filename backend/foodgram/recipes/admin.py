from django.contrib import admin

from .models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                     Subscribe, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags__name")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class AmountAmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")


admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Tag)

admin.site.register(Amount, AmountAmin)

admin.site.register(Subscribe)

admin.site.register(Favorite)

admin.site.register(ShoppingCart)
