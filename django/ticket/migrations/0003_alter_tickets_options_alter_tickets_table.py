# Generated by Django 4.2.1 on 2023-06-12 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_alter_tickets_actual_closure_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tickets',
            options={'default_permissions': ('view', 'create', 'change', 'delete')},
        ),
        migrations.AlterModelTable(
            name='tickets',
            table='tbl_tickets',
        ),
    ]
