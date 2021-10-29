# Generated by Django 3.2.8 on 2021-10-25 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_auto_20211024_2333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaign',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='choiceevent',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='conditional',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='nodechoice',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='scene',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='scenenode',
            old_name='_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='backgroundimage',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='iconimage',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]