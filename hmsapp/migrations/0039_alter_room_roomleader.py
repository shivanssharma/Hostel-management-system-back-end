# Generated by Django 4.2.6 on 2024-03-18 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0038_alter_student_dateofbirth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='roomLeader',
            field=models.BooleanField(default=False),
        ),
    ]
