# Generated by Django 5.1.5 on 2025-03-22 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userrole'),
        ),
    ]
