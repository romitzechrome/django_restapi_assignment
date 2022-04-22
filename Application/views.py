from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse_lazy
from Application.forms import *
from Application.models import *
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    template_name = 'base.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class UserModeFormView(View):
    form_class = UserModelForm
    initial = {}
    template_name = 'User_Registration.html'

    def get(self, *args, **kwargs):
        form = self.form_class()
        self.initial.update({
            'form': form
        })
        return render(self.request, self.template_name, context={'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            pwd = self.request.POST.get('password')
            user = form.save(commit=False)
            user.set_password(pwd)
            user.save()
            return HttpResponseRedirect(reverse_lazy('user_login'))
        return render(self.request, self.template_name, {'form': form})


class LoginFormView(View):
    form_class = LoginForm
    initial = {}
    template_name = 'User_Login.html'

    def get(self, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        self.initial.update({
            'form': form
        })
        return render(self.request, self.template_name, context={'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        username = self.request.POST['Username']
        password = self.request.POST['Password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(self.request, user)
                self.request.session['user_teacher'] = username
                return HttpResponseRedirect(reverse_lazy('teacher_home'))
            elif user.is_active:
                login(self.request, user)
                self.request.session['user_student'] = username
                return HttpResponseRedirect(reverse_lazy('teacher_home'))
        except AttributeError:
            return HttpResponse('Username or Password not valid')
        return render(self.request, self.template_name, {'form': form})


def user_logout(request):
    try:
        logout(request)
        del request.session['user_teacher']
        del request.session['user_student']
        return HttpResponseRedirect(reverse_lazy('user_login'))
    except KeyError:
        return HttpResponseRedirect(reverse_lazy('user_login'))


class CourseModelFormView(LoginRequiredMixin, View):
    form_class = CourseModelForm
    initial = {}
    template_name = 'courses.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('teacher_home'))
        return render(self.request, self.template_name, {'form': form})


class TeachersHomeView(LoginRequiredMixin, View):
    template_name1 = 'teacher_home.html'
    template_name2 = 'student_home.html'
    login_url = 'user_login'

    def get(self, request, *args, **kwargs):
        data = Course.objects.all()
        if request.session.get('user_student', None):
            return render(request, self.template_name2, {'data': data})
        elif request.session.get('user_teacher', None):
            return render(request, self.template_name1, {'data': data})


class AddAssigmentView(LoginRequiredMixin, View):

    form_class = AssigmentModelForm
    initial = {}
    login_url = 'user_login'
    template_name = 'Add_Assigment.html'

    def get(self, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        courses = Course.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.course = courses
            form.save()
            return HttpResponseRedirect(reverse_lazy('teacher_home'))
        return render(self.request, self.template_name, {'form': form})


class All_AssignmentView(LoginRequiredMixin, View):
    template_name = 'all_assignment.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        courses = Course.objects.get(pk=self.kwargs['pk'])
        data = Assigment.objects.filter(course=courses).all()
        return render(self.request, self.template_name, {'data': data})


class AssigmentView(LoginRequiredMixin, View):
    template_name = 'View_Assigment.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        courses = Course.objects.get(pk=self.kwargs['pk'])
        data = Assigment.objects.filter(course=courses).all()
        return render(self.request, self.template_name, {'data': data})


class SolutionDetailsView(LoginRequiredMixin, View):
    template_name = 'Solution_Details.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        try:
            data = Assigment.objects.get(pk=self.kwargs['pk'])
            solution = Solution.objects.filter(ass=data).all()
            context = {
                'data': data,
                'solution': solution
            }
            return render(self.request, self.template_name, context)
        except Solution.DoesNotExist:
            return HttpResponse('Data Does Not Exits')


class Stud_AssigmentView(LoginRequiredMixin, View):
    template_name = 'stud_assignment.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        usr = self.request.session['user_student']
        user = User.objects.get(username=usr)
        solution = Solution.objects.filter(user=user).all
        context = {
            'solution': solution,
        }
        return render(self.request, self.template_name, context)


class DetailsView(LoginRequiredMixin, View):
    form_class = SolutionModelForm
    initial = {}
    template_name = 'view_details.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        usr = self.request.session['user_student']
        user = User.objects.get(username=usr)
        data = Assigment.objects.get(pk=self.kwargs['pk'])
        try:
            if Solution.objects.get(ass=data, user=user):
                return HttpResponseRedirect(reverse_lazy('stud_assigment'))
            else:
                return render(self.request, self.template_name, {'data': data})
        except Solution.DoesNotExist:
            return render(self.request, self.template_name, {'data': data})


class SolutionView(LoginRequiredMixin, View):
    form_class = SolutionModelForm
    initial = {}
    template_name = 'solution.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(self.request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST, self.request.FILES)
        print(self.request.FILES)
        usr = self.request.session['user_student']
        user = User.objects.get(username=usr)
        ass = Assigment.objects.get(pk=self.kwargs['pk'])
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.ass = ass
            form_obj.user = user
            if 'files' in self.request.FILES:
                form_obj.file = self.request.FILES['files']
            form_obj.save()
            return HttpResponseRedirect(reverse_lazy('stud_assigment'))
        return render(self.request, self.template_name, {'form': form})


class AddPointsCommentsView(LoginRequiredMixin, View):
    form_class = PointsCommentsModelForm
    initial = {}
    template_name = 'add_points_comments.html'
    login_url = 'user_login'

    def get(self, *args, **kwargs):
        sol = Solution.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(initial=self.initial, instance=sol)
        return render(self.request, self.template_name, {'form': form, 'sol': sol})

    def post(self, *args, **kwargs):
        sol = Solution.objects.get(pk=self.kwargs['pk'])
        form = self.form_class(self.request.POST, instance=sol)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('teacher_home'))
        return render(self.request, self.template_name, {'form': form})
