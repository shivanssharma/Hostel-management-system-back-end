# Generated by Django 4.2.6 on 2024-03-17 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0035_remove_student_roomleader_room_roomleader_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='RegistrationNumber',
        ),
        migrations.AddField(
            model_name='room',
            name='RegistrationNumber',
            field=models.ManyToManyField(to='hmsapp.student'),
        ),
    ]
