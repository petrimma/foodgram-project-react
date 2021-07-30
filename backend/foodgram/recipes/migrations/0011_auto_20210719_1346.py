import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20210717_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amount',
            options={'verbose_name': 'Количество', 'verbose_name_plural': 'Количество'},
        ),
        migrations.RemoveIndex(
            model_name='amount',
            name='recipes_amo_ingredi_460959_idx',
        ),
        migrations.AlterField(
            model_name='amount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='amount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]
