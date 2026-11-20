import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
            options={
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='account_email_lower_unique')],
            },
        ),
    ]
