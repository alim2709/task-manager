# Generated by Django 4.2.3 on 2023-07-22 09:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0021_alter_task_assignees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
