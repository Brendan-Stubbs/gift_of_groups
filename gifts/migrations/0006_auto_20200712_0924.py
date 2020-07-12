# Generated by Django 2.2.13 on 2020-07-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0005_auto_20200712_0758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftgroup',
            old_name='user',
            new_name='users',
        ),
        migrations.AddField(
            model_name='giftgroup',
            name='admins',
            field=models.ManyToManyField(related_name='admin', to='gifts.Profile'),
        ),
    ]
