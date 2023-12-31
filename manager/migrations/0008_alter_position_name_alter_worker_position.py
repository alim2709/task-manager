# Generated by Django 4.2.3 on 2023-07-15 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0007_alter_worker_position"),
    ]

    operations = [
        migrations.AlterField(
            model_name="position",
            name="name",
            field=models.CharField(
                blank=True, default="worker", max_length=60, null=True, unique=True
            ),
        ),
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
