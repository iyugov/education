# Generated by Django 5.0.7 on 2024-07-30 20:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pass_tags', '0015_passtagrequestitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passtagrequestitem',
            name='pass_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pass_tags.passtag', verbose_name='Чип'),
        ),
        migrations.AlterField(
            model_name='passtagrequestitem',
            name='processing_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата обработки'),
        ),
    ]