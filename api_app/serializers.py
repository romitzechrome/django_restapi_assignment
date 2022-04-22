from rest_framework import serializers
from api_app.models import *
from Application.models import Course, Assigment, Solution
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="A user with that email address already exists.")]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        username = validated_data['username']
        password = validated_data['password']
        user.set_password(password)
        user.is_active = False
        user.save()
        return user


class CourseSerializer(serializers.ModelSerializer):
    Course = serializers.CharField(
        validators=[UniqueValidator(queryset=Course.objects.all())]
    )

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        course.save()
        return course


class AssigmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assigment
        fields = ['id', 'Name', 'Questions', 'Deadline']

    def create(self, validated_data):
        assign = Assigment.objects.create(**validated_data)
        assign.save()
        return assign


class ShowSolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = ['id', 'title', 'answer', 'user', 'created_date']

    def to_representation(self, instance):
        rep = super(ShowSolutionSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        return rep


class SolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = ['title', 'answer', 'files']

    def create(self, validated_data):
        solution = Solution.objects.create(**validated_data)
        solution.save()
        return solution


class StudAssignmentSerializer(serializers.ModelSerializer):
    deadline = serializers.RelatedField(source='Assigment', read_only=True)

    class Meta:
        model = Solution
        fields = ['id', 'ass', 'deadline', 'title', 'points', 'comments']

    def to_representation(self, instance):
        rep = super(StudAssignmentSerializer, self).to_representation(instance)
        rep['deadline'] = instance.ass.Deadline
        rep['ass'] = instance.ass.Name
        return rep
