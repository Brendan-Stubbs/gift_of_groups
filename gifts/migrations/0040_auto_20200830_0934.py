# Generated by Django 2.2.15 on 2020-08-30 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0039_groupinvitationlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitationlink',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gifts.GiftGroup'),
        ),
    ]
