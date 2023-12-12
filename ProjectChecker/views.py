from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . models import CustomUser, Project, Department
from . forms import RegisterForm, UpdateUserForm,RegisterLecturerForm

# Create your views here.

def student_dashboard(request):
    if request.method == "GET":
        q = request.GET.get('q')
                               
        if q is not None:
            q = q
            department = Department.objects.filter(
                         Q(name__icontains= q))
        else:
            q = ''
            department = Department.objects.all()
            
    context = {'department':department}
    return render(request,'ProjectChecker/student.html',context)

def lecturer_dashboard(request):
    if request.method == "GET":
        q = request.GET.get('q')
                               
        if q is not None:
            q = q
            department = Department.objects.filter(
                         Q(name__icontains= q))
        else:
            q = ''
            department = Department.objects.all()
            
    context = {'department':department}
    return render(request,'ProjectChecker/lecturer.html',context)

def sessions(request , pk):
    department = Department.objects.get(id = pk)
    if request.method == "GET":
        q = request.GET.get('q')
                               
        if q is not None:
            q = q
            year = Project.objects.filter(
                         Q(session__iexact=q))
        else:
            q = ''
            year = Project.objects.filter(department=department).first()
            
    year = Project.objects.filter(department=department).first()
    first  = '2022/2023'
    second = '2021/2022'
    third = '2020/202'
    forth = '2019/2020'
    fifth = '2022/2023'
    context = {'year':year,'pk':pk,'first':first,'second':second,'third':third,'forth':forth,'fifth':fifth,}
    return render(request, 'ProjectChecker/sessions.html',context)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:    
        if request.method == "POST":
            email = request.POST["email" ]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None and user.status=='student':
                login(request,user)
                return redirect('lecturer_dashboard')
            elif user is not None and user.status=='lecturer':
                login(request,user)
                return redirect('lecturer_dashboard')     
            else:
                error_message = "Invalid Email Or Password"
                return render(request,"ProjectChecker/login.html",{"error_message":error_message})

    return render(request,"ProjectChecker/login.html")

def login_select(request):
    
    return render(request,"ProjectChecker/login_select.html")

def logout_user(request):
    logout(request)
    return redirect('student_dashboard')


@login_required(login_url='/login_user')
def profile(request):
    user = request.user
    
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            messages.error(request, "Invalid Input")
    
    context = {"form": form,}

    return render(request, "ProjectChecker/profile.html", context)

def student_signup(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.status = 'student'
                user.username = user.username.lower()
                user.save()

                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Error creating account. Please check the form.")
        
        else:
            form = RegisterForm()
        
        context = {"form": form}
        return render(request, "ProjectChecker/student_signup.html", context)
    
def lecturer_signup(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard')
    else:
        if request.method == "POST":
            form = RegisterLecturerForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.status = 'lecturer'
                user.save()

                login(request, user)
                messages.success(request, "Account created successfully!")
                return redirect('lecturer_dashboard')
            else:
                messages.error(request, "Error creating account. Please check the form.")
        
        else:
            form = RegisterLecturerForm()
        
        context = {"form": form}
        return render(request, "ProjectChecker/lecturer_signup.html", context)
    
@login_required(login_url='/login_user')
def upload_project(request):
    if request.method == "POST":
        projects =  Project.objects.all()
        department = request.POST.get('department')
        title = request.POST.get('title')
        for check in projects:
            if check.title == title:
                upload_error  = "Sorry Similar Topic Name Already Exist"
                context = {'upload_error':upload_error}
                go_on = False
                return render(request,"ProjectChecker/upload.html",context)
            elif check.title == title and check.status == 'declined':
                upload_error  = "Similar Topic Has been rejected in the past"
                context = {'upload_error':upload_error}
                go_on = False
                return render(request,"ProjectChecker/upload.html",context)
            else:
                go_on = True
        if go_on == True:
            try:
                project = Project.objects.create(
                    author = request.user,
                    title = request.POST.get('title'),
                    content = request.POST.get('content'),
                    department = Department.objects.get(name = department),
                    session = request.POST.get('session'),
                    status = 'pending',
                )
            except:
                if request.user.projects is not None:
                    upload_error  = "Sorry You Already Have A Project, Please Contact Admin"
                    context = {'upload_error':upload_error}
                    return render(request,"ProjectChecker/upload.html",context)
                else:
                    upload_error  = "Invalid Input"
                    context = {'upload_error':upload_error}
                    return render(request,"ProjectChecker/upload.html",context)
        else:
            return render(request,"ProjectChecker/upload.html")
        
    return render(request,"ProjectChecker/upload.html")

def approve_project(request,project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = 'approved'
    project.save()

    return redirect(request.META.get('HTTP_REFERER', 'topics'))

def decline_project(request,project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = 'declined'
    project.save()

    return redirect(request.META.get('HTTP_REFERER', 'topics'))

def approved_projects(request,pk):
    # fetched_projects = Project.objects.get(session = pk)
    # session = fetched_projects.session
    approved_projects = Project.objects.filter(session = pk , status = 'approved')
    if request.method == "GET":
        q = request.GET.get('q')

        if q is not None:
            q = q
            approved_projects = Project.objects.filter(
                                                    Q(title__icontains=q),
                                                         session =  pk , status = 'approved')
            url_action= 'approved_projects'  
            context = {'approved_projects':approved_projects,'pk':pk,'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 
        else:
            q = ''
            approved_projects = Project.objects.filter(session = pk , status = 'approved')
            url_action= 'approved_projects'
            context = {'approved_projects':approved_projects,'pk':pk,'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 

    url_action= 'approved_projects'                                             
    context = {'approved_projects':approved_projects,'pk':pk,'url_action':url_action}
    return render(request, 'ProjectChecker/approved.html',context) 

def rejected_projects(request,pk):
    # fetched_projects = Project.objects.get(id = pk)
    # session = fetched_projects.session
    approved_projects = Project.objects.filter(session = pk , status = 'declined')
    if request.method == "GET":
        q = request.GET.get('q')

        if q is not None:
            q = q
            approved_projects = Project.objects.filter(
                                                    Q(title__icontains=q),
                                                         session = pk , status = 'declined')
            url_action= 'rejected_projects'  
            context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 
        else:
            q = ''
            approved_projects = Project.objects.filter(session = pk , status = 'declined')
            url_action= 'rejected_projects'
            context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 

    url_action= 'rejected_projects'                                             
    context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
    return render(request, 'ProjectChecker/approved.html',context) 

def pending_projects(request,pk):
    # fetched_projects = Project.objects.get(id = pk)
    # session = fetched_projects.session
    approved_projects = Project.objects.filter(session = pk , status = 'pending')
    if request.method == "GET":
        q = request.GET.get('q')

        if q is not None:
            q = q
            approved_projects = Project.objects.filter(
                                                    Q(title__icontains=q),
                                                         session = pk , status = 'pending')
            url_action= 'pending_projects'  
            context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 
        else:
            q = ''
            approved_projects = Project.objects.filter(session = pk , status = 'pending')
            url_action= 'pending_projects'
            context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
            return render(request, 'ProjectChecker/approved.html',context) 

    url_action= 'pending_projects'                                             
    context = {'approved_projects':approved_projects,'pk':pk, 'url_action':url_action}
    return render(request, 'ProjectChecker/approved.html',context) 

def project_detail(request,pk):
    project = Project.objects.get(id=pk)
    url_action = 'Project Detail'
    context = {'project':project}
    return render(request,'ProjectChecker/details.html',context)