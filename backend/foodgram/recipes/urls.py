from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import SubscribeViewSet

router = DefaultRouter()

router.register("ingredients", views.IngredientViewSet, basename="ingredients")
router.register("tags", views.TagViewSet,)
router.register("recipes", views.RecipeViewSet, basename="recipe")


urlpatterns = [
    path("users/<int:author_id>/subscribe/",
         SubscribeViewSet.as_view({"get": "create", "delete": "destroy"}),),
    path("users/subscriptions/", SubscribeViewSet.as_view({"get": "list"})),
    path("recipes/<int:recipe_id>/favorite/",
         views.FavoriteViewSet.as_view(
             {"get": "create", "delete": "destroy"})),
    path("recipes/<int:recipe_id>/shopping_cart/",
         views.ShoppingCartViewSet.as_view(
             {"get": "create", "delete": "destroy"})),
    path("recipes/download_shopping_cart/",
         views.download_shopping_cart, name="download"),
    path("", include(router.urls)),
]
