# Generated by Django 3.1 on 2020-09-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0005_auto_20200917_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='damage',
            field=models.IntegerField(null=True),
        ),
    ]
