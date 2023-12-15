# Generated by Django 5.0 on 2023-12-15 19:38

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0003_alter_assignment_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("grade", models.CharField(max_length=24, null=True)),
                ("solution", tinymce.models.HTMLField()),
                (
                    "assignment",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="lms.assignment",
                    ),
                ),
            ],
        ),
    ]