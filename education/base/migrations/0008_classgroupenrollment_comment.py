# Generated by Django 5.0.7 on 2024-08-23 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_transportpass'),
    ]

    operations = [
        migrations.AddField(
            model_name='classgroupenrollment',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Комментарий'),
        ),
    ]