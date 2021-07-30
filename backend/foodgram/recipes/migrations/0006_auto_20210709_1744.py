from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20210709_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amount',
            options={'ordering': ('recipe',), 'verbose_name': 'Количество', 'verbose_name_plural': 'Количество'},
        ),
        migrations.RemoveIndex(
            model_name='amount',
            name='recipes_amo_recipe__8a8b43_idx',
        ),
        migrations.AddIndex(
            model_name='amount',
            index=models.Index(fields=['ingredient'], name='recipes_amo_ingredi_460959_idx'),
        ),
    ]
