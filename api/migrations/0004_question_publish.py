# Generated by Django 3.0.4 on 2020-03-10 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_question_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='publish',
            field=models.BooleanField(default=False, help_text='La question est prête à être publiée'),
        ),
    ]