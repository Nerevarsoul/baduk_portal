# Generated by Django 2.2.5 on 2019-12-13 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_auto_20191112_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='time_started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время начала партии'),
        ),
    ]
