# Generated by Django 3.1.7 on 2021-05-24 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('znaki', '0002_auto_20210524_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recognition',
            name='groupID',
        ),
        migrations.DeleteModel(
            name='RecognitionGroup',
        ),
    ]
