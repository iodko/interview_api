# Generated by Django 2.2.10 on 2021-08-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answertype',
            name='is_text_answer',
            field=models.BooleanField(default=False),
        ),
    ]