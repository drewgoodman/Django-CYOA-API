# Generated by Django 3.2.8 on 2021-10-14 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20211012_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditional',
            name='for_success',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
