# Generated by Django 4.2 on 2023-04-19 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='announcement',
            old_name='adnminID',
            new_name='adminID',
        ),
    ]