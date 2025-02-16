# Generated by Django 5.1.2 on 2024-12-19 20:59

import consultations.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0012_alter_medications_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorsessionmessage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/chat_images/', validators=[consultations.models.validate_file]),
        ),
        migrations.AddField(
            model_name='doctorsessionmessage',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='media/chat_videos/', validators=[consultations.models.validate_file]),
        ),
        migrations.AddField(
            model_name='medications',
            name='has_reminder',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='doctorsessionmessage',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('notification', 'Notification'), ('image', 'Image'), ('video', 'Video')], default='text', max_length=50),
        ),
    ]
