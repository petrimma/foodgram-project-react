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
