# Generated by Django 4.1.5 on 2023-03-12 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sshkbase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
