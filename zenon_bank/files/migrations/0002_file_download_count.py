# Generated by Django 3.0.7 on 2020-09-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='download_count',
            field=models.IntegerField(default=0),
        ),
    ]
