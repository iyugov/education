# Generated by Django 5.0.7 on 2024-08-07 09:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0007_alter_classgroupenrollmentitem_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classgroupenrollmentitem',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='classes.student', verbose_name='Обучающийся'),
        ),
        migrations.CreateModel(
            name='ClassGroupEnrollmentRegistryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата зачисления')),
                ('class_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='classes.classgroup', verbose_name='Класс')),
                ('class_group_enrollment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.classgroupenrollment', verbose_name='Зачисление')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='class_group_enrollment_registry', to='classes.student', verbose_name='Обучающийся')),
            ],
            options={
                'verbose_name': 'Элемент зачисления в класс (регистр)',
                'verbose_name_plural': 'Элементы зачисления в класс (регистр)',
            },
        ),
    ]