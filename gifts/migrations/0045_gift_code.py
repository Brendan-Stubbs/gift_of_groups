# Generated by Django 2.2.15 on 2020-12-25 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0044_giftinvitationlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='code',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
    ]
