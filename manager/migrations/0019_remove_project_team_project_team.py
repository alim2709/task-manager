# Generated by Django 4.2.3 on 2023-07-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0018_remove_project_team_project_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="team",
        ),
        migrations.AddField(
            model_name="project",
            name="team",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="manager.team"
            ),
        ),
    ]