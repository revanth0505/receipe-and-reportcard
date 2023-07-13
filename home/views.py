from django.shortcuts import render,redirect
from .utils import send_email_to_client
from django.http import HttpResponse
def home(request):
    peoples=[
        {'name':'Revanth','age':20},
        {'name':'Manvitha','age':24},
    ]
    return render(request,"home/index.html",context={'peoples':peoples,'page':'Home'})
def contact(request):
    return render(request,"home/contacts.html",context={'page':'Contacts'})
def about(request):
    return render(request,"home/about.html",context={'page':'About'})
def success_page(request):
    return HttpResponse("Hey I am success page")
def send_email(request):
    send_email_to_client()
    return redirect('/')