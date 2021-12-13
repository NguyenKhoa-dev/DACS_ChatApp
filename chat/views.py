from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from .forms import CreateUserForm
from .models import Message, Room, RoomHistory,Information
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

import datetime


@login_required(login_url='Chat:user')
def index(request):
    # rooms = Room.objects.all()
    rhs = RoomHistory.objects.filter(user=request.user)
    rooms = [rh.room for rh in rhs]
    rhs = RoomHistory.objects.all()
    if request.method == 'POST':
        if 'create-room' in request.POST:
            room_name = request.POST.get('room-name')
            password = request.POST.get('room-pwd')
            room = Room.objects.filter(user=request.user, name=room_name).first()
            if room == None:
                room = Room.objects.create(user=request.user, name=room_name, password=password)
                RoomHistory.objects.create(user=request.user, room=room)
            return redirect("Chat:room", room_id=room.id)
        elif 'search-room' in request.POST:
            room_name = request.POST.get('room-name')
            if room_name != "":
                rooms = Room.objects.all()
                rooms = [room for room in rooms if room.name.lower().find(room_name.lower())!=-1]
    # create info user
    if Information.objects.filter(user=request.user).exists() ==False:
        d= datetime.date(2000,1,1)
        Information.objects.create(user=request.user,imagelink='/person.png',birthday=d)
    info_entity = Information.objects.filter(user=request.user).first()
    return render(request, 'chat/index.html', {"rhs": rhs, "rooms": rooms, "user_name": request.user.username,"info_entity":info_entity})


@login_required(login_url='Chat:user')
def room(request, room_id):
    room_entity = Room.objects.filter(id=room_id).first()
    if room_entity == None:
        messages.info(request, 'Khong co phong nay!')
        return redirect("Chat:index")
    if not RoomHistory.objects.filter(room=room_entity, user=request.user).exists():
        room_password=""
        if request.method == "POST":
            room_password = request.POST.get('room-pwd')
        room_entity = Room.objects.filter(id=room_id, password=room_password).first()
        if room_entity == None:
            messages.info(request, 'Mat khau sai!')
            return redirect("Chat:index")
        RoomHistory.objects.create(user=request.user, room=room_entity)
    username = request.user.username
    mgs = Message.objects.filter(room=room_entity)
    mgs = mgs[int(len(mgs)/15):]
    info_entity = Information.objects.filter(user=request.user).first()
    rhs = RoomHistory.objects.filter(room=room_entity)
    infors = [Information.objects.filter(user=rh.user).first() for rh in rhs]
    return render(request, 'chat/room.html', {'room_entity': room_entity, 'username': username, 'messagesUser': mgs, "info_entity":info_entity,"infors":infors})

@login_required(login_url='Chat:user')
def myrooms(request):
    rooms = Room.objects.filter(user = request.user)
    if 'create-room' in request.POST:
        room_name = request.POST.get('room-name')
        password = request.POST.get('room-pwd')
        room = Room.objects.filter(user=request.user, name=room_name).first()
        if room == None:
            room = Room.objects.create(user=request.user, name=room_name, password=password)
            RoomHistory.objects.create(user=request.user, room=room)
        return redirect("Chat:room", room_id=room.id)
    elif 'search-room' in request.POST:
        room_name = request.POST.get('room-name')
        if room_name != "":
            rooms = [room for room in rooms if room.name.lower().find(room_name.lower())!=-1]
    # create info user
    if Information.objects.filter(user=request.user).exists() == False:
        d= datetime.date(2000,1,1)
        Information.objects.create(user=request.user,imagelink='/person.png',birthday=d)
    info_entity = Information.objects.filter(user=request.user).first()
    return render(request, 'chat/myrooms.html', {"rooms": rooms, "user_name": request.user.username,"info_entity":info_entity})

def UserLoginRegister(request):
    if request.user.is_authenticated:
        return redirect('Chat:index')
    else:
        if request.method != 'POST':
            form = CreateUserForm()
        else:
            if 'Sign-up' in request.POST:
                form = CreateUserForm(data=request.POST)
                if form.is_valid():
                    form.save()
                    userSignUp = form.cleaned_data.get('username')
                    messages.success(
                        request, 'Account was created for ' + userSignUp)

            elif 'Login' in request.POST:
                username = request.POST.get('user_signin')
                password = request.POST.get('pwd_signin')
                user = authenticate(
                    request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('Chat:index')
                else:
                    messages.info(
                        request, 'Username or password is incorrect!')
                    return redirect('Chat:user')
        context = {'form': form}
        return render(request, 'User/User.html', context)

@login_required(login_url='Chat:user')
def deleteRoom(request,room_id):
    room = Room.objects.get(id=room_id)
    if room.user == request.user:
        room.delete()
        messages.info(request,'delete successfully!')
    else:
        messages.info(request,'Invalid user!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='Chat:user')
def escapeRoom(request,room_id):
    room = Room.objects.get(id=room_id)
    rh = RoomHistory.objects.get(room=room,user=request.user)
    if rh != None:
        rh.delete()
        messages.info(request,'escape successfully!')
    else:
        messages.info(request,'Invalid processing!')
    return redirect('Chat:index')

@login_required(login_url='Chat:user')
def updateRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    info_entity = Information.objects.filter(user=request.user).first()

    if (request.method == "POST"):
        roomName = request.POST.get('room-name-update')
        roomPwd = request.POST.get('room-pwd-update')
        if (room.password == roomPwd):
            if not 'chk-update-room-pwd' in request.POST:
                room.name = roomName
                Room.save(room)
                messages.info(request, 'Update Room Name successfully')
                return redirect("Chat:index")
            else:
                newPwd = request.POST.get('room-new-pwd-update')
                confirmPwd = request.POST.get('room-confirm-pwd-update')
                if newPwd == confirmPwd:
                    room.name = roomName
                    room.password = newPwd
                    Room.save(room)
                    messages.info(request, 'Update Password successfully')
                    return redirect("Chat:index")
                else:
                    messages.info(request, 'New password and confirm password didn\'t match!')
        else:
            messages.info(request, 'Password is incorrect!')

    context = {'room': room, 'username': request.user.username, "info_entity":info_entity}
    return render(request, 'chat/update.html', context)

def logoutUser(request):
    logout(request)
    return redirect('Chat:user')

def account_view(request,user_name):
    # getID_room = 
    if Information.objects.filter(user=request.user).exists() ==False:
        d= datetime.date(2000,1,1)
        Information.objects.create(user=request.user,imagelink='/person.png',birthday=d)
    info_entity = Information.objects.filter(user=request.user).first()  
    return render(request,'user/info.html',{'info_entity':info_entity,'username':request.user.username})

@login_required(login_url='Chat:user')
def edit_account_view(request,user_name):
    info_entity = Information.objects.filter(user=request.user).first()
    if request.method == 'POST':
        user_name_edit = request.POST.get('username')
        birth_day = request.POST.get('birthday')
        image_link = request.FILES.get('profileimage')
        
        User.objects.filter(username=request.user).update(username=user_name_edit)
        
        info_entity.birthday= birth_day
        info_entity.imagelink=image_link
        info_entity.save()
        
        return redirect('Chat:viewinfo',user_name_edit)
        
    return render(request,"user/edit_info.html",{"info_entity":info_entity})

