# Generated by Django 2.2.13 on 2020-08-02 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0023_giftidea_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributorgiftrelation',
            name='participation_status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=15),
        ),
    ]
