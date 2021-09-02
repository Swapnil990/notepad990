from core.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile,Notes
import uuid
from django.contrib import auth
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.conf import settings
#--------------------------------------------------------------------------------------------
@login_required
def home(request):
    notes = Notes.objects.filter(user = request.user)
    return render(request , 'home.html', {
        'notes':notes
    })


#--------------------------------------------------------------------------------------------


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username = username).first():
            messages.success(request , 'Username is Taken')
            return redirect('/register')
        if User.objects.filter(email = email).first():
            messages.success(request, 'Email is taken')
            return redirect('/register')
        
        obj = User.objects.create(username=username,email=email)
        obj.set_password(password)
        obj.save()
        auth_token = str(uuid.uuid4())
        profile = Profile.objects.create(user = obj, auth_token = auth_token)
        profile.save()
        send_mail_verify( email, auth_token)
        

        return redirect('/token_send')

        
    return render(request , 'register.html')


#--------------------------------------------------------------------------------------------



def login_custom(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        obj = User.objects.filter(username=username).first()

        if obj is None:
            messages.success(request, 'User not found !!')
            return redirect('/login')
        profile = Profile.objects.filter(user=obj).first()
        if not profile.is_verified:
            messages.success(request, 'Profile is not verified !! Please check your mail')
            return redirect('/login')
        
        user = authenticate(username=username , password=password)
        if user is None:
            messages.success(request, 'Enter Valid Credentials !!')
            return redirect('/login')
        login(request,user)
        return redirect('/')
    return render(request , 'login.html')

#--------------------------------------------------------------------------------------------

def send_mail_verify(email,token):
    subject = 'Your account needs to be verified'
    message = f'Hi! paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
#--------------------------------------------------------------------------------------------

def token_send(request):
    return render(request, 'token_send.html')

#--------------------------------------------------------------------------------------------

def verify(request, auth_token):
    profile = Profile.objects.filter(auth_token = auth_token).first()

    if profile:
        profile.is_verified = True
        profile.save()
        messages.success(request, 'Your account has been Verified')
        return redirect('/login')
    else:
        return redirect('/error')

#--------------------------------------------------------------------------------------------


def error(request):
    return render(request, 'error.html')

#--------------------------------------------------------------------------------------------

def create(request):
    return render(request, 'create_note.html')

#--------------------------------------------------------------------------------------------
def addnote(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    

    obj = Notes.objects.create(title=title , user = request.user , description = description)
    obj.save()
    return redirect('/')

#--------------------------------------------------------------------------------------------

def update(request, id):
    if request.method == 'GET':
        obj = Notes.objects.filter(user = request.user)
        obj1 = obj.get(pk=id)
        
        return render(request, 'update_note.html', {
            'obj1':obj1,
            'id':id
        })
    
 #--------------------------------------------------------------------------------------------       

def save_update(request , id):
    title = request.POST.get('title')
    description = request.POST.get('description') 

    obj = Notes.objects.get(user = request.user , pk=id)
    
    obj.title = title
    obj.description = description
    obj.save()
    
    return redirect('/')

#--------------------------------------------------------------------------------------------

def delete_note(request , id ):
    Notes.objects.get(pk=id).delete()
    return redirect('/')

#--------------------------------------------------------------------------------------------

def logout_custom(request):
    auth.logout(request)
    return redirect('/login')

