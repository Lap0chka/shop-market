# Generated by Django 4.2.2 on 2023-06-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_emailverification_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
