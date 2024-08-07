# Generated by Django 5.0.7 on 2024-07-29 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_individual_is_student'),
        ('classes', '0002_remove_student_individual'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='individual',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='student', to='base.individual', verbose_name='Физическое лицо'),
            preserve_default=False,
        ),
    ]
