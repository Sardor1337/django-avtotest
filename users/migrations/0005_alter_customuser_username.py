# Generated by Django 5.1.5 on 2025-03-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='user_d19f9335-7af8-4f80-afc0-39176090fd49', max_length=255, null=True, unique=True),
        ),
    ]
