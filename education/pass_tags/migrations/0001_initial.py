# Generated by Django 5.0.7 on 2024-07-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PassCardType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип пропускных карт',
                'verbose_name_plural': 'Типы пропускных карт',
            },
        ),
    ]