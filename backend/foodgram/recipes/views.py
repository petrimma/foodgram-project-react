from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.models import User
from .filters import IngredientFilter, RecipeFilter
from foodgram.pagination import FoodgramPagination
from .models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                     Subscribe, Tag)
from .permissions import IsAuthor, RecipePermission, SubscribePermission
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer,
                          SubscribeSerializer, TagSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [RecipePermission, ]
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RecipeSerializer
        else:
            return CreateRecipeSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = [SubscribePermission, ]
    pagination_class = FoodgramPagination
    lookup_field = "author_id"

    def get_queryset(self):
        user = self.request.user
        return Subscribe.objects.filter(user=user)

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.kwargs.get("author_id"))
        serializer.save(user=self.request.user, author=author)

    def perform_destroy(self, instance):
        user = self.request.user
        author = get_object_or_404(User, pk=self.kwargs.get("author_id"))
        follow = get_object_or_404(Subscribe, user=user, author=author)
        follow.delete()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = "recipe_id"

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = "recipe_id"

    def get_queryset(self):
        user = self.request.user
        return ShoppingCart.objects.filter(user=user)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        favorite = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        favorite.delete()


@api_view(["GET"])
@permission_classes([IsAuthor | IsAdminUser])
def download_shopping_cart(request):
    user = request.user
    recipes_in_shopping_cart = Recipe.objects.filter(
        in_shopping_cart__user=user)
    ingredients_in_shopping_cart = Amount.objects.filter(
        recipe__in=recipes_in_shopping_cart).select_related("ingredient")
    ingredients_sum = ingredients_in_shopping_cart.values(
        "ingredient").annotate(sum=Sum("amount"))

    response = HttpResponse()
    response.write("Список покупок Foodgram \n")
    response.write("\n")

    for item in ingredients_sum:
        ingredient = ingredients_in_shopping_cart.filter(
            ingredient=item["ingredient"])[0].ingredient
        ingredient_name = ingredient.name
        ingredient_unit = ingredient.measurement_unit
        sum = item["sum"]
        response.write(f"{ingredient_name} ({ingredient_unit}): {sum} \n")

    response["Content-Type"] = "text/plain"
    response["Content-Disposition"] = "attachment; \
        filename='shopping_list.txt'"
    return response
