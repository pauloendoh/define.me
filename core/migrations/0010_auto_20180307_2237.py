# Generated by Django 2.0.2 on 2018-03-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180307_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tag',
            field=models.CharField(default='general', max_length=20),
        ),
    ]
