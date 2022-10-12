from django.contrib.auth import logout

from ip2geotools.databases.noncommercial import DbIpCity

from django.shortcuts import render, redirect

from django.contrib import messages
from .models import *

from django.contrib.auth import authenticate, login

import uuid
from .utils import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .tokens import generate_token
from django.core.mail import send_mail


def signup(request):
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if ip is None:
        ip = "0.0.0.0"
    try:
        response = DbIpCity.get(ip, api_key="free")
        country = response.country + "|" + response.city
    except:
        country = "Unknown"

    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        mobile_no = request.POST["mob"]
        city = request.POST["city"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already Exist Try another one")
            return redirect("/")
        if User.objects.filter(email=email):
            messages.error(request, "Email already Registered Try another one")
            return redirect("/")
        if len(username) > 35:
            messages.error(request, "Length of username is greater than 35 character")
            return redirect("/")
        if pass1 != pass2:
            messages.error(request, "Different Passwords")
            return redirect("/")
        if pass1 == "":
            messages.error(request, "Password cannot be blank")
            return redirect("/")
        if len(pass1) <= 7:
            messages.error(request, "Too short password")
            return redirect("/")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha Numeric")
            return redirect("/")

        if pass1 == pass2:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.first_name = fname
            my_user.last_name = lname
            my_user.is_active = False
            my_user.save()

            current_site = get_current_site(request)
            domain = current_site.domain
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            uid = urlsafe_base64_encode(force_bytes(my_user.pk))
            token = generate_token.make_token(my_user)

            send_mail_after_registration(request, email, token=token, uid=uid)
            contact = LoginData(username=username, email=email, mobile_no=mobile_no, city=city, location=country,
                                ip_address=ip)
            contact.save()
            return render(request, 'success.html')
        else:
            return redirect('/')


def signout(request):
    logout(request)
    return redirect("/")


def signin(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "Welcome to Kullhadwalla")
        return redirect("/")
    else:
        messages.error(request, "Bad Credentials")
        return redirect("/")


def news(request):
    if request.method == "POST":
        email = request.POST["email"]
        r_mail = NewsLetter.objects.all()[0:]
        for i in r_mail:
            if i == email:
                messages.error(request, "Already registered for newsletter")
                return redirect('/')
            else:
                news = NewsLetter(email=email)
                news.save()
                messages.success(request, "Successfully  signed up for newsletter")
                return redirect('/')


def index(request):
    data = CustomerReview.objects.all()
    product_data = MainData.objects.all()
    head_data = HeadCarousel.objects.all()

    dic = {'data': data, 'md': product_data, 'hd': head_data}

    return render(request, 'index.html', context=dic)


def send_mail_after_registration(request, email, token, uid):
    current_site = get_current_site(request)
    domain = current_site.domain
    # uid = urlsafe_base64_encode(force_bytes(my_user.pk))
    subject = 'Your account needs to be verified'
    message = f'Follow this link to verify your account\n http://{domain}/activate/{uid}/{token} \nTeam Kullhadwalla'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def error_page(request):
    return render(request, 'error.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def product(request):
    return render(request, 'product.html')


def contact(request):
    return render(request, 'contact.html')


def delt(uid):
    Forget.objects.filter(u_no=uid).delete()


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user != None and generate_token.check_token(my_user, token):
        my_user.is_active = True
        my_user.save()
        login(request, my_user)
        messages.success(request, "Account successfully verified")
        return redirect('/')
    else:
        messages.error(request, "User not registered")
        return redirect('/')


def changepassword(request):
    return render(request, 'passreset.html')


def passwordchange(request):
    email = request.POST["email"]
    # username = request.POST["username"]
    my_user = User.objects.filter(email=email)
    print(my_user)

    # uid = urlsafe_base64_encode(force_bytes(my_user))
    uid = uuid.uuid4()

    # sav = LoginData.objects.filter(email="email")

    user1 = Forget(email=email, u_no=uid)
    user1.save()
    # print(sav)
    # sav.u_no = uid
    # print(sav)

    # token1 = force_text(generate_token.make_token(my_user))
    # token = uuid.uuid4()

    current_site = get_current_site(request)
    domain = current_site.domain
    # uid = urlsafe_base64_encode(force_bytes(my_user.pk))
    subject = 'Password reset link'
    message = f'Hi follow the link to reset your password http://{domain}/reset/{uid}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    # delay = 300
    # start_time = threading.Timer(delay, delt(uid))
    # start_time.start()
    messages.success(request, "Check your email for reset link")

    return redirect("/")


def reset(request, uidb64):
    try:
        try:
            # uid = force_text(urlsafe_base64_decode(uidb64))
            my_user = Forget.objects.filter(u_no=uidb64).order_by("-id")[0]
            print(my_user)
        except:
            my_user = Forget.objects.filter(u_no=uidb64)


    except (TypeError, ValueError, OverflowError, User.DoesNotExist,):
        my_user = None

    if my_user != None:
        return render(request, 'final.html', context={'user': my_user})
    else:
        print(my_user)
        return redirect('/')


def finalreset(request):
    uid = request.POST["custId"]
    pass1 = request.POST["pass1"]
    pass2 = request.POST["pass2"]
    if pass1 != pass2:
        messages.error(request, "Different Passwords")
        return redirect("/")
    if pass1 == "":
        messages.error(request, "Password cannot be blank")
        return redirect("/")
    if len(pass1) <= 7:
        messages.error(request, "Too short password")
        return redirect("/")

    try:
        email1 = Forget.objects.filter(u_no=uid).order_by("-id")[0]
    except:
        email1 = Forget.objects.filter(u_no=uid)

    email = force_text(email1)
    print(email)

    if pass1 == pass2:
        try:
            u = User.objects.get(email=email)
            u.set_password(pass1)
            u.save()
            messages.success(request, "Password changed successfully. You can login now.")
            Forget.objects.filter(u_no=uid).delete()
        except:
            return redirect("/")

        print(uid)
        return redirect('/')


    else:
        return redirect('/')
