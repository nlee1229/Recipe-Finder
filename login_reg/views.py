from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt



def root(request):
    if 'user_id' in request.session:
        return redirect('/success')
    context = {
        "users": User.objects.all()
    }
    return render(request, 'login.html', context)

def reg_process(request):
    errors = User.objects.reg_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect('/')
    if User.objects.filter(email=request.POST['email']):
        messages.error(request, "A user with that email already exists!")
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

        newuser = User.objects.create(
            fname = request.POST["fname"],
            lname = request.POST["lname"],
            email = request.POST["email"],
            password = hashed,
        )
        request.session['user_id'] = newuser.id
        return redirect ('/list_ingredients')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if not errors:
        user = User.objects.filter(email=request.POST['email']) 
        if user: 
            logged_user = user.first()
            if bcrypt.checkpw(request.POST["password"].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                if request.session['user_id'] == 8:
                    return redirect('/admin')
                return redirect('/home')
            
    messages.error(request, "Try checking your email or password.")
    return redirect('/')
    
def logout(request):
    request.session.flush()
    return redirect('/')

def delete(request, id):
    d = User.objects.get(id = id)
    d.delete()
    return redirect('/')

#Change the render to redirect to the second app
#Don't forget to copy and paste the 'context' over to the other views.py

#Def Success currently not in use atm.
def success(request):
    if 'user_id' not in request.session:
        request.session.flush()
        return redirect('/')
    return redirect('/home')