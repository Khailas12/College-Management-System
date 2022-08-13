from django.urls import path

from . import views


urlpatterns = [    
            
    path('', views.student_home, name="student"),    # home page
    
    path('student_view_attendance', views.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', views.student_view_attendance_post, name="student_view_attendance_post"),
    
    path('student_apply_leave', views.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', views.student_apply_leave_save, name="student_apply_leave_save"),
    
    path('student_feedback', views.student_feedback, name="student_feedback"),
    path('student_feedback_save', views.student_feedback_save, name="student_feedback_save"),
    
    path('student_all_notification',views.student_all_notification,name="student_all_notification"),
    
    path('student_view_result',views.student_view_result,name="student_view_result"),
    
    path('student_profile', views.student_profile, name="student_profile"),
    path('student_profile_save', views.student_profile_save, name="student_profile_save"),
    
    path('student_fcmtoken_save', views.student_fcmtoken_save, name="student_fcmtoken_save"),
]
