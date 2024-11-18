# Generated by Django 5.1.2 on 2024-11-17 22:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0011_medications_created_by_medications_created_for'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='medications',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='medications',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medication_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='medications',
            name='created_for',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medications_for', to=settings.AUTH_USER_MODEL),
        ),
    ]
