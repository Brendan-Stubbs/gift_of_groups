# Generated by Django 2.2.15 on 2021-01-13 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0046_contributorgiftrelation_receiver_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributorgiftrelation',
            name='email_notifications_allowed',
            field=models.BooleanField(default=True),
        ),
    ]
