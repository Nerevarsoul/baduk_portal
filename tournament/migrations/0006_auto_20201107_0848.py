# Generated by Django 3.1.1 on 2020-11-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0005_auto_20200131_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='tour',
            field=models.IntegerField(blank=True, null=True, verbose_name='№ тура'),
        ),
        migrations.AddField(
            model_name='participant',
            name='group',
            field=models.IntegerField(blank=True, null=True, verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='challenger',
            field=models.BooleanField(blank=True, null=True, verbose_name='Претендент'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='title_holder',
            field=models.BooleanField(blank=True, null=True, verbose_name='Держатель титула'),
        ),
        migrations.AlterField(
            model_name='title',
            name='cron_string',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Данные для авто создания турнира'),
        ),
        migrations.AlterField(
            model_name='title',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='title',
            name='tag',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Тэг'),
        ),
        migrations.AlterField(
            model_name='title',
            name='time_to_life',
            field=models.IntegerField(blank=True, null=True, verbose_name='Продолжительность'),
        ),
        migrations.AlterField(
            model_name='title',
            name='with_title_match',
            field=models.BooleanField(blank=True, null=True, verbose_name='Матч за титул'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='point_for_win',
            field=models.FloatField(default=1, verbose_name='Очки за победу'),
        ),
    ]