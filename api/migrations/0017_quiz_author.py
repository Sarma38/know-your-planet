# Generated by Django 3.0.4 on 2020-04-15 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_auto_20200412_1732"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="author",
            field=models.CharField(
                blank=True, help_text="L'auteur du quiz", max_length=50
            ),
        ),
    ]
