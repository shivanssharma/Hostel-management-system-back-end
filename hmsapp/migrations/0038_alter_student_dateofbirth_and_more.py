# Generated by Django 4.2.6 on 2024-03-18 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0037_student_is_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='DateOfBirth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='DateOfJoining',
            field=models.DateField(),
        ),
    ]