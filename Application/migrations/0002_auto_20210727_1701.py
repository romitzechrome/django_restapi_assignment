# Generated by Django 3.2.5 on 2021-07-27 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigment',
            name='Answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Application.solution'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
