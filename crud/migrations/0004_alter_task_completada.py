# Generated by Django 4.1.3 on 2023-02-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0003_remove_task_importante_task_completada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
