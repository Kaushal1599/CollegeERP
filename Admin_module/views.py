from django.shortcuts import render
from django.contrib.auth.hashers import make_password
# Create your views here.

import json
from django.core import serializers
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import Student_GeneralForm, Student_AcademyForm
from Student_module.models import Student_Academy_Info, Student_General_Info
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect, HttpResponse
from Teacher_module.models import Teacher_General_Info, Teacher_Academy_Info, Exam_Marks_ClassTest, Exam_Marks_FA, Exam_Marks_SA, Teacher_Feedback
from .forms import Teacher_GeneralForm, Exam_ScheduleForm
from .models import Student_Fee_Info, Notices


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Create_Student(request):

    if request.method == 'POST':

        Student = Student_GeneralForm(data=request.POST)
        Academy = Student_AcademyForm(data=request.POST)
        email = request.POST.get('email')
        date = request.POST.get('date')

        if Student.is_valid() and Academy.is_valid():
            Academy_info = Academy.save(commit=False)

            user = Student.save(commit=False)
            try:
                check_name = Student_General_Info.objects.get(Name=user.Name)
                check_class = Student_Academy_Info.objects.get(
                    Class=Academy_info.Class)
                if check_name.Father_Name == user.Father_Name:
                    if check_class.Class == Academy_info.Class:
                        messages.error(request, "User Already Exist")
            except Exception as e:
                print(e)

                if 'Photo' in request.FILES:
                    user.Photo = request.FILES['Photo']
                user.Date_Of_Birth = date
                user.save()
                Password = user.Father_Phone_Number[7:]
                Auth = User()
                Auth.username = user.Student_ID
                Auth.set_password(Password)
                Auth.email = email
                Auth.save()

                Academy_info = Academy.save(commit=False)

                Academy_info.student_ID_id = user

                Academy_info.save()
                messages.success(request, 'Student Registered Successfully')
                Student = Student_GeneralForm()
                Academy = Student_AcademyForm()
        else:
            print(Student.errors)
            print(Academy.errors)
    else:
        Student = Student_GeneralForm()
        Academy = Student_AcademyForm()
    return render(request, 'Admin/Add_Student.html', {'Student': Student, 'Academy': Academy})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Create_Teacher(request):

    if request.method == 'POST':
        Teacher = Teacher_GeneralForm(data=request.POST)
        Subject = request.POST.getlist('Subject[]')
        Class = request.POST.getlist('Class[]')
        Section = request.POST.getlist('Section[]')
        Class_teacher = request.POST.getlist('class_teacher[]')
        email = request.POST.get('email')
        if Teacher.is_valid():
            user = Teacher.save(commit=False)

            if 'Photo' in request.FILES:
                user.Photo = request.FILES['Photo']

            user.save()
            Password = user.Teacher_Phone_Number[7:]
            Auth = User()
            Auth.username = user.Teacher_ID
            Auth.set_password(Password)
            Auth.email = email
            Auth.save()

            i = 0

            while(i < len(Subject)):
                Academy = Teacher_Academy_Info()
                Academy.Subject = Subject[i]
                Academy.Class = int(Class[i])
                Academy.Section = Section[i]
                Academy.teacher_ID_id = user.Teacher_ID
                Academy.save()
                i += 1

            if len(Class_teacher) != 0:
                Academy.Class_Teacher_Class = int(Class_teacher[0])
                Academy.Class_Teacher_Section = Class_teacher[1]

            Academy.save()
            Teacher = Teacher_GeneralForm()
            messages.success(request, 'Teacher Registered Successfully')
        else:
            print(Teacher.errors)

    else:
        Teacher = Teacher_GeneralForm()

    return render(request, "Admin/Add_Teacher.html", {'Teacher': Teacher})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Schedule_Exam(request):
    if request.method == 'POST':
        ExamSchedule = Exam_ScheduleForm(request.POST, request.FILES)
        print(ExamSchedule)
        if ExamSchedule.is_valid():
            Exam = ExamSchedule.save(commit=False)

            Exam.save()
            messages.success(request, 'Upload Successfully')
        else:
            print(ExamSchedule.errors)
    else:
        ExamSchedule = Exam_ScheduleForm()
    return render(request, "Admin/Exam.html", {'ExamSchedule': ExamSchedule})


def Teacher_Details(request):
    General_Info = Teacher_General_Info.objects.all()
    if request.method == 'POST':
        username = request.POST.get('delete-val')
        user_general = Teacher_General_Info.objects.get(Teacher_ID=username)
        user_academy = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
        user_auth = User.objects.get(username=username)
        user_auth.delete()
        user_academy.delete()
        user_general.delete()
        messages.success(request, "Teacher is deleted Successfully")

    return render(request, "Admin/TeacherDetails.html", {'General_Info': General_Info})


def Student_Details(request):
    if request.method == 'POST':
        Student = Student_GeneralForm(data=request.POST)
        Academy = Student_AcademyForm(data=request.POST)

        username = request.POST.get('delete-val')
        print(username)
    else:
        Student = Student_GeneralForm()
        Academy = Student_AcademyForm()

    return render(request, "Admin/StudentDetails.html", {'Student': Student, 'Academy': Academy})


def get_data(request):
    # username = request.user.username

    if request.method == 'GET':
        General_Info = []
        Class = request.GET['class']
        Student_ID = Student_Academy_Info.objects.all().filter(Class=Class)
        Student_Class = Student_ID[0].Class
        for Student in Student_ID:
            General_Info.append(Student_General_Info.objects.get(
                Student_ID=Student.student_ID_id))
        # print(General_Info[0].Student_ID)
        data = serializers.serialize('json', General_Info)
        return HttpResponse(data, content_type="application/json")
    # else:
        # GeneralInfo = []


def after_delete(request):
    if request.method == 'GET':
        username = request.GET['username']
        exam_classtest = Exam_Marks_ClassTest.objects.all().filter(Student_ID_id=username)
        exam_fa = Exam_Marks_FA.objects.all().filter(Student_ID_id=username)
        exam_sa = Exam_Marks_SA.objects.all().filter(Student_ID_id=username)
        user_academy = Student_Academy_Info.objects.get(student_ID_id=username)
        user_general = Student_General_Info.objects.get(Student_ID=username)
        user_auth = User.objects.get(username=username)
        Class = user_academy.Class
        exam_classtest.delete()
        exam_fa.delete()
        exam_sa.delete()
        user_academy.delete()
        user_general.delete()
        user_auth.delete()
        General_Info = []
        Student_ID = Student_Academy_Info.objects.all().filter(Class=Class)
        Student_Class = Student_ID[0].Class
        for Student in Student_ID:
            General_Info.append(Student_General_Info.objects.get(
                Student_ID=Student.student_ID_id))
        # print(General_Info[0].Student_ID)
        data = serializers.serialize('json', General_Info)
        return HttpResponse(data, content_type="application/json")


def TeacherFeedback(request):
    Feedback = Teacher_Feedback.objects.all()
    Teacher_Detail = []
    for Details in Feedback:
        Teacher_Detail.append(Teacher_General_Info.objects.get(
            Teacher_ID=Details.Teacher_ID_id))
        Details.Audibility_Sum //= Details.Count
        Details.Knowledge_Sum //= Details.Count
        Details.Explaination_Sum //= Details.Count
        Details.Doubt_Clearance_Sum //= Details.Count
    data = zip(Feedback, Teacher_Detail)
    return render(request, "Admin/Feedback.html", {'data': data})


def FeeDetails(request):
    Fee_Details = Student_Fee_Info.objects.all()
    Academy_Details = []
    General_Details = []
    for Details in Fee_Details:
        Academy_Details.append(Student_Academy_Info.objects.get(
            student_ID_id=Details.Student_ID_id))
        General_Details.append(Student_General_Info.objects.get(
            Student_ID=Details.Student_ID_id))
    data = zip(Fee_Details, Academy_Details, General_Details)

    return render(request, 'Admin/FeeDetails.html', {'data': data})


def Upload_Notice(request):
    if request.method == 'POST':
        Student = request.POST.get('Student')
        Teacher = request.POST.get('Teacher')
        Notice = request.POST.get('Notice')
        Notice_Details = Notices()
        if Student == "1" and Teacher == "1":
            Notice_Details.User = 'All'

            if 'file' in request.FILES:
                Notice_Details.File = request.FILES['file']
            else:
                Notice_Details.Notice = Notice
            Notice_Details.save()
            messages.success(request, "Notice Uploaded Successfully!!")
        elif Student == '1':
            Notice_Details.User = 'Student'
            if 'file' in request.FILES:
                Notice_Details.File = request.FILES['file']
            else:
                Notice_Details.Notice = Notice
            Notice_Details.save()

            messages.success(request, "Notice Uploaded Successfully!!")
        elif Teacher == '1':
            Notice_Details.User = 'Teacher'
            if 'file' in request.FILES:
                Notice_Details.File = request.FILES['file']
            else:
                Notice_Details.Notice = Notice
            Notice_Details.save()

            messages.success(request, "Notice Uploaded Successfully!!")
        else:
            messages.error(request, "Select Atleast One CheckBox!!")

    return render(request, 'Admin/Upload_Notice.html')
