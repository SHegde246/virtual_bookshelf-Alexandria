# Generated by Django 3.0.4 on 2020-04-20 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0004_shelf_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='browse',
            name='shelved',
        ),
    ]
