# Generated by Django 3.2.5 on 2021-08-16 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0017_auto_20210729_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='dept',
        ),
        migrations.AlterField(
            model_name='assigment',
            name='Deadline',
            field=models.DateField(),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]