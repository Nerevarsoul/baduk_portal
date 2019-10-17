# Generated by Django 2.2.5 on 2019-09-23 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tsumego', '0002_auto_20190911_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tsumego',
            name='kind',
            field=models.CharField(choices=[('life and death', 'жизнь и смерть'), ('fuseki', 'фусеки'), ('yose', 'йосе'), ('position', 'позиционка')], max_length=20, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='tsumegoresult',
            name='status',
            field=models.CharField(choices=[('done', 'решена'), ('failed', 'с ошибкой')], max_length=10, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='tsumegoresult',
            name='tsumego',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsumego.Tsumego', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='tsumegoresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Участник'),
        ),
    ]