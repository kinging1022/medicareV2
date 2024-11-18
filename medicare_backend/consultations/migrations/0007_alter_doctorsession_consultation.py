# Generated by Django 5.1.2 on 2024-11-14 22:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0006_doctorsession_consultation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsession',
            name='consultation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='consultations.consultation'),
        ),
    ]
