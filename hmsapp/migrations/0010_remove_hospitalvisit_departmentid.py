# Generated by Django 4.2.6 on 2024-03-02 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hmsapp', '0009_delete_admin_remove_order_totalprice_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalvisit',
            name='departmentID',
        ),
    ]