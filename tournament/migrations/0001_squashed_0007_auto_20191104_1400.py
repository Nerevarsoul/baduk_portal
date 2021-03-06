# Generated by Django 2.2.5 on 2019-11-04 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('tournament', '0001_initial'), ('tournament', '0002_auto_20191031_1042'), ('tournament', '0003_auto_20191031_1052'), ('tournament', '0004_auto_20191031_1419'), ('tournament', '0005_auto_20191031_1530'), ('tournament', '0006_auto_20191103_0717'), ('tournament', '0007_auto_20191104_1400')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('tag', models.CharField(max_length=150, verbose_name='Тэг')),
                ('cron_string', models.CharField(max_length=20, verbose_name='Данные для авто создания турнира')),
                ('time_to_life', models.IntegerField(verbose_name='Продолжительность')),
                ('tour_number', models.IntegerField(blank=True, null=True, verbose_name='Число туров')),
                ('is_active', models.BooleanField(verbose_name='Активен')),
                ('with_title_match', models.BooleanField(verbose_name='Матч за титул')),
            ],
            options={
                'verbose_name': 'Титул',
                'verbose_name_plural': 'Титулы',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('is_active', models.BooleanField(verbose_name='Активен')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Title', verbose_name='Титул')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Победитель')),
                ('tag', models.CharField(blank=True, max_length=150, null=True, verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Турнир',
                'verbose_name_plural': 'Турниры',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='tournament.Tournament', verbose_name='Турнир')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='Уровень')),
                ('start_points', models.FloatField(blank=True, null=True, verbose_name='Стартовые очки')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('done', 'окончена'), ('not played', 'не сыграна')], max_length=10, verbose_name='Статус')),
                ('result', models.CharField(choices=[('black', 'b+'), ('white', 'w+'), ('jigo', '=')], max_length=10, verbose_name='Результат')),
                ('handicap', models.IntegerField(blank=True, null=True, verbose_name='Фора')),
                ('score', models.FloatField(blank=True, null=True, verbose_name='Счет')),
                ('sgf', models.FileField(blank=True, null=True, upload_to='', verbose_name='СГФ')),
                ('black_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='black_user', to='tournament.Participant', verbose_name='Черный игрок')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='tournament.Tournament', verbose_name='Турнир')),
                ('white_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='white_user', to='tournament.Participant', verbose_name='Белый игрок')),
            ],
            options={
                'verbose_name': 'Игра',
                'verbose_name_plural': 'Игры',
            },
        ),
    ]
