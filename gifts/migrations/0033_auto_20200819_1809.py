# Generated by Django 2.2.15 on 2020-08-19 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0032_auto_20200817_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfilePic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField()),
                ('is_premium', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gifts.ProfilePic'),
        ),
    ]
