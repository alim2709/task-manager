# Generated by Django 4.2.3 on 2023-07-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_alter_worker_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(default='worker', max_length=60, unique=True),
        ),
    ]
