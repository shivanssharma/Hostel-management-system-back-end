# Generated by Django 4.2.6 on 2024-03-06 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0022_alter_student_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='username',
        ),
    ]