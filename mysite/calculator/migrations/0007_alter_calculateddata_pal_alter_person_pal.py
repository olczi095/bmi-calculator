# Generated by Django 4.1.7 on 2024-02-21 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0006_alter_person_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calculateddata",
            name="pal",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1.2", "1.2"),
                    ("1.3", "1.3"),
                    ("1.4", "1.4"),
                    ("1.5", "1.5"),
                    ("1.6", "1.6"),
                    ("1.7", "1.7"),
                    ("1.8", "1.8"),
                    ("1.9", "1.9"),
                    ("2.0", "2.0"),
                    ("2.2", "2.2"),
                ],
                default="1.2",
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="pal",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1.2", "1.2"),
                    ("1.3", "1.3"),
                    ("1.4", "1.4"),
                    ("1.5", "1.5"),
                    ("1.6", "1.6"),
                    ("1.7", "1.7"),
                    ("1.8", "1.8"),
                    ("1.9", "1.9"),
                    ("2.0", "2.0"),
                    ("2.2", "2.2"),
                ],
                default="1.2",
                max_length=3,
                null=True,
            ),
        ),
    ]
