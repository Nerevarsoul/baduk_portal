# Generated by Django 2.2.5 on 2019-09-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsumego', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tsumego',
            name='kind',
            field=models.CharField(choices=[('life and death', 'жизнь и смерть'), ('fuseki', 'фусеки'), ('yose', 'йосе'), ('position', 'позиционка')], max_length=20),
        ),
        migrations.AlterField(
            model_name='tsumego',
            name='level',
            field=models.CharField(choices=[('0', 'для всех'), ('1', 'для начинающих'), ('2', 'для старшей группы')], max_length=2, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='tsumegoresult',
            name='status',
            field=models.CharField(choices=[('done', 'решена'), ('failed', 'с ошибкой')], max_length=10),
        ),
    ]
