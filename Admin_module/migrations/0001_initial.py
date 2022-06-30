# Generated by Django 2.0.2 on 2020-07-23 16:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Student_module', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam_Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('Term', models.CharField(choices=[('SA-1', 'SA-1'), ('SA-2', 'SA-2'), ('FA-1', 'FA-1'), ('FA-2', 'FA-2'), ('FA-3', 'FA-3'), ('FA-4', 'FA-4'), ('Class Test', 'Class Test')], max_length=20)),
                ('Time_Table', models.FileField(upload_to='Time_Table')),
                ('Date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Notice', models.CharField(max_length=1000)),
                ('User', models.CharField(max_length=10)),
                ('Notice_Date', models.DateField(auto_now=True)),
                ('File', models.FileField(blank=True, upload_to='photo')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Fee_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fee_Status', models.CharField(max_length=5)),
                ('Installment_No', models.IntegerField()),
                ('Due_Date', models.DateField()),
                ('Paid_On', models.DateField(blank=True)),
                ('Student_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student_module.Student_General_Info')),
            ],
        ),
    ]