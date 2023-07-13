from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum
# Create your views here.
@login_required(login_url='/login/')
def receipes(request):
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        description=data.get('description')
        image=request.FILES.get('image')
        print(name)
        print(description)
        print(image)
        Receipe.objects.create(
            name=name,
            description=description,
            image=image
        )
        return redirect('/receipes/')
    queryset=Receipe.objects.all()
    if request.GET.get('search'):
        queryset=queryset.filter(name__icontains=request.GET.get('search'))
    
    context={'receipes':queryset,'page':'Receipe'}
    return render(request,'reciepes.html',context)
@login_required(login_url='/login/')
def delete_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')
@login_required(login_url='/login/')
def update_receipe(request,id):
    queryset=Receipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        name=data.get('name')
        description=data.get('description')
        image=request.FILES.get('image')
        queryset.name=name
        queryset.description=description
        if image: 
            queryset.image=image
        queryset.save()
        return redirect('/receipes/')
    context={'receipes':queryset,'page':'Update Receipe'}
    return render(request,'update-receipe.html',context)
def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/receipes/')
    context={'page':'Login'}
    return render(request,'login.html',context)
def register_page(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exist')
            return redirect('/register/')
        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
        ) 
        user.set_password(password) 
        user.save()
        messages.info(request,'User Created Successfully')
        return redirect('/register/')
    context={'page':'Register'}
    return render(request,'register.html',context)
def logout_page(request):
    logout(request)
    return redirect('/login/')
@login_required(login_url='/admin-login/')
def admin_details(request):
    queryset=User.objects.all()
    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(username__icontains=search)|
            Q(first_name__icontains=search)|
            Q(last_name__icontains=search)
              )
        
    
    context={'User':queryset,'page':'User Details'}
    return render(request,'admin.html',context)
def admin_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/admin-details/')
    context={'page':'Admin Login'}
    return render(request,'admin_login.html',context)
def admin_register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        adminkey=request.POST.get('adminkey')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exist')
            return redirect('/register/')
        if not adminkey=="admin":
            messages.info(request,'Wrong Admin Key, Give a valid Admin Key')
            return redirect('/admin-register/')
        user=User.objects.create(
        first_name=first_name,
        last_name=last_name,
        username=username
        ) 
        user.set_password(password) 
        user.save()
        messages.info(request,'User Created Successfully')
        return redirect('/admin-register/')
    context={'page':'Admin Register'}
    return render(request,'admin_register.html',context)
@login_required(login_url='/admin-login/')
def delete_user(request,id):
    queryset=User.objects.get(pk=id)
    queryset.delete()
    return redirect('/admin-details/')
@login_required(login_url='/admin-login/')
def update_user(request,id):
    queryset=User.objects.get(pk=id)
    if request.method=="POST":
        data=request.POST
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        username=data.get('username')
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username already exist')
            return redirect('/admin-details/')
        queryset.first_name=firstname
        queryset.last_name=lastname
        queryset.username=username
        queryset.save()
        return redirect('/admin-details/')
    context={'receipes':queryset,'page':'Update User'}
    return render(request,'update_user.html',context)
def get_students(request):
    queryset=Student.objects.all()
    
    if request.GET.get('search'):
        search=request.GET.get('search')
        queryset=queryset.filter(
            Q(student_name__icontains=search)|
            Q(department__department__icontains=search)|
            Q(student_id__student_id__icontains=search)|
            Q(student_email__icontains=search)
        )
    
    paginator = Paginator(queryset, 10)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    return render(request,'report/students.html',{'queryset':page_obj,'page':'Student Report'})
from .seed import generate_report
def see_marks(request,student_id):
    queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))
    current_rank=-1
    i=1
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-student_age')
    for rank in ranks:
        if student_id==rank.student_id.student_id:
            current_rank=i
            break
        i=i+1
    return render(request,'report/see_marks.html',{'queryset':queryset,'total_marks':total_marks,'page':'Report Card','current_rank':current_rank})