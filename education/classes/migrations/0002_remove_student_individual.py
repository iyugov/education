# Generated by Django 5.0.7 on 2024-07-29 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='individual',
        ),
    ]
