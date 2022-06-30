from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from Student_module.models import Student_General_Info
# Create your models here.
TERM = (('SA-1', 'SA-1'), ('SA-2', 'SA-2'), ('FA-1', 'FA-1'), ('FA-2', 'FA-2'),
        ('FA-3', 'FA-3'), ('FA-4', 'FA-4'), ('Class Test', 'Class Test'))


class Exam_Schedule(models.Model):
    Class = models.IntegerField(validators=[
        MaxValueValidator(12), MinValueValidator(1)])
    Term = models.CharField(max_length=20, choices=TERM)
    Time_Table = models.FileField(upload_to='Time_Table')
    Date = models.DateField(auto_now=True)


class Student_Fee_Info(models.Model):
    Student_ID = models.ForeignKey(
        Student_General_Info, on_delete=models.CASCADE)
    Fee_Status = models.CharField(max_length=5)
    Installment_No = models.IntegerField()
    Due_Date = models.DateField()
    Paid_On = models.DateField(blank=True)


class Notices(models.Model):
    Notice = models.CharField(max_length=1000)
    User = models.CharField(max_length=10)
    Notice_Date = models.DateField(auto_now=True)
    File = models.FileField(upload_to='photo', blank=True)
