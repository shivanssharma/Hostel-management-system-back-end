# Generated by Django 4.2.6 on 2024-03-11 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0027_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='userName',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
