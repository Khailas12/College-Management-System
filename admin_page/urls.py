from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_page, name="admin_page"),

    path('add_staff', views.add_staff, name="add_staff"),
    path('add_staff_save', views.add_staff_save, name="add_staff_save"),
    path('add_course/', views.add_course, name="add_course"),
    path('add_course_save', views.add_course_save, name="add_course_save"),
    path('add_student', views.add_student, name="add_student"),
    path('add_student_save', views.add_student_save, name="add_student_save"),
    path('add_subject', views.add_subject, name="add_subject"),
    path('add_subject_save', views.add_subject_save, name="add_subject_save"),
    
    path('manage_staff', views.manage_staff, name="manage_staff"),
    path('manage_student', views.manage_student, name="manage_student"),
    path('manage_course', views.manage_course, name="manage_course"),
    path('manage_subject', views.manage_subject, name="manage_subject"),
    
    path('edit_staff/<str:staff_id>', views.edit_staff, name="edit_staff"),
    path('edit_staff_save', views.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>',
         views.edit_student, name="edit_student"),
    path('edit_student_save', views.edit_student_save, name="edit_student_save"),
    path('edit_subject/<str:subject_id>',
         views.edit_subject, name="edit_subject"),
    path('edit_subject_save', views.edit_subject_save, name="edit_subject_save"),
    path('edit_course/<str:course_id>', views.edit_course, name="edit_course"),
    path('edit_course_save', views.edit_course_save, name="edit_course_save"),
    
    path('manage_session', views.manage_session, name="manage_session"),
    path('add_session_save', views.add_session_save, name="add_session_save"),
    
    path('check_email_exist', views.check_email_exist, name="check_email_exist"),
    path('check_username_exist', views.check_username_exist,
         name="check_username_exist"),
    
    path('student_feedback_message', views.student_feedback_message,
         name="student_feedback_message"),
    path('student_feedback_message_replied', views.student_feedback_message_replied,
         name="student_feedback_message_replied"),
    path('staff_feedback_message', views.staff_feedback_message,
         name="staff_feedback_message"),
    path('staff_feedback_message_replied', views.staff_feedback_message_replied,
         name="staff_feedback_message_replied"),
    
    path('student_leave_view', views.student_leave_view, name="student_leave_view"),
    path('staff_leave_view', views.staff_leave_view, name="staff_leave_view"),
    
    path('student_approve_leave/<str:leave_id>',
         views.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>',
         views.student_disapprove_leave, name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>',
         views.staff_disapprove_leave, name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>',
         views.staff_approve_leave, name="staff_approve_leave"),
    
    path('admin_view_attendance', views.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_dates', views.admin_get_attendance_dates,
         name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', views.admin_get_attendance_student,
         name="admin_get_attendance_student"),
    
    path('admin_profile', views.admin_profile, name="admin_profile"),
    path('admin_profile_save', views.admin_profile_save, name="admin_profile_save"),
    
    path('admin_send_notification_staff', views.admin_send_notification_staff,
         name="admin_send_notification_staff"),
    path('admin_send_notification_student', views.admin_send_notification_student,
         name="admin_send_notification_student"),
    path('send_student_notification', views.send_student_notification,
         name="send_student_notification"),
    path('send_staff_notification', views.send_staff_notification,
         name="send_staff_notification"),
]
