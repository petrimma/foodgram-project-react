# Generated by Django 2.2 on 2021-07-13 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
