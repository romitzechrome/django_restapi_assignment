# Generated by Django 3.2.5 on 2021-08-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0032_solution_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='file',
        ),
        migrations.AddField(
            model_name='solution',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='Documents/'),
        ),
    ]
