# Generated by Django 2.2.15 on 2020-08-27 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gifts', '0034_auto_20200823_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gifts.GiftGroup')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
