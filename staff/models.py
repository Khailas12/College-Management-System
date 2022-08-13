# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# # from management_app.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
# #     LeaveReportStaff, Staffs, FeedBackStaffs, CustomUser, Courses, NotificationStaffs, StudentResult, OnlineClassRoom

# # from management_app.models import (
# #     Students, SessionYearModel, Staffs, CustomUser, Courses
# # )

# import management_app.models 


# class Staffs(models.Model):
#     id = models.AutoField(primary_key=True)
#     admin = models.OneToOneField(
#         management_app.models.CustomUser, on_delete=models.CASCADE
#     )
#     address = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     fcm_token = models.TextField(default="")
#     objects = models.Manager()


# class Subjects(models.Model):
#     id = models.AutoField(primary_key=True)
#     subject_name = models.CharField(max_length=255)
#     course_id = models.ForeignKey(
#         management_app.models.Courses, on_delete=models.CASCADE, default=1)
#     staff_id = models.ForeignKey(
#         management_app.models.CustomUser, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()

# # class SessionYearModel(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     session_start_year = models.DateField()
# #     session_end_year = models.DateField()
# #     object = models.Manager()

# # class Students(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
# #     gender = models.CharField(max_length=255)
# #     profile_pic = models.FileField()
# #     address = models.TextField()
# #     course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
# #     session_year_id = models.ForeignKey(
# #         SessionYearModel, on_delete=models.CASCADE)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now_add=True)
# #     fcm_token = models.TextField(default="")
# #     objects = models.Manager()


# class Attendance(models.Model):
#     id = models.AutoField(primary_key=True)
#     subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
#     attendance_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     session_year_id = models.ForeignKey(
#         management_app.models.SessionYearModel, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class AttendanceReport(models.Model):
#     id = models.AutoField(primary_key=True)
#     student_id = models.ForeignKey(
#         management_app.models.Students, on_delete=models.DO_NOTHING)
#     attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
#     status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class LeaveReportStaff(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.ForeignKey(
#         management_app.models.Staffs, on_delete=models.CASCADE)
#     leave_date = models.CharField(max_length=255)
#     leave_message = models.TextField()
#     leave_status = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class FeedBackStaffs(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.ForeignKey(
#         management_app.models.Staffs, on_delete=models.CASCADE
#     )
#     feedback = models.TextField()
#     feedback_reply = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class NotificationStaffs(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.ForeignKey(
#         management_app.models.Staffs, on_delete=models.CASCADE
#     )
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()


# class OnlineClassRoom(models.Model):
#     id = models.AutoField(primary_key=True)
#     room_name = models.CharField(max_length=255)
#     room_pwd = models.CharField(max_length=255)
#     subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
#     session_years = models.ForeignKey(
#         management_app.models.SessionYearModel, on_delete=models.CASCADE)
#     started_by = models.ForeignKey(
#         management_app.models.Staffs, on_delete=models.CASCADE
#     )
#     is_active = models.BooleanField(default=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     objects = models.Manager()
