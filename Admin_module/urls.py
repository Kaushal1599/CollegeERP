from django.urls import path

from Admin_module import views

app_name = 'Admin_module'
urlpatterns = [
    path('Create_Student/', views.Create_Student, name='Create_Student'),
    path('Create_Teacher/', views.Create_Teacher, name='Create_Teacher'),
    path('Exam/', views.Schedule_Exam, name='Schedule_Exam'),
    path('TeacherDetails/', views.Teacher_Details, name='TeacherDetails'),
    path('StudentDetails/', views.Student_Details, name='StudentDetails'),
    path('get_data/', views.get_data, name='get_data'),
    path('after_delete/', views.after_delete, name='after_delete'),
    path('Feedback/', views.TeacherFeedback, name='Feedback'),
    path('FeeDetails/', views.FeeDetails, name="FeeDetails"),
    path('Upload_Notice/', views.Upload_Notice, name='Upload_Notice'),

]
