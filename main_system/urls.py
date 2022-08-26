
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from management_app import views
from main_system import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),  # password reset
    
    # apps
    path('',views.ShowLoginPage,name="show_login"),
    path('admin_page/', include('admin_page.urls')),
    path('staff/', include('staff.urls')),
    path('student/', include('student.urls')),
    
    
    # signup 
    path('signup_admin',views.signup_admin,name="signup_admin"),
    path('signup_student',views.signup_student,name="signup_student"),
    path('signup_staff',views.signup_staff,name="signup_staff"),
    
    # signup verification and saving
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('do_staff_signup',views.do_staff_signup,name="do_staff_signup"),
    path('do_signup_student',views.do_signup_student,name="do_signup_student"),
    
    
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
            
    
    path('firebase-messaging-sw.js', views.showFirebaseJS,name="show_firebase_js"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
