# Generated by Django 2.2.15 on 2020-08-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0030_profile_has_made_donation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('origin', models.CharField(blank=True, max_length=30, null=True)),
                ('amount', models.FloatField(default=0)),
            ],
        ),
    ]
