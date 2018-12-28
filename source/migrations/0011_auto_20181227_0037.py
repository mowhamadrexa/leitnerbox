# Generated by Django 2.1.4 on 2018-12-27 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('source', '0010_messagelog_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='temp_data',
            field=models.CharField(blank=True, max_length=90000),
        ),
        migrations.AlterField(
            model_name='messagelog',
            name='metadata',
            field=models.TextField(max_length=90000),
        ),
    ]
