from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


from .serializers import AddIngredientToRecipeSerializer, CreateRecipeSerializer, FavoriteSerializer, IngredientSerializer, ShoppingCartSerializer, SubscribeSerializer, TagSerializer, RecipeSerializer, RecipeShortSerializer
from .models import Amount, Favorite, Ingredient, ShoppingCart, Subscribe, Tag, Recipe
from .permissions import IsAuthor
from users.models import User
from foodgram.pagination import FoodgramPagination
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404


def TemplateView(request):                              ###
    return render(request, 'build/index.html')


class IngredientViewSet(viewsets.ModelViewSet):
    #queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer    # AddIngredientToRecipeSerializer
    #filter_backends = [filters.SearchFilter]
    #search_fields = ["^name"]

    #def get(self, request, *args, **kwargs):
     #   query = request.GET['query']
     #   queryset = self.queryset.filter(title__istartswith=query)
      #  serializer = IngredientSerializer(queryset, many=True)
       # return Response(serializer.data)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        print(name)
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset


class AmountViewSet(viewsets.ModelViewSet):
    serializer_class = AddIngredientToRecipeSerializer
        
    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get("name")
        print(name)
        if name is not None:
            queryset = queryset.filter(name__startswith=name)
        return queryset



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("slug",)   


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,) 
    filterset_fields = ("author",)   

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        tags = self.request.query_params.getlist("tags") 
        
        if is_favorited == "true":    
            user = self.request.user
            queryset = queryset.filter(favorite_user__user=user)
        
        if is_in_shopping_cart == "true":
            user = self.request.user
            queryset = queryset.filter(in_shopping_cart__user=user)   

        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
 
        return queryset 

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        else:
            return CreateRecipeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthor | IsAdminUser]
        return [permission() for permission in permission_classes]


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
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

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthor | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


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
@permission_classes((IsAuthor,))
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

    response["Content-Type"] = "text/plain"    #application/pdf
    response["Content-Disposition"] = "attachment; filename='shopping_list.txt'"
    return response

