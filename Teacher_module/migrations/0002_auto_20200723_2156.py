# Generated by Django 2.0.2 on 2020-07-23 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher_general_info',
            name='Qualification',
            field=models.CharField(max_length=20),
        ),
    ]