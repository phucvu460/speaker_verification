# Generated by Django 3.1.2 on 2021-05-08 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speaker_verification', '0002_user_embedding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='embedding',
            field=models.FileField(null=True, upload_to='embedding/'),
        ),
    ]
