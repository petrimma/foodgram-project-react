# Generated by Django 2.2 on 2021-07-08 15:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Amount',
                'verbose_name_plural': 'Amounts',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица изменения')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('color', models.CharField(max_length=200, verbose_name='Цветовой HEX-код')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления в минутах')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='ingredients', through='recipes.Amount', to='recipes.Ingredient', verbose_name='Ингредиенты')),
                ('tags', models.ManyToManyField(related_name='tags', to='recipes.Tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='amount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='amount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe'),
        ),
    ]