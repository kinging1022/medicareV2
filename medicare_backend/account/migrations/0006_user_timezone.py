# Generated by Django 5.1.2 on 2024-12-24 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='timezone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]