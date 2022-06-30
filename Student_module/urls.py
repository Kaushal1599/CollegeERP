from django.urls import path

from . import views

app_name = 'Student_module'

urlpatterns = [
    path('Profile_Info/', views.Profile_Info, name='Profile_Info'),
    path('Result/', views.Result, name='Result'),
    path('Exam/', views.Exam, name='Exam'),
    path('Syllabus/', views.See_Syllabus, name='Syllabus'),
    path('Show_Attendance/', views.Show_Attendance, name='Show_Attendance'),
    path('Teacher_Feedback/', views.TeacherFeedback, name='Teacher_Feedback'),
    path('FeeDetails/', views.FeeDetails, name='FeeDetails'),
    path('Notes/', views.StudentNotes, name='Notes'),
    path('Assignment/', views.AssignmentSubmission, name='Assignment'),
]
