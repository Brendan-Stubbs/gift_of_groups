# Generated by Django 2.2.13 on 2020-07-16 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0009_giftgroup_only_admin_can_invite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='giftgroup',
            old_name='only_admin_can_invite',
            new_name='standard_user_can_invite',
        ),
    ]
