from Application import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('user/registration', views.UserModeFormView.as_view(), name='user_registration'),
    path('user/login/', views.LoginFormView.as_view(), name='user_login'),
    path('user/logot/', views.user_logout, name='user_logout'),
    path('add/courses/', views.CourseModelFormView.as_view(), name='add_courses'),
    path('teacher/home/', views.TeachersHomeView.as_view(), name='teacher_home'),
    path('add/assigment/<int:pk>/', views.AddAssigmentView.as_view(), name='add_assigment'),
    path('all/assignment/<int:pk>/', views.All_AssignmentView.as_view(), name='all_assignment'),
    path('view/assigment/<int:pk>/', views.AssigmentView.as_view(), name='view_assigment'),
    path('solution_details/<int:pk>/', views.SolutionDetailsView.as_view(), name='solution_details'),
    path('student/assigment/', views.Stud_AssigmentView.as_view(), name='stud_assigment'),
    path('view/details/<int:pk>/', views.DetailsView.as_view(), name='view_details'),
    path('solution/<int:pk>/', views.SolutionView.as_view(), name='solution'),
    path('add/points/comments/<int:pk>/', views.AddPointsCommentsView.as_view(), name='add_points_comments'),

]
