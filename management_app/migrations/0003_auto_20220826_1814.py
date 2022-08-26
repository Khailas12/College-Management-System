# Generated by Django 3.2.15 on 2022-08-26 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management_app', '0002_delete_onlineclassroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancereport',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_app.students'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'Admin'), (2, 'Staff'), (3, 'Student')], default=1, max_length=10),
        ),
    ]
