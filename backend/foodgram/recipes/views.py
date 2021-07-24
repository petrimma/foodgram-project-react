from django.shortcuts import get_object_or_404
from django.db.models import Avg, Sum, Count
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.validators import UniqueTogetherValidator

from rest_framework.generics import ListAPIView

from .serializers import CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer, ShoppingCartSerializer, SubscribeSerializer, TagSerializer, RecipeSerializer, RecipeShortSerializer
from .models import Amount, Favorite, Ingredient, ShoppingCart, Subscribe, Tag, Recipe
from users.models import User
from foodgram.pagination import FoodgramPagination
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["^name"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    #serializer_class = RecipeSerializer
    pagination_class = FoodgramPagination

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        else:
            return CreateRecipeSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    pagination_class = FoodgramPagination
    permission_classes = [IsAuthenticated, ]
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
    queryset = Favorite.objects.all()
    lookup_field = "recipe_id"

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
    queryset = ShoppingCart.objects.all()
    lookup_field = "recipe_id"

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        favorite = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        favorite.delete()


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
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

    response["Content-Type"] = "application/pdf"
    response["Content-Disposition"] = "attachment; filename='shopping_list.pdf'"

    return response
