import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from Application.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout


class UserIndexView(View):
    template_name = 'ui_base.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class UserRegisterView(View):
    template_name = 'user_registration.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="post",
            url='http://127.0.0.1:8000/' + 'api/registration/',
            data=self.request.POST

        ).json()
        context_data.update({
            'data': response
        })
        if 'status' in response:
            if response['status'] == 201:
                return HttpResponseRedirect(reverse_lazy('login_user', kwargs={
                    'data': 'Registration Successful, Kindly check your mail and confirm your account.'}))
        else:
            return render(self.request, self.template_name, context_data)


class UserLoginView(View):
    template_name = 'login_user.html'

    def get(self, *args, **kwargs):
        if 'data' in self.kwargs:
            context_data = {
                'data': self.kwargs['data']
            }
            return render(self.request, self.template_name, context_data)
        else:
            return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        response = requests.request(
            method="post",
            url='http://127.0.0.1:8000/' + 'api/login/',
            data=self.request.POST
        ).json()
        if 'message' in response:
            context_data = {
                'data': response['message']
            }
            return render(self.request, self.template_name, context_data)
        else:
            if response.get('login_teacher', None):
                username = response['login_teacher']
                user = User.objects.get(username=username)
                login(self.request, user)
                self.request.session['teacher'] = response['login_teacher']
                return HttpResponseRedirect(reverse_lazy('user_home_page'))
            elif response.get('login_student', None):
                username = response['login_student']
                user = User.objects.get(username=username)
                login(self.request, user)
                self.request.session['student'] = response['login_student']
                return HttpResponseRedirect(reverse_lazy('show_courses'))


class UserLogoutView(View):

    def get(self, *args, **kwargs):
        response = requests.request(
            method="get",
            url='http://127.0.0.1:8000/' + 'api/logout/',
            data=self.request.GET
        ).json()
        try:
            logout(self.request)
            del self.request.session['teacher']
            del self.request.session['student']
            return HttpResponseRedirect(reverse_lazy('login_user'))
        except KeyError:
            return HttpResponseRedirect(reverse_lazy('login_user'))


class HomePageView(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = 'home_page_view.html'

    def get(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="get",
            url='http://127.0.0.1:8000/' + 'api/add/course/',
            data=self.request.GET

        ).json()
        context_data.update({
            "data": response
        })
        return render(self.request, self.template_name, context_data)


class AddCourseView(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = 'add_courses.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        context_data = {}
        context_data.update(
            response=requests.request(
                method="post",
                url='http://127.0.0.1:8000/' + 'api/add/course/',
                data=self.request.POST

            ).json()
        )
        return HttpResponseRedirect(reverse_lazy('user_home_page'))


class AddAssignmentView(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "add_assignment.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        response = requests.request(
            method="post",
            url=f'http://127.0.0.1:8000/api/add/assignment/{kwargs.get("id")}/',
            data=self.request.POST

        ).json()
        print(self.request.POST)
        print(response)
        return HttpResponseRedirect(reverse_lazy('user_home_page'))


class ShowAssignment(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "show_assignment.html"

    def get(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/add/assignment/{kwargs.get("id")}/',
            data=self.request.GET
        ).json()
        context_data.update({
            "data": response
        })
        return render(self.request, self.template_name, context_data)


class StudAssignment(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "stud_assign.html"

    def get(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/add/assignment/{kwargs.get("id")}/',
            data=self.request.GET
        ).json()
        context_data.update({
            "assignment": response
        })
        return render(self.request, self.template_name, context_data)


class ShowCourses(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "student_home_view.html"

    def get(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/show/courses/',
            data=self.request.GET
        ).json()
        context_data.update({
            "data": response
        })
        return render(self.request, self.template_name, context_data)


class AddSolution(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "add_solution.html"

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        response = requests.request(
            method="post",
            url=f'http://127.0.0.1:8000/api/add/solution/{kwargs.get("id")}/',
            data={
                'title': self.request.POST['title'],
                'answer': self.request.POST['answer'],
                'file': self.request.FILES['files'],
                'user': self.request.session['student']
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Disposition': 'attachment; filename="file"'}
        ).json()
        print(response)
        return HttpResponseRedirect(reverse_lazy('solution_assignment'))


class EditSolution(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = 'edit_solution.html'

    def get(self, *args, **kwargs):
        context_data = {}
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/edit/solution/{kwargs.get("id")}/',
            data=self.request.GET
        ).json()
        print(response)
        context_data.update({
            'data': response
        })
        return render(self.request, self.template_name, context_data)

    def post(self, *args, **kwargs):
        response = requests.request(
            method="post",
            url=f'http://127.0.0.1:8000/api/edit/solution/{kwargs.get("id")}/',
            data=self.request.POST
        ).json()
        return HttpResponseRedirect(reverse_lazy('solution_assignment'))


class ShowSolution(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "show_Solution.html"

    def get(self, *args, **kwargs):
        context_data = {}
        assign = Assigment.objects.get(id=self.kwargs['id'])
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/show/solution/{kwargs.get("id")}/',
            data=self.request.GET
        ).json()
        context_data.update({
            "data": response,
            "assign": assign
        })
        return render(self.request, self.template_name, context_data)


class AssignmentDetails(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = "assignment_details.html"

    def get(self, *args, **kwargs):
        username = self.request.session['student']
        user = User.objects.get(username=username)
        assign = Assigment.objects.get(id=self.kwargs["id"])
        try:
            if Solution.objects.get(ass=assign, user=user):
                return HttpResponseRedirect(reverse_lazy('solution_assignment'))
        except Solution.DoesNotExist:
            context_data = {}
            response = requests.request(
                method="get",
                url=f'http://127.0.0.1:8000/api/assignment/details/{kwargs.get("id")}/',
                data={
                    'data': self.request.GET,
                    'user': self.request.session['student']
                }
            ).json()
            context_data.update({
                "data": response
            })
            return render(self.request, self.template_name, context_data)


class Solution_Assignment(LoginRequiredMixin, View):
    login_url = 'login_user'
    template_name = 'solution_assignment.html'

    def get(self, *args, **kwargs):
        context_data = {}
        if 'student' in self.request.session:
            user = self.request.session['student']
        response = requests.request(
            method="get",
            url=f'http://127.0.0.1:8000/api/show/assigments/',
            data={
                'user': user
            }
        ).json()
        context_data.update({
            "data": response
        })
        return render(self.request, self.template_name, context_data)
