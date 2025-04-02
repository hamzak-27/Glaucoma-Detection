# Generated by Django 5.1.4 on 2025-04-02 01:08

import detection.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
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
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="GlaucomaTest",
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
                (
                    "image",
                    models.ImageField(upload_to=detection.models.get_upload_path),
                ),
                ("is_glaucoma", models.BooleanField(null=True)),
                ("confidence_score", models.FloatField(null=True)),
                ("raw_score", models.FloatField(null=True)),
                (
                    "result_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="uploads/results"
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_processed", models.DateTimeField(blank=True, null=True)),
                ("processing_time", models.FloatField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("error_message", models.TextField(blank=True, null=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tests",
                        to="detection.patient",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_created"],
            },
        ),
    ]
