# Generated by Django 2.0.2 on 2020-07-26 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher_module', '0004_assignment_submission_student_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment_submission',
            name='Answer_Sheet',
            field=models.FileField(blank=True, upload_to='Answer'),
        ),
    ]