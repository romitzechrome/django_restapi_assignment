from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from api_app.serializers import *
from django.contrib.auth import authenticate, login, logout
from api_app.tokens import account_activation_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(APIView):

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            if user:
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': 'http://127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email = EmailMessage(
                    mail_subject, message, to=[user.email]
                )
                email.send()
                content = {
                    'user': f'{user} registered Successfully...',
                    'message': 'email send please verify your account.',
                    'status': status.HTTP_201_CREATED,
                }
            return Response(content)
        else:
            content = {
                'message': 'registration fail....',
                'status': 400,
            }
            return Response(content)


class UserLoginView(APIView):

    def post(self, request):
        username = request.data.get('Username', None)
        password = request.data.get('Password', None)
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_staff:
                login(request, user)
                request.session['teacher'] = username
                content = {
                    'user': f'{username} login Successfully...',
                    'login_teacher': request.session['teacher']
                }
                return Response(content, status=status.HTTP_200_OK)
            elif user.is_active:
                login(request, user)
                request.session['student'] = username
                content = {
                    'user': f'{username} login Successfully...',
                    'login_student': request.session['student']

                }
                return Response(content, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Account is not active, kindly activate your account then login"},
                            status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):

    def get(self, request):
        try:
            logout(request)
            del request.session['teacher']
            del request.session['student']
            return Response({'message': f'user logout...'})
        except KeyError:
            return Response({'message': f'user logout...'})


@api_view(('GET',))
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('login_user'))
    else:
        return Response({'message': 'Activation link is invalid!'})


class Courses(APIView):

    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        course_serializer = CourseSerializer(data=request.data)
        if course_serializer.is_valid(raise_exception=True):
            course_serializer.save()
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Assignments(APIView):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        assigment = Assigment.objects.filter(course=course).all()
        serializer = AssigmentSerializer(assigment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        serializer = AssigmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowSolutions(APIView):

    def get(self, request, pk):
        assign = Assigment.objects.get(pk=pk)
        solution = Solution.objects.filter(ass=assign).all()
        serializer = ShowSolutionSerializer(solution, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShowCourses(APIView):

    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)


class ShowAssignments(APIView):

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        assigment = Assigment.objects.filter(course=course).all()
        serializer = AssigmentSerializer(assigment, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)


class SolutionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, **kwargs):
        solution = Solution.objects.all()
        serializer = SolutionSerializer(solution, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        assign = Assigment.objects.get(pk=kwargs.get('pk'))
        if 'user' in request.data:
            username = request.data.get('user')
        elif 'student' in request.session:
            username = request.session['student']
        user = User.objects.get(username=username)
        try:
            if Solution.objects.get(ass=assign, user=user):
                return HttpResponseRedirect(reverse_lazy('solution_assignment'))
        except Solution.DoesNotExist:
            serializer = SolutionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(ass=assign, user=user,)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditSolution(APIView):

    def get(self, request, pk):
        solution = Solution.objects.get(pk=pk)
        serializer = SolutionSerializer(instance=solution)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        solution = Solution.objects.get(pk=pk)
        serializer = SolutionSerializer(data=request.data, instance=solution)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudAssignments(APIView):

    def get(self, request):
        user = User.objects.get(username=request.data.get('user'))
        solution = Solution.objects.filter(user=user).all()
        serializer = StudAssignmentSerializer(solution, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentDetails(APIView):

    def get(self, request, pk):
        assign = Assigment.objects.get(pk=pk)
        serializer = AssigmentSerializer(assign)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
