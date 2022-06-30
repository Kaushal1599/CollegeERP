from django.urls import path
from . import views
app_name = 'Teacher_module'

urlpatterns = [
    path('Show_Info/', views.Show_Info, name='Show_Info'),
    path('Get_Details/', views.Get_Details, name='Get_Details'),
    path('Upload_Marks/', views.Upload_Marks, name='Upload_Marks'),
    path('Upload_Attendance/', views.Upload_Attendance, name='Upload_Attendance'),
    path('Syllabus/', views.Upload_Syllabus, name='Syllabus'),
    #path('get_class/', views.get_class, name='get_class')
    path('Attendance_Date/', views.Attendance_Date, name='Attendance_Date'),
    path('Add_Notes/', views.Notes, name='Add_Notes'),
    path('Assignment/', views.Student_Assignment, name='Assignment'),
    path('Submission/<int:id>', views.Submissions, name='Submission'),
]
