# Generated by Django 5.0.7 on 2024-07-28 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_individual_is_student_alter_individual_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individual',
            name='is_student',
            field=models.BooleanField(default=False, verbose_name='Обучающийся'),
        ),
    ]
