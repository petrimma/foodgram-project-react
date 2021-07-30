from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20210723_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite_count',
            field=models.IntegerField(default=0, verbose_name='Добавлен в избранное'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Тег'),
        ),
    ]