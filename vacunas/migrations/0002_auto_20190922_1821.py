# Generated by Django 2.2.4 on 2019-09-23 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacunas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='a_os',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='persona',
            name='dias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='persona',
            name='meses',
            field=models.IntegerField(default=0),
        ),
    ]
