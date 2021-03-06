# Generated by Django 3.0.4 on 2020-04-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_auto_20200409_1828"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="answer_option_c",
            field=models.CharField(
                blank=True, help_text="La réponse c", max_length=150
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="answer_option_d",
            field=models.CharField(
                blank=True, help_text="La réponse d", max_length=150
            ),
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(help_text="Le nom du quiz", max_length=50)),
                (
                    "description",
                    models.TextField(blank=True, help_text="Une description du quiz"),
                ),
                (
                    "created",
                    models.DateField(
                        auto_now=True,
                        help_text="La date & heure de la création du quiz",
                    ),
                ),
                (
                    "questions",
                    models.ManyToManyField(
                        help_text="Les questions du quiz",
                        related_name="quizzes",
                        to="api.Question",
                    ),
                ),
            ],
        ),
    ]
