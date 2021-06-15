from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    request.session.flush()
    return render(request,'index.html')

#render success page
def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0] 
    }
    return render (request, 'profile.html', context)


#validate the registration
def register(request):
    if request.method =='POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        #hash the password
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        #create a user
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
            #create a session
        request.session['user_id'] = new_user.id
        return redirect('/profile')
    return redirect('/')


#login
def login(request):
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/profile')
    return redirect('/')


#logout
def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    return render(request, 'new.html')

def create(request):
    errors = Con.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    Con.objects.create(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        plan = request.POST['plan'],
    )
    return redirect('/profile')

def con(request, con_id):
    one_trip = Con.objects.get(id=con_id)
    context = {
    'trip': one_trip,
    }
    return render(request, 'trip.html', context)

def edit(request, trip_id):
    one_trip = Con.objects.get(id=trip_id)
    context = {
    'trip': one_trip
    }
    return render(request, 'edit.html', context)

def update(request, con_id):
    errors = Con.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{con_id}/edit')
    to_update = Con.objects.get(id=con_id)
    to_update.destination = request.POST['destination']
    to_update.start_date= request.POST['start_date']
    to_update.end_date = request.POST['end_date']
    to_update.plan = request.POST['plan']
    to_update.save()

    return redirect('/profile')

def remove(request, con_id):
    to_delete = Con.objects.get(id=con_id)
    to_delete.delete()
    return redirect('/profile')
