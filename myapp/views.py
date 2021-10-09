 
 
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import *
from . forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
 
 # Create your views here.


# Home Page Views 

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Room.objects.filter(Q(topic__name__icontains=q)  |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    ) 
    topics = Topic.objects.all() 
    room_count = room.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context =  {'rooms':room,'topic':topics,'room_count':room_count,'room_messages':room_messages }
    return render(request,'index.html',context)  


    # Room Page Views   


def room(request, pk):
    room =Room.objects.get(id=pk)  
    room_messages = room.message_set.all()
    participants = room.participants.all() 

    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,room=room,
            msg_body=request.POST.get('msg_body')
        )
        participants=room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'room.html', {'room':room,'msg':room_messages,'participants':participants})



@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
      
        return redirect('index')
    context={ 'topics':topics}
    return render(request,'room_form.html',context) 




@login_required(login_url='login')
def updateroom(request,pk):
    room  =Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse( "<h1> You are not allowed </h1> " )

    if request.method=='POST':

        topic_name=request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name=request.POST.get('name') 
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('index')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'room_form.html',context)




@login_required(login_url='login')
def deleteroom(request,pk): 

    room = Room.objects.get(id=pk)
    context = {"obj":room}
    if request.user != room.host:
        return HttpResponse('<h1>"You are not allowed"</h1>')
    if request.method=='POST':
        room.delete()
        return redirect('index')

    return render(request,'delete.html', context)


# Delete Message Views


def deletemsg(request,pk): 

    msg = Message.objects.get(id=pk)
    context = {"obj":msg}
    if request.user != msg.user:
        return HttpResponse('<h1>"You are not allowed"</h1>')
    if request.method=='POST':
        msg.delete()
        return redirect('index')

    return render(request,'delete.html', context)    


# User Deatil Views


def userprofile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics = Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topic':topics}
    return render(request,'profile.html',context)    



@login_required(login_url='login')
def userupdate(request):
    user=request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form =  UserForm(request.POST,request.FILES,instance=user)
        form.save()
        return redirect('profile', pk=user.id)
    return render(request,'update_user.html',{'form':form})


# User Authentication Views


def registerpage(request):
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
    return render(request,'register.html',{'form':form})        



def loginpage(request):
    page= 'login'
    # if request.user.is_authenticated:
    #     return redirect('index')
    if request.method=='POST':
        username= request.POST.get('username').lower()    
        password= request.POST.get('password') 
        user=authenticate(username=username,password=password)  
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return redirect('login')
                 
    context={}             
    return render(request,'login.html',context)           


def logoutpage(request):
    logout(request)
    return redirect('login')


# Recent Activities and Topic Views

def activities(request):
    room_messages = Message.objects.all()
    return render(request,'activities.html',{'room_messages':room_messages})


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topic = Topic.objects.filter(name__icontains=q)
    return render(request,'topics.html',{'topic':topic})
