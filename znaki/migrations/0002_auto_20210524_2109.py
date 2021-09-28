# Generated by Django 3.1.7 on 2021-05-24 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('znaki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecognitionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('label', models.CharField(max_length=255)),
                ('images_amount', models.CharField(default=0, max_length=255)),
                ('probability', models.FloatField(default=0)),
                ('algorithm', models.CharField(max_length=50)),
                ('ownerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='znaki.user')),
            ],
        ),
        migrations.AddField(
            model_name='recognition',
            name='groupID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='znaki.recognitiongroup'),
        ),
    ]
