# Generated by Django 5.0.7 on 2024-07-26 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True)),
                ('birth_date', models.DateField()),
            ],
        ),
    ]
