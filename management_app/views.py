from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from management_app.EmailBackEnd import EmailBackEnd
from management_app.models import CustomUser, Courses, SessionYearModel


def ShowLoginPage(request): # homepage as assigned
    return render(request, "login_page.html")


def doLogin(request):   # loigin verification and redirect to respective page
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    else:   
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))

        if user != None:    # if user exists
            login(request, user)

            # redirects to the specific page according to the usertype
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_page')

            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))

            else:
                return HttpResponseRedirect(reverse("student_home"))
            
        else:       # if user not found or invalid entry
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def GetUserDetails(request):    # fetches the respective user details 
    if request.user != None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))

    else:   # if user already exists
        return HttpResponse("Please Login First")


# Used Firebase to send notification to staff and student
def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
        'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
        'var firebaseConfig = {' \
        '        apiKey: "YOUR_API_KEY",' \
        '        authDomain: "FIREBASE_AUTH_URL",' \
        '        databaseURL: "FIREBASE_DATABASE_URL",' \
        '        projectId: "FIREBASE_PROJECT_ID",' \
        '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
        '        messagingSenderId: "FIREBASE_SENDER_ID",' \
        '        appId: "FIREBASE_APP_ID",' \
        '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
        ' };' \
        'firebase.initializeApp(firebaseConfig);' \
        'const messaging=firebase.messaging();' \
        'messaging.setBackgroundMessageHandler(function (payload) {' \
        '    console.log(payload);' \
        '    const notification=JSON.parse(payload);' \
        '    const notificationOption={' \
        '        body:notification.body,' \
        '        icon:notification.icon' \
        '    };' \
        '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
        '});'

    return HttpResponse(data, content_type="text/javascript")


def signup_admin(request):
    return render(request, "signup_admin_page.html")


def signup_staff(request):
    return render(request, "signup_staff_page.html")


def signup_student(request):
    courses = Courses.objects.all()
    session_years = SessionYearModel.object.all()
    context = {"courses": courses, "session_years": session_years}
    return render(request, "signup_student_page.html", context)


def do_admin_signup(request):   # signup verification 
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, user_type=1)
        user.save()
        
        messages.success(request, "Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))

    except:
        messages.error(request, "Failed to Create Admin")
        return HttpResponseRedirect(reverse("signup_admin"))


def do_staff_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    sex = request.POST.get("sex")

    try:
        user = CustomUser.objects.create_user(
            last_name=last_name,  first_name=first_name, 
            username=username, password=password, email=email, user_type=2)
        
        user.staffs.address = address
        user.staffs.gender = sex
        user.save()
        
        messages.success(request, "Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))

    except:
        messages.error(request, "Failed to Create Staff")
        return HttpResponseRedirect(reverse("signup_staff"))


def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")
    
    fs = FileSystemStorage()

    user = CustomUser.objects.create_user(
        username=username, password=password, email=email,
        last_name=last_name,  first_name=first_name, user_type=3
        )

    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.save()
    
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
