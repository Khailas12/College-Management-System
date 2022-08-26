import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student.forms import AddStudentForm, EditStudentForm
from management_app.models import (
    CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel,
    FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, NotificationStudent, NotificationStaffs
)


def admin_page(request):    # admin homepage that shows the graphs and status
    student_count1 = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []

    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []

    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(
            staff_id=staff.id, leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []

    for student in students_all:
        attendance = AttendanceReport.objects.filter(
            student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(
            student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(
            student_id=student.id, leave_status=1).count()

        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)

    return render(
        request, "admin_template/home_content.html",
        {"student_count": student_count1, "staff_count": staff_count, "subject_count": subject_count,
         "course_count": course_count, "course_name_list": course_name_list, "subject_count_list": subject_count_list, "student_count_list_in_course": student_count_list_in_course, "student_count_list_in_subject": student_count_list_in_subject, "subject_list": subject_list, "staff_name_list": staff_name_list,
         "attendance_present_list_staff": attendance_present_list_staff, "attendance_absent_list_staff": attendance_absent_list_staff, "student_name_list": student_name_list, "attendance_present_list_student": attendance_present_list_student, "attendance_absent_list_student": attendance_absent_list_student}
    )


def add_staff(request):     # add staff page
    return render(request, "admin_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")

    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        try:
            # creates a user uniquely cross checking everything with database
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email,
                last_name=last_name, first_name=first_name, user_type=2)

            user.staffs.address = address
            user.save()

            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("manage_staff"))

        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, "admin_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")

    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()

            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("manage_course"))

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    form = AddStudentForm()
    context = {"form": form}
    return render(request, "admin_template/add_student_template.html", context)


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")

    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            fs = FileSystemStorage()
            try:
                user = CustomUser.objects.create_user(
                    username=username, password=password, email=email,
                    last_name=last_name, first_name=first_name, user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year = SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender = sex
                user.save()

                messages.success(request, "Student Added Succesfully")
                return HttpResponseRedirect(reverse("manage_student"))

            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            context = {"form": form}
            return render(request, "admin_template/add_student_template.html", context)


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    context = {"staffs": staffs, "courses": courses}
    return render(request, "admin_template/add_subject_template.html", context)


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,
                               course_id=course, staff_id=staff)
            subject.save()

            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("manage_subject"))

        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    context = {"staffs": staffs}
    return render(request, "admin_template/manage_staff_template.html", context)


def manage_student(request):
    students = Students.objects.all()
    context = {"students": students}
    return render(request, "admin_template/manage_student_template.html", context)


def manage_course(request):
    courses = Courses.objects.all()
    context = {"courses": courses}
    return render(request, "admin_template/manage_course_template.html", context)


def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {"subjects": subjects}
    return render(request, "admin_template/manage_subject_template.html", context)


def delete_subject(request, id):
    if request.method == "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        subject_id = request.POST.get("subject_id")
        subject = Subjects.objects.get(id=id)
        subject.delete()

        context = {"subject_id": subject_id, "id": subject_id}
        messages.error(request, "Subject Deleted")
        return HttpResponseRedirect(reverse("manage_subject"), context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    context = {"staff": staff, "id": staff_id}
    return render(request, "admin_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))

        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def delete_staff(request, staff_id):
    if request.method == "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        request.session['staff_id'] = staff_id
        staff = Staffs.objects.get(admin=staff_id)
        staff.delete()

        context = {"staff_id": staff_id, "id": staff_id}
        messages.error(request, "Staff Deleted")
        return HttpResponseRedirect(reverse("manage_staff"), context)


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()

    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {"form": form, "id": student_id,
               "username": student.admin.username}
    return render(request, "admin_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender = sex
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                student.save()

                del request.session['student_id']

                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

            except:
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))

        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)

            context = {"form": form, "id": student_id,
                       "username": student.admin.username}
            return render(request, "admin_template/edit_student_template.html", context)


def delete_student(request, student_id):
    if request.method == "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        request.session['student_id'] = student_id
        student = Students.objects.get(admin=student_id)
        student.delete()

        context = {"student_id": student_id, "id": student_id}
        messages.error(request, "Student Deleted")
        return HttpResponseRedirect(reverse("manage_student"), context)


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)

    context = {"subject": subject, "staffs": staffs,
               "courses": courses, "id": subject_id}
    return render(request, "admin_template/edit_subject_template.html", context)


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)

    context = {"course": course, "id": course_id}
    return render(request, "admin_template/edit_course_template.html", context)


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")

        try:
            course = Courses.objects.get(id=course_id)
            print(Courses.course_name)
            course.course_name = course_name
            course.save()

            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))

        except:
            messages.error(request, "Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))


def delete_course(request, id):
    if request.method == "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        course_id = request.POST.get("course_id")
        course = Courses.objects.get(id=id)
        course.delete()

        context = {"course_id": course_id, "id": course_id}
        messages.error(request, "Course Deleted")
        return HttpResponseRedirect(reverse("manage_course"), context)


def manage_session(request):
    return render(request, "admin_template/manage_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))

    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(
                session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()

            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("view_session_year"))

        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


def view_session_year(request):
    session_years = SessionYearModel.object.all()

    context = {"session_years": session_years}
    return render(request, "admin_template/view_session_year.html", context)


def delete_session_year(request, id):
    if request.method == "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        year_id = request.POST.get("year_id")
        year = SessionYearModel.object.get(id=id)
        year.delete()

        context = {"year_id": year_id, "id": year_id}
        messages.error(request, "Academic Year Deleted")
        return HttpResponseRedirect(reverse("manage_session"), context)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()

    if user_obj:
        return HttpResponse(True)

    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()

    if user_obj:
        return HttpResponse(True)

    else:
        return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {"feedbacks": feedbacks}
    return render(request, "admin_template/staff_feedback_template.html", context)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {"feedbacks": feedbacks}
    return render(request, "admin_template/student_feedback_template.html", context)


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {"leaves": leaves}
    return render(request, "admin_template/staff_leave_view.html", context)


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {"leaves": leaves}
    return render(request, "admin_template/student_leave_view.html", context)


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.object.all()
    return render(
        request, "admin_template/admin_view_attendance.html",
        {"subjects": subjects, "session_year_id": session_year_id}
    )


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(
        subject_id=subject_obj, session_year_id=session_year_obj
    )
    attendance_obj = []

    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(
            attendance_single.attendance_date), "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " "+student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {"user": user}
    return render(request, "admin_template/admin_profile.html", context)


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))

    else:
        password = request.POST.get("password")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.save()

            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_send_notification_student(request):
    students = Students.objects.all()
    context = {"students": students}
    return render(request, "admin_template/student_notification.html", context)


def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    context = {"staffs": staffs}
    return render(request, "admin_template/staff_notification.html", context)


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student = Students.objects.get(admin=id)
    token = student.fcm_token

    url = "https://fcm.googleapis.com/fcm/send"

    body = {
        "notification": {
            "title": "College Management System",
            "body": message,
            "click_action": "shorturl.at/cgh07",
            "icon": "shorturl.at/gmOV8"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=SERVER_KEY_HERE"}

    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStudent(student_id=student, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(admin=id)

    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"

    body = {
        "notification": {
            "title": "College Management System",
            "body": message,
            "click_action": "shorturl.at/deIJ2",
            "icon": "https://res.cloudinary.com/dzzjp6xlv/image/upload/v1661474583/logo_b7edsg.png"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "key=SERVER_KEY_HERE"}

    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaffs(staff_id=staff, message=message)
    notification.save()

    print(data.text)
    return HttpResponse("True")
