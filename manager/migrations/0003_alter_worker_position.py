# Generated by Django 4.2.3 on 2023-07-12 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_alter_worker_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workers",
                to="manager.position",
            ),
        ),
    ]
