# Generated by Django 2.1.4 on 2018-12-26 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0005_auto_20181226_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mode',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
