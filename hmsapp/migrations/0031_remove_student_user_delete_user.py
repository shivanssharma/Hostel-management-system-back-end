# Generated by Django 4.2.6 on 2024-03-11 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0030_remove_user_id_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]