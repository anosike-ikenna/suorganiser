# Generated by Django 2.2.3 on 2019-07-25 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organiser', '0003_startup_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newslink',
            old_name='links',
            new_name='link',
        ),
    ]
