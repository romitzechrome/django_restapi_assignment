from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', UserIndexView.as_view(), name='ui_home_page'),
    path('user/register/', UserRegisterView.as_view(), name='user_register'),
    path('login/user/', UserLoginView.as_view(), name='login_user'),
    path('logout/user/', UserLogoutView.as_view(), name='ui_logout'),
    path('user/home/page/', HomePageView.as_view(), name='user_home_page'),
    path('add/course/', AddCourseView.as_view(), name='add_course'),
    path('add/assignments/<int:id>/', AddAssignmentView.as_view(), name="add_assigment_view"),
    path('show/assignments/<int:id>/', ShowAssignment.as_view(), name='show_assigment_view'),
    path('stud/assignment/<int:id>/', StudAssignment.as_view(), name='stud_assigment_view'),
    path('show/courses/', ShowCourses.as_view(), name='show_courses'),
    path('assignment/details/<int:id>/', AssignmentDetails.as_view(), name="assignment_details"),
    path('add/solution/<int:id>/', AddSolution.as_view(), name='add_solution'),
    path('show/solution/<int:id>/', ShowSolution.as_view(), name='show_solution'),
    path('show/solutions/assignemnt/', Solution_Assignment.as_view(), name='solution_assignment'),

    path('edit/solution/<int:id>/', EditSolution.as_view(), name="edit_solution"),


    url(r'^login/user/(?P<data>.*)/$', UserLoginView.as_view(), name='login_user')
]
