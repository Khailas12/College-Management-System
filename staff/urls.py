from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from management_app.EditResultVIewClass import EditResultViewClass

from . import views


urlpatterns = [
    path('', views.staff_home, name='staff_home'),

    # attendence
    path('staff_take_attendance', views.staff_take_attendance,
         name="staff_take_attendance"),
    path('staff_update_attendance', views.staff_update_attendance,
         name="staff_update_attendance"),
    path('get_students', views.get_students, name="get_students"),
    path('get_attendance_dates', views.get_attendance_dates,
         name="get_attendance_dates"),
    path('get_attendance_student', views.get_attendance_student,
         name="get_attendance_student"),
    path('save_attendance_data', views.save_attendance_data,
         name="save_attendance_data"),
    path('save_updateattendance_data', views.save_updateattendance_data,
         name="save_updateattendance_data"),

    # leave
    path('staff_apply_leave', views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', views.staff_apply_leave_save,
         name="staff_apply_leave_save"),


    path('staff_feedback', views.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', views.staff_feedback_save,
         name="staff_feedback_save"),

    # profile
    path('staff_profile', views.staff_profile, name="staff_profile"),
    path('staff_profile_save', views.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', views.staff_fcmtoken_save,
         name="staff_fcmtoken_save"),


    path('staff_all_notification', views.staff_all_notification,
         name="staff_all_notification"),
    path('staff_add_result', views.staff_add_result, name="staff_add_result"),
    path('save_student_result', views.save_student_result,
         name="save_student_result"),
    path('edit_student_result', EditResultViewClass.as_view(),
         name="edit_student_result"),
    path('fetch_result_student', views.fetch_result_student,
         name="fetch_result_student"),

    # live classroom
    path('start_live_classroom', views.start_live_classroom,
         name="start_live_classroom"),
    path('start_live_classroom_process', views.start_live_classroom_process,
         name="start_live_classroom_process"),

    # path('node_modules/canvas-designer/widget.html',views.returnHtmlWidget,name="returnHtmlWidget"),
     path('node_modules/canvas-designer/widget.html',views.returnHtmlWidget,name="returnHtmlWidget"),
]
