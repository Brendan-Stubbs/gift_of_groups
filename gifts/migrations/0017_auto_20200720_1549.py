# Generated by Django 2.2.13 on 2020-07-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0016_giftgroupinvitation_days_to_notify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftgroupinvitation',
            name='days_to_notify',
        ),
        migrations.AddField(
            model_name='giftgroup',
            name='days_to_notify',
            field=models.IntegerField(default=14),
        ),
    ]