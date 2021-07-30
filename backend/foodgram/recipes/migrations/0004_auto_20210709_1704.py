from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210709_1623'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='amount',
            index=models.Index(fields=['ingredient'], name='recipes_amo_ingredi_460959_idx'),
        ),
    ]
