# Generated by Django 2.1.4 on 2018-12-27 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0007_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='telegram_start_text',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='setting',
            name='telegram_welcome_text',
            field=models.TextField(max_length=400),
        ),
    ]