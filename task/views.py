from django.shortcuts import render,redirect
from .models import task
from .forms import taskForm
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def home(request):
    obj=task.objects.all()
    form=taskForm
    if request.method=='POST':
        form=taskForm(request.POST)
        if form.is_valid():
          form.save()
        return redirect('home')
    return render(request,'index.html',{'obj':obj,'form':form})



def delete(request,id): 
    obj=task.objects.get(id=id)
    if request.method=='POST':
        obj.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':obj})


def update(request,id):
    obj=task.objects.get(id=id)
    form=taskForm(instance=obj)
    if request.method=='POST':
        form=taskForm(request.POST,instance=obj)
        if form.is_valid():
          form.save()
        return redirect('home')
    return render(request,'update.html',{'obj':obj,'form':form})
    
def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'User already exists')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=pass2)  
                user.save()     
                return redirect('login')
        else:
            messages.info(request,'password does not match')    
    return render(request,'register.html')



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        pass2=request.POST['password']
        user=auth.authenticate(username=username,password=pass2)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
    return render(request,'login.html')


def logout(request):
    auth.logout(request)  
    return redirect('/')  