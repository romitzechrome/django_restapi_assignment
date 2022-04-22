from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    Course = models.CharField(max_length=100,)

    class Meta:
        verbose_name_plural = "Courses"
    def __str__(self):
        return self.Course


class Assigment(models.Model):
    Name = models.CharField(max_length=100)
    Questions = models.TextField()
    Year = models.CharField(max_length=100)
    Created_date = models.DateTimeField(auto_now_add=True)
    Deadline = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

    # def get_solution(self):
    #     try:
    #         return Solution.objects.get(ass=self)
    #     except Solution.DoesNotExist:
    #         return None


class Solution(models.Model):
    ass = models.ForeignKey(Assigment, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    answer = models.TextField()
    files = models.FileField(upload_to="Documents/", null=True, blank=True)
    points = models.FloatField(null=True, default=0.0)
    comments = models.CharField(max_length=300, null=True)
    created_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ass.Name}"

