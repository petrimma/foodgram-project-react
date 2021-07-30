from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210709_1744'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscribe',
        ),
    ]
