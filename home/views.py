from datetime import date, datetime
from multiprocessing import pool
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from home.models import contact, userInfo, userCarpools
from django.conf import settings
from geopy.geocoders import Nominatim
from geopy import distance
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def homepage(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

@login_required(login_url='/login')
def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        feedback = contact(name=name , email=email , message=message)
        feedback.save()

    return render(request,'feedback.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(login)
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect(login)
            else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password, email=email)
                user.save()
                
                return redirect(login)


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(homepage)
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect(login)

def logout_user(request):
    auth.logout(request)
    return redirect(homepage)

# def user_registration(request):
#     return render(request,'reg.html')

@login_required(login_url='/login')
def search(request):

    if request.method == 'POST':
        start = request.POST['starting']
        dest = request.POST['destination']
        
        results = userCarpools.objects.filter(start=start , to=dest).values()
        check = results.exists()
        context = {'searchResults':results , 'check':check}

        return render(request,'search.html',context)


def user_profile(request):

    current_user = request.user
    active_user_id = current_user.id

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        gender= request.POST['gender']
        dob= request.POST['dob']
        address= request.POST['address']
        pin= request.POST['pin']
        drivelic= request.POST['drivelic']
        drivelicpic= request.POST['drivelicpic']


        profileInfo = userInfo(firstname=firstname , lastname=lastname , email=email , mobile=mobile , gender=gender , dob=dob , address=address , pin=pin , drivelic=drivelic ,  drivelicpic=drivelicpic , user_id=active_user_id)

        profileInfo.save()

    if(userInfo.objects.filter(user_id=active_user_id).exists()):
    
        userData = userInfo.objects.filter(user_id=active_user_id)
        dataCount = userData.count()
        sortedUserData = userInfo.objects.filter(user_id=active_user_id).values()[dataCount-1]
    
        context={'userData':sortedUserData}
        
        return render(request,'reg.html',context)
    
    else:
        return render(request,'regform.html')

def update_profile(request):
    if request.method == 'POST':        
        return render(request,'regform.html')



def carpools(request):

    current_user = request.user
    active_user_id = current_user.id

    if request.method == 'POST':
        start = request.POST['start']
        to = request.POST['to']
        poolDate = request.POST['poolDate']
        poolTime = request.POST['poolTime']
        brand = request.POST['brand']
        carNo = request.POST['carNo']
        color = request.POST['color']
        
        geocoder = Nominatim(user_agent="carpoolPrice")
        location1=start + " ,india"
        location2=to + " ,india"
        coordinates1=geocoder.geocode(location1)
        coordinates2=geocoder.geocode(location2)
        lat1,long1=(coordinates1.latitude),(coordinates1.longitude)
        lat2,long2=(coordinates2.latitude),(coordinates2.longitude)
        placel=(lat1,long1)
        place2=(lat2,long2)
        travelDist = round(distance.distance(placel,place2).km)
        milage = 19
        petrol = 105
        mnt = 35

        if travelDist<=20:
            price = 50
        else:
            price = (((travelDist/milage)*petrol)*0.25)+mnt
        
        carpoolInfo = userCarpools(start=start , to=to , poolDate=poolDate , poolTime=poolTime , brand=brand , carNo=carNo , price=price ,  color=color , user_id=active_user_id)
        carpoolInfo.save()

    carpoolData = userCarpools.objects.filter(user_id=active_user_id).values()

    context = {'carpoolData':carpoolData}

    return render(request,'carpools.html',context)

def fullCarpool(request,carpoolId):

    carpoolInfo = userCarpools.objects.filter(id=carpoolId).values()
    
    carpoolUser = 0
    for y in carpoolInfo:
        carpoolUser = y['user_id']

    userData = userInfo.objects.filter(user_id=carpoolUser).values()
    dataCount = userData.count()
    sortedUserData = userInfo.objects.filter(user_id=carpoolUser).values()[dataCount-1]

    context = {
        'carpoolId':carpoolId , 
        'carpoolInfo':carpoolInfo , 
        'sortedUserData':sortedUserData,
    }


    return render(request,'fullCarpool.html',context)

def fullCarpoolSearch(request,carpoolId):

    carpoolInfo = userCarpools.objects.filter(id=carpoolId).values()
    
    carpoolUser = 0
    for y in carpoolInfo:
        carpoolUser = y['user_id']

    userData = userInfo.objects.filter(user_id=carpoolUser).values()
    dataCount = userData.count()
    sortedUserData = userInfo.objects.filter(user_id=carpoolUser).values()[dataCount-1]

    context = {
        'carpoolId':carpoolId , 
        'carpoolInfo':carpoolInfo , 
        'sortedUserData':sortedUserData,
    }

    return render(request,'fullCarpoolSearch.html',context)

def deleteCarpool(request,carpoolId):

    record = userCarpools.objects.get(id=carpoolId)
    record.delete()
    return redirect('/carpools')