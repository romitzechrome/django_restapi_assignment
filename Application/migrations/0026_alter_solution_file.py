# Generated by Django 3.2.5 on 2021-08-24 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0025_alter_solution_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='file',
            field=models.FileField(default=None, upload_to=''),
        ),
    ]
