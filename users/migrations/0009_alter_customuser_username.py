# Generated by Django 5.1.7 on 2025-03-24 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_category_type_remove_table_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, default='user_057c52bc-8020-49af-be15-2fda083b6b2f', max_length=255, null=True),
        ),
    ]
