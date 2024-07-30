# Generated by Django 5.0.7 on 2024-07-26 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_individual_options_and_more'),
        ('pass_tags', '0006_alter_passcardissue_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passcard',
            name='pass_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pass_tags.passcardtype', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='passcardissue',
            name='action',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pass_tags.passcardaction', verbose_name='Действие'),
        ),
        migrations.AlterField(
            model_name='passcardissue',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pass_tags.passcard', verbose_name='Карта'),
        ),
        migrations.AlterField(
            model_name='passcardissue',
            name='individual',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.individual', verbose_name='Физическое лицо'),
        ),
    ]