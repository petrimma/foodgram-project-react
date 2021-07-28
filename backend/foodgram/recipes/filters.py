from django_filters.rest_framework import FilterSet, ModelMultipleChoiceFilter

from .models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags", ]
