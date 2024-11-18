# Generated by Django 5.1.2 on 2024-11-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0009_medications_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorsessionmessage',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('notification', 'Notification')], default='text', max_length=50),
        ),
    ]
