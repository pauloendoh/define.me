# Generated by Django 2.0.2 on 2018-03-08 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20180307_2152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['updated_at', 'tag']},
        ),
        migrations.AddField(
            model_name='question',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
