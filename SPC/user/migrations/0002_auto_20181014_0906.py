# Generated by Django 2.0.5 on 2018-10-14 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files',
            old_name='file',
            new_name='docfile',
        ),
        migrations.RemoveField(
            model_name='files',
            name='path',
        ),
    ]
