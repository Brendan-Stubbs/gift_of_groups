# Generated by Django 2.2.15 on 2020-08-17 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0029_auto_20200816_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_made_donation',
            field=models.BooleanField(default=False),
        ),
    ]
