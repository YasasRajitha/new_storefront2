# Generated by Django 5.0.6 on 2024-05-24 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_order_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['user__first_name', 'user__last_name'], 'permissions': [('view_history', 'Can view history')]},
        ),
    ]
