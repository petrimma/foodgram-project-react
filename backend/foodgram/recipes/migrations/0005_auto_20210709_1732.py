from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210709_1704'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='amount',
            name='recipes_amo_ingredi_460959_idx',
        ),
        migrations.AddIndex(
            model_name='amount',
            index=models.Index(fields=['recipe'], name='recipes_amo_recipe__8a8b43_idx'),
        ),
    ]
