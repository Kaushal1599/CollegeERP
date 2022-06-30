from django.shortcuts import render
from django.contrib import messages
from .models import Student_General_Info, Student_Academy_Info, Student_Attendance
from Teacher_module.models import Exam_Marks_ClassTest, Exam_Marks_FA, Exam_Marks_SA, Syllabus, Teacher_Academy_Info, Teacher_General_Info, Teacher_Feedback, Student_Notes, Assignment, Assignment_Submission
from Admin_module.models import Exam_Schedule, Student_Fee_Info
from django.contrib.auth.models import User
# Create your views here.


def Profile_Info(request):
    user = request.user.username
    General_Info = Student_General_Info.objects.get(Student_ID=user)
    Academy_Info = Student_Academy_Info.objects.get(student_ID_id=user)
    Info = User.objects.get(username=user)

    return render(request, 'Student/Profile_Info.html', {'Info': Info, 'General_Info': General_Info, 'Academy_Info': Academy_Info})


def Result(request):
    user = request.user.username
    FA_Result = Exam_Marks_FA.objects.all().filter(Student_ID_id=user)
    SA_Result = Exam_Marks_SA.objects.all().filter(Student_ID_id=user)
    ClassTest_Result = Exam_Marks_ClassTest.objects.all().filter(Student_ID_id=user)

    return render(request, 'Student/Result.html', {'FA_Result': FA_Result, 'SA_Result': SA_Result, 'ClassTest_Result': ClassTest_Result})


def Exam(request):
    user = request.user.username
    Academy_Info = Student_Academy_Info.objects.get(student_ID_id=user)
    Schedule = Exam_Schedule.objects.all().filter(Class=Academy_Info.Class)

    return render(request, 'Student/Exam.html', {'Schedule': Schedule})


def See_Syllabus(request):
    username = request.user.username
    Academy_Info = Student_Academy_Info.objects.get(student_ID_id=username)
    Details = Syllabus.objects.all().filter(Class=Academy_Info.Class)

    return render(request, 'Student/Syllabus.html', {'Details': Details})


def Show_Attendance(request):
    username = request.user.username
    Attendance = Student_Attendance.objects.all().filter(Student_ID_id=username)
    Count_Present = 0
    Count_Absent = 0
    for Detail in Attendance:
        if Detail.Attendance == 'P':
            Count_Present += 1
        else:
            Count_Absent += 1
    try:
        Agg = (Count_Present/(Count_Present+Count_Absent))*100
        Agg = float("{:.2f}".format(Agg))
    except Exception as e:
        print(e)
        Agg = 0.00
    return render(request, 'Student/Show_Attendance.html', {'Agg': Agg, 'Attendance': Attendance})


def TeacherFeedback(request):
    username = request.user.username
    Details = Student_Academy_Info.objects.get(
        student_ID_id=username)
    Class = Details.Class
    Section = Details.Section

    Teacher_ID = Teacher_Academy_Info.objects.all().filter(Class=Class,
                                                           Section=Section)

    Teacher_Details = []

    for Details in Teacher_ID:
        Teacher_Details.append(Teacher_General_Info.objects.get(
            Teacher_ID=Details.teacher_ID_id))

    if request.method == 'POST':
        try:
            for Details in Teacher_Details:
                Feedback = Teacher_Feedback.objects.all().filter(Teacher_ID_id=Details.Teacher_ID)
                if not Feedback:
                    Feedback_Details = Teacher_Feedback()
                    Feedback_Details.Teacher_ID = Details
                    Feedback_Details.Audibility_Sum = request.POST.get(
                        'Audio'+str(Details.Teacher_ID))
                    Feedback_Details.Knowledge_Sum = request.POST.get(
                        'Knowledge'+str(Details.Teacher_ID))
                    Feedback_Details.Explaination_Sum = request.POST.get(
                        'Explaination'+str(Details.Teacher_ID))
                    Feedback_Details.Doubt_Clearance_Sum = request.POST.get(
                        'Doubt'+str(Details.Teacher_ID))
                    Feedback_Details.Count = 1
                    Feedback_Details.save()

                else:
                    Feedback_Info = Feedback[0]
                    Feedback_Info.Audibility_Sum += int(request.POST.get(
                        'Audio'+str(Details.Teacher_ID)))
                    Feedback_Info.Knowledge_Sum += int(request.POST.get(
                        'Knowledge'+str(Details.Teacher_ID)))
                    Feedback_Info.Explaination_Sum += int(request.POST.get(
                        'Explaination'+str(Details.Teacher_ID)))
                    Feedback_Info.Doubt_Clearance_Sum += int(request.POST.get(
                        'Doubt'+str(Details.Teacher_ID)))
                    Feedback_Info.Count += 1
                    Feedback_Info.save()
            messages.success(request, 'Feedback Submitted SuccessFully!!')
        except:
            messages.error(request, "Submit Your Response!!")
    return render(request, 'Student/TeacherFeedback.html', {'Teacher_Details': Teacher_Details})


def FeeDetails(request):
    user = request.user.username
    Details = Student_Fee_Info.objects.all().filter(Student_ID_id=user)
    return render(request, 'Student/FeeDetails.html', {'Details': Details})


def StudentNotes(request):
    user = request.user.username
    Student = Student_Academy_Info.objects.get(student_ID_id=user)
    print(Student.Class, Student.Section)
    Details = Student_Notes.objects.all().filter(
        Class=Student.Class, Section=Student.Section)
    print(Details)
    return render(request, 'Student/Notes.html', {'Details': Details})


def AssignmentSubmission(request):
    user = request.user.username
    Student = Student_Academy_Info.objects.get(student_ID_id=user)
    Student_Details = Student_General_Info.objects.get(Student_ID=user)

    Submission = Assignment_Submission.objects.values('Assignment_ID_id').filter(
        Student_ID_id=user)
    print(Submission)
    Details = Assignment.objects.all().filter(
        Class=Student.Class, Section=Student.Section).exclude(id__in=Submission)
    print(Details)
    if request.method == 'POST':
        Submission = Assignment_Submission()
        Submission.Assignment_ID = Assignment(id=int(request.POST.get('id')))
        Submission.Student_ID = Student_General_Info(Student_ID=user)
        Submission.Class = Student.Class
        Submission.Section = Student.Section
        Submission.Student_Name = Student_Details.Name
        if 'assignment' in request.FILES:
            Submission.Answer_Sheet = request.FILES['assignment']
        Submission.save()
        messages.success(request, "Uploaded Successfully..!!")
    return render(request, 'Student/Assignment.html', {'Details': Details})
