# Generated by Django 4.2.3 on 2023-07-16 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Urgent', 'Urgent'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=6),
        ),
    ]
