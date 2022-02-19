from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime, timedelta, date

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.reg_val(request.POST)
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    pword = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    each_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pword,
    )
    request.session['user_id'] = each_user.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.log_val(request.POST)
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    each_user = User.objects.filter(email = request.POST['email'])
    request.session['user_id'] = each_user[0].id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def create(request):
    errors = Show.objects.show_val(request.POST)
    if len(errors) != 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    Show.objects.create(
        title =request.POST['title'],
        network =request.POST['network'],
        release_date =request.POST['release_date'],
        description =request.POST['description'],
        owner = User.objects.get(id=request.session['user_id'])
    )
    return redirect('/dashboard')

def dashboard(request):
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'shows':Show.objects.all()
    }
    return render(request, 'dashboard.html', context)

def new(request):
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'new.html', context)

def update(request, show_id):
    show = Show.objects.get(id=show_id)
    show.title = request.POST['title']
    show.network = request.POST['network']
    show.release_date = request.POST['release_date']
    show.description = request.POST['description']
    show.save()
    return redirect('/dashboard')

def delete(request, show_id):
    my_delete = Show.objects.get(id=show_id)
    my_delete.delete()
    return redirect('/dashboard')

def edit(request, show_id):
    my_show = Show.objects.get(id=show_id)
    context = {
        'show': my_show
    }
    return render(request, 'edit.html', context)

def show(request, show_id):
    my_show = Show.objects.get(id=show_id)
    context = {
        'show': my_show
    }
    return render(request, 'show.html', context)
