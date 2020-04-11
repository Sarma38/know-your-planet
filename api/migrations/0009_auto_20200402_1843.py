# Generated by Django 3.0.4 on 2020-04-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_update_question_link_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='is_question',
            field=models.BooleanField(default=True, help_text='La contribution est une question'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='description',
            field=models.TextField(help_text='Informations supplémentaires sur la contribution (réponse, lien, ...)'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='text',
            field=models.TextField(help_text="La contribution de l'utilisateur (une question ou un commentaire)"),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_image_link',
            field=models.URLField(blank=True, help_text="Un lien vers une image pour illustrer la réponse (idéalement avec la source indiquée en bas de l'image)", max_length=500),
        ),
    ]