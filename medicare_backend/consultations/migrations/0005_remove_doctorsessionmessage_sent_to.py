# Generated by Django 5.1.2 on 2024-11-12 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0004_doctorsession_doctorsessionmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorsessionmessage',
            name='sent_to',
        ),
    ]