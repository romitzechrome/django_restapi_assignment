from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', UserRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('add/course/', Courses.as_view()),
    path('add/assignment/<int:pk>/', Assignments.as_view()),
    path('show/solution/<int:pk>/', ShowSolutions.as_view()),
    path('show/courses/', ShowCourses.as_view()),
    path('add/solution/<int:pk>/', SolutionView.as_view()),
    path('show/assigments/', StudAssignments.as_view()),
    path('assignment/details/<int:pk>/', AssignmentDetails.as_view()),
    path('edit/solution/<int:pk>/', EditSolution.as_view()),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
