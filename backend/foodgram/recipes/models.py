from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):
    name = models.CharField("Название", max_length=200)
    color = models.CharField("Цветовой HEX-код", max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField("Название", max_length=200)
    measurement_unit = models.CharField("Единица изменения", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_recipes", verbose_name="Автор")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    name = models.CharField("Название", max_length=200)
    image = models.ImageField("Изображение", upload_to='recipes/')
    text = models.TextField("Описание")
    ingredients = models.ManyToManyField(
        Ingredient, through="Amount", related_name="ingredients_amount", verbose_name="Ингредиенты")
    tags = models.ManyToManyField(
        Tag, related_name="tags", verbose_name="Теги")
    cooking_time = models.IntegerField(
        "Время приготовления в минутах", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    amount = models.IntegerField(
        "Количество", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Количество"
        verbose_name_plural = "Количество"
        #indexes = [
         #   models.Index(fields=["ingredient"]),
        #]
        #ordering = ("recipe",)

    # def __str__(self):
        # return self.ingredient + {measurement_unit}


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="follower")               # blank=True, null=True,
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        #ordering = ("",)

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_recipe")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_user")

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        #ordering = ("",)

    # def __str__(self):
        # return self.user.username


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="in_shopping_cart")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="in_shopping_cart")

    class Meta:
        verbose_name = "Рецепт в списке покупок"
        verbose_name_plural = "Рецепты в списке покупок"
