from datetime import datetime, timedelta
from django.shortcuts import render
from Teacher_module.models import Teacher_General_Info, Teacher_Academy_Info, Exam_Marks_ClassTest, Exam_Marks_FA, Exam_Marks_SA, Syllabus, Student_Notes, Assignment, Assignment_Submission
from Student_module.models import Student_General_Info, Student_Academy_Info, Student_Attendance
# Create your views here.
import json
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Teacher_module.forms import Student_NotesForm
@login_required
def Show_Info(request):

    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False
    Student_ID = Student_Academy_Info.objects.all().filter(Class=Class,
                                                           Section=Section)
    try:
        AcademyDetails = Student_ID[0]
    except Exception as e:
        print(e)
    Student_Details = []
    for Student in Student_ID:
        Student_Details.append(Student_General_Info.objects.get(
            Student_ID=Student.student_ID_id))

    print(Student_Details)

    return render(request, 'Teacher/Show_Info.html', {'Student_Details': Student_Details, 'class_teacher': class_teacher, 'AcademyDetails': AcademyDetails})


Details_Academy = []


@login_required
def Get_Details(request):
    class_teacher = True

    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False

    global Details_Academy
    AcademyDetails = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Subject = []
    Class = []
    Section = []
    for Details in AcademyDetails:
        if Details.Subject != None:
            Subject.append(Details.Subject)
        if Details.Class != None:
            Class.append(Details.Class)
        if Details.Section != None:
            Section.append(Details.Section)
    Subject = set(Subject)
    Class = set(Class)
    Section = set(Section)

    if request.method == 'POST':

        Teacher_Subject = request.POST.get('Subject')
        Student_Class = request.POST.get('Class')
        Student_Section = request.POST.get('Section')

        Student_Class = int(Student_Class)
        # print("ABC")
        # print(Teacher_Subject, Student_Class, Student_Section)

        Details_Academy = [Teacher_Subject, Student_Class, Student_Section]
        return HttpResponseRedirect('../Upload_Marks')

    return render(request, 'Teacher/Get_Details.html', {'Subject': Subject, 'Class': Class, 'Section': Section, 'class_teacher': class_teacher})


@login_required
def Upload_Marks(request):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False

    global Details_Academy
    # print(Details_Academy)
    Student_ID = Student_Academy_Info.objects.all().filter(
        Class=Details_Academy[1], Section=Details_Academy[2])
    Student_Details = []
    for Student in Student_ID:
        Student_Details.append(Student_General_Info.objects.get(
            Student_ID=Student.student_ID_id))
    if request.method == 'POST':
        Student_Marks = request.POST.getlist('Marks[]')
        Term = request.POST.get('Term')
        Max_Mark = request.POST.get('max')
        if max(Student_Marks) > Max_Mark:
            messages.error(request, 'Marks cannot greater than Maximum Marks')
        else:
            if Term[:2] == 'FA':
                i = 0

                for Student in Student_Details:
                    Details = Exam_Marks_FA()
                    Details.Subject = Details_Academy[0]
                    Details.Term = Term
                    Details.Maximum_Marks = Max_Mark
                    Details.Marks = Student_Marks[i]
                    Details.Student_ID_id = Student.Student_ID
                    Details.save()
                    i += 1
                messages.success(request, 'Marks Uploaded Successfully')
            elif Term[:2] == 'SA':
                i = 0

                for Student in Student_Details:
                    Details = Exam_Marks_SA()
                    Details.Subject = Details_Academy[0]
                    Details.Term = Term
                    Details.Maximum_Marks = Max_Mark
                    Details.Marks = Student_Marks[i]
                    Details.Student_ID_id = Student.Student_ID
                    Details.save()
                    i += 1
                messages.success(request, 'Marks Uploaded Successfully')
            else:
                i = 0

                for Student in Student_Details:
                    Details = Exam_Marks_ClassTest()
                    Details.Subject = Details_Academy[0]
                    Details.Term = Term
                    Details.Maximum_Marks = Max_Mark
                    Details.Marks = Student_Marks[i]
                    Details.Student_ID_id = Student.Student_ID
                    Details.save()
                    i += 1
                messages.success(request, 'Marks Uploaded Successfully')
    return render(request, 'Teacher/Upload_Marks.html', {'Student_Details': Student_Details, 'class_teacher': class_teacher})


Date = datetime.now()


@login_required
def Upload_Attendance(request):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False
    Student_ID = Student_Academy_Info.objects.all().filter(Class=Class,
                                                           Section=Section)

    Student_Details = []
    for Student in Student_ID:
        Student_Details.append(Student_General_Info.objects.get(
            Student_ID=Student.student_ID_id))
    global Date
    if request.method == 'POST':
        Present = request.POST.getlist('Check[]', '')
        for Student in Student_Details:

            Attend = Student_Attendance()
            Attend.Teacher_ID = username
            Attend.Date = Date
            Attend.Student_ID_id = Student.Student_ID
            if str(Student.Student_ID) in Present:
                Attend.Attendance = 'P'
            else:
                Attend.Attendance = 'A'
            Attend.save()
        messages.success(request, 'Attendance is Uploaded')
    return render(request, 'Teacher/Upload_Attendance.html', {'Student_Details': Student_Details, 'class_teacher': class_teacher})


def Attendance_Date(request):
    global Date
    username = request.user.username
    class_teacher = True
    Dates = []
    for i in range(0, 7):
        Dates.append((datetime.now() - timedelta(i)).strftime('%Y-%m-%d'))
    if request.method == 'POST':
        Date = request.POST.get('date')
        # Date = datetime.strptime(Date, '%d/%m/%y')

        Check = Student_Attendance.objects.all().filter(
            Teacher_ID=username, Date=Date)
        if not Check:
            return HttpResponseRedirect(reverse('Teacher_module:Upload_Attendance'))
        else:
            messages.error(request, 'Attendance Already Uploaded')

    return render(request, 'Teacher/Attendance_Date.html', {'Dates': Dates, 'class_teacher': class_teacher})


def Upload_Syllabus(request):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False

    username = request.user.username
    AcademyDetails = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Subject = []
    Class = []
    for Details in AcademyDetails:
        if Details.Subject != None:
            Subject.append(Details.Subject)
        if Details.Class != None:
            Class.append(Details.Class)
    Subject = set(Subject)
    Class = set(Class)
    if request.method == 'POST':
        try:
            Details = Syllabus()
            Details.Subject = request.POST.get('Subject')
            Details.Class = request.POST.get('Class')
            Details.Term = request.POST.get('Term')
            Syllabus_Details = request.POST.get('Syllabus')

            if 'syllabus' in request.FILES:
                Details.File = request.FILES['syllabus']
                Details.Syllabus = "None"
            else:
                Details.Syllabus = Syllabus_Details
            Details.save()
            messages.success(request, 'Syllabus Uploaded')
        except Exception as e:
            print(e)
            messages.error(request, "Some Error Occurred..!!")
    return render(request, 'Teacher/Syllabus.html', {'Subject': Subject, 'class_teacher': class_teacher, 'Class': Class})


# def get_class(request):
#     username = request.user.username
#     if request.method == 'GET':
#         Subject = request.GET['subject']
#         Details = Teacher_Academy_Info.objects.all().filter(
#             Subject=Subject, teacher_ID_id=username)
#         Class = []
#         for Teacher in Details:
#             Class.append(Teacher.Class)
#         Class = set(Class)
#         Class = list(Class)
#         Class = json.dumps(Class)
#         return HttpResponse(Class, content_type="application/json")


def Notes(request):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False

    AcademyDetails = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Subject = []
    Class = []
    Section = []
    for Details in AcademyDetails:
        if Details.Subject != None:
            Subject.append(Details.Subject)
        if Details.Class != None:
            Class.append(Details.Class)
        if Details.Section != None:
            Section.append(Details.Section)
    Subject = set(Subject)
    Class = set(Class)
    Section = set(Section)

    Details = Student_Notes.objects.all().filter(Teacher_ID_id=username)
    if request.method == 'POST':
        Note = Student_Notes()
        Note.Teacher_ID = Teacher_General_Info(Teacher_ID=username)
        Note.Class = request.POST.get('Class')
        Note.Section = request.POST.get('Section')
        Note.Subject = request.POST.get('Subject')
        if 'notes' in request.FILES:
            Note.Notes = request.FILES['notes']
        Note.Description = request.POST.get('description')
        Note.save()
        messages.success(request, "Notes are Uploaded Successfully")

    return render(request, 'Teacher/Add_Notes.html', {'class_teacher': class_teacher, 'Subject': Subject, 'Class': Class, 'Section': Section, 'Details': Details})


def Student_Assignment(request):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False

    AcademyDetails = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Subject = []
    Class = []
    Section = []
    for Details in AcademyDetails:
        if Details.Subject != None:
            Subject.append(Details.Subject)
        if Details.Class != None:
            Class.append(Details.Class)
        if Details.Section != None:
            Section.append(Details.Section)
    Subject = set(Subject)
    Class = set(Class)
    Section = set(Section)

    Details = Assignment.objects.all().filter(Teacher_ID_id=username)

    if request.method == 'POST':
        Assignment_Details = Assignment()
        Assignment_Details.Teacher_ID = Teacher_General_Info(
            Teacher_ID=username)
        Assignment_Details.Description = request.POST.get('description')
        Assignment_Details.Class = request.POST.get('Class')
        Assignment_Details.Section = request.POST.get('Section')
        Assignment_Details.Subject = request.POST.get('Subject')
        if 'assignment' in request.FILES:
            Assignment_Details.Question_Paper = request.FILES['assignment']
        Assignment_Details.save()
        messages.success(request, 'Upload Successfully..!!')
    return render(request, 'Teacher/Assignment.html', {'class_teacher': class_teacher, 'Subject': Subject, 'Class': Class, 'Section': Section, 'Details': Details})


def Submissions(request, id):
    class_teacher = True
    AcademyDetails = []
    username = request.user.username
    Teacher_Detail = Teacher_Academy_Info.objects.all().filter(teacher_ID_id=username)
    Class = Section = None
    for teacher in Teacher_Detail:
        if teacher.Class_Teacher_Class != None:
            Class = teacher.Class_Teacher_Class
        if teacher.Class_Teacher_Section != None:
            Section = teacher.Class_Teacher_Section
    if Class == None:
        class_teacher = False
    Details = Assignment.objects.get(id=id)
    Submitted = Assignment_Submission.objects.all().filter(Assignment_ID_id=id)
    Not_Submitted = Assignment_Submission.objects.values(
        'Student_ID_id').filter(Assignment_ID_id=id)
    Academy = Student_Academy_Info.objects.all().filter(
        Class=Details.Class, Section=Details.Section).exclude(student_ID_id__in=Not_Submitted)
    print(Details.Class, Details.Section)
    Student = []
    for Detail in Academy:
        Student.append(Student_General_Info.objects.get(
            Student_ID=Detail.student_ID_id))

    # all_details = []
    # for Detail in Academy:
    #     all_details.append(Student_General_Info.objects.get(
    #         Student_ID=Detail.student_ID_id))
    # Data = zip(all_details, Submitted)

    return render(request, 'Teacher/Submission.html', {'Submitted': Submitted, 'Student': Student, 'class_teacher': class_teacher})
