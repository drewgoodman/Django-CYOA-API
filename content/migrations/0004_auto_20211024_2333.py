# Generated by Django 3.2.8 on 2021-10-25 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_iconimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conditional',
            name='choice_linked',
        ),
        migrations.RemoveField(
            model_name='conditional',
            name='for_success',
        ),
    ]