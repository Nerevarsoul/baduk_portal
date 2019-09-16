# Generated by Django 2.2.5 on 2019-09-11 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tsumego',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата публикации')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('kind', models.CharField(choices=[('life and death', 'жизнь и смерть'), ('fuseki', 'фусеки'), ('yose', 'йосе')], max_length=20)),
                ('level', models.CharField(choices=[('0', 'для всех'), ('1', 'для начинающих'), ('2', 'для старшей группы'), ('3', 'позиционка')], max_length=2, verbose_name='Уровень')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='TsumegoResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('done', 'решена'), ('failed', 'с ошибкой')], max_length=2)),
                ('tsumego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tsumego.Tsumego')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Результат задачи',
                'verbose_name_plural': 'Результаты задач',
            },
        ),
    ]
