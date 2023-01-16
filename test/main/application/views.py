from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from main import settings
from django.contrib.auth import authenticate, login, logout
from main import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 
from . token_start import generate_token
from .helpers import send_maill
import uuid
from .models import Profile
from django.views import generic
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter().order_by('-created_on')
    template_name = 'index.html'
    def index(request):
        return render(request, 'index.html')
def account(request):
    from django.contrib import messages


    if request.method == 'POST':
        username = request.POST["username"]
        name = request.POST["Name"]
        age = request.POST["age"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]
        checkbox = request.POST["checkbox"]

        if User.objects.filter(username=username):
            messages.error(request, "username already exist! Please try some other username.")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
        
        if len(username)>20:
            messages.error(request, "The Username must be under 20 characters!!")
            username = None
            password = None
            email = None

        if len(password) < 5:
            messages.error(request, "The password must be above 5 characters!!")
        
        if password != cpassword:
            messages.error(request, "Passwords didn't matched!!")
        
        if not username.isalnum():
            messages.error(request, "username must be Alpha-Numeric!!")

        myuser = User.objects.create_user(username, email, password)
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        subject = "Welcome to SmartBite."
        messages = "Hello " + name + " please confirm your email address, \n SmartBite officially Security Email Account."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, messages, from_email, to_list, fail_silently = True)

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ SmartBite Login!!"
        message2 = render_to_string('tabs/email_confirmation.html',{
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
            })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect(signin)
        
    return render(request, 'tabs/account.html')

def activate(request,uidb64,token):
    try:
        uid = force_str (urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect(signin)
    else:
        return render(request,'activation_faild.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            username = user.username
            # messages.success(request, "Logged In Sucessfully!!")
            context = {"username":username}
            return render(request, 'tabs/account.html', context)
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect("/")
    
    return render(request, "tabs/login.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("/")

def contact(request):
    return render(request, 'tabs/contact.html')

def about_us(request):
    return render(request, 'tabs/About_us.html')
