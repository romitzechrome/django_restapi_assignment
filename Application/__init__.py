# class EmployeeMaster(models.Model):

#     DEPARTMENT_NAME = (
#         ('1', ' Network administrator'),
#         ('2', ' User experience designer'),
#         ('3', ' Senior software engineer'),
#         ('4', ' Cloud engineer')
#     )

#     GENDER_CHOICE = (
#         ('1', ' Male'),
#         ('2', 'Female')
#         )

#     emp_id = models.AutoField(db_column="emp_id", primary_key=True, null=False)
#     employee_first_name = models.CharField(db_column="employee_first_name", max_length=255, default="", null=False)
#     employee_last_name = models.CharField(db_column="employee_last_name", max_length=255, default="", null=False)
#     employee_surname = models.CharField(db_column="employee_surname", max_length=255, default="", null=False)
#     department_name = models.CharField(db_column="department_name", max_length=1, choices=DEPARTMENT_NAME,default="",null=False)
#     employee_salary = models.CharField(db_column="employee_salary", max_length=255, default="", null=False)
#     dob = models.DateTimeField(null=True,blank=True)
#     gender = models.CharField(db_column="gender",choices=GENDER_CHOICE, max_length=255, default="", null=False)

#     def __str__(self):
#         return '{} {}'.format(self.employee_first_name, self.employee_last_name)

#     def __as_dict__(self):
#         return {
#             "employee_first_name": self.employee_first_name,
#             "employee_last_name": self.employee_last_name,
#             "employee_surname": self.employee_surname,
#             "department_name": self.department_name,
#             "employee_salary": self.employee_salary,
#             "dob": self.dob,
#             "gender": self.gender,
#         }

#     class Meta:
#         db_table = "employee_master"