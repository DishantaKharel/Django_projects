from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

@login_required(login_url="/login/")
def home_page(request,*args,**kwargs):

    profile_detail = UserProfile.objects.all()
    content = UserPost.objects.all()
    context = {
        'userprofiles': profile_detail,
        'userposts': content
    }

    return render(request,"index.html", context)

@login_required(login_url="/login/")
def register_userprofile(request,*args,**kwargs):

    if UserProfile.objects.filter(user=request.user).exists():

        return redirect('/')

    if request.method == "POST":

        data  = request.POST
        image = request.FILES

        user        = request.user
        profile_pic = image.get('profile_pic')
        bio         = data.get('bio')

        UserProfile.objects.create(
            user= user,
            profile_pic= profile_pic,
            bio= bio
        )

        return redirect('/profile/')

    return render(request,"registeruser.html",{})


@login_required(login_url="/login/")
def user_profile(request,*args,**kwargs):

    userprofile = UserProfile.objects.filter(user= request.user)

    if not userprofile.exists():

        return redirect('/')

    if request.method == "POST":

        data = request.POST
        image = request.FILES

        status = data.get('status', None)
        photo = image.get('photo', None)

        if status is None and photo is None:
            return redirect('/profile/')

        else:

            UserPost.objects.create(
                user= request.user,
                feed_photo= photo,
                status= status,
            )

            return redirect('/profile/')

    userpost= UserPost.objects.filter(user= request.user)

    context={
        'userprofiles' : userprofile,
        'userposts': userpost
    }

    return render(request,"userprofile.html", context)



@login_required(login_url="/login/")
def search_result(request,*args,**kwargs):

    searched = request.GET['search']

    profile_detail = UserProfile.objects.filter(    Q(user__first_name__icontains=searched) |
                                                    Q(user__last_name__icontains=searched) |
                                                    Q(user__username__icontains=searched)     )

    content = UserPost.objects.filter(              Q(user__first_name__icontains=searched) |
                                                    Q(user__last_name__icontains=searched) |
                                                    Q(user__username__icontains=searched)     )

    print(profile_detail)
    print(content)

    context = {
        'userprofiles': profile_detail,
        'userposts': content
    }

    return render(request,"search.html", context)



@login_required(login_url="/login/")
def delete_post(request,id):

    id_post= UserPost.objects.get(id=id)
    id_post.delete()

    return redirect("/")



def login_register_page(request,*args,**kwargs):

    if request.method == "POST":

        data = request.POST

        login_username = data.get('login_username', None)
        login_password = data.get('login_password', None)

        if login_username is not None and login_password is not None:


            if not User.objects.filter(username=login_username).exists():

                messages.error(request, "User does not exist.")
                return redirect("/login/")

            user = authenticate(username=login_username, password=login_password)

            if user is None:

                messages.error(request, "Invalid password")
                return redirect("/login/")

            else:

                login(request, user)
                return redirect("/create_user/")


        else:

            f_name = data.get('f_name')
            l_name = data.get('l_name')
            signup_username = data.get('signup_username')
            signup_password = data.get('signup_password')
            email = data.get('email')

            user = User.objects.filter(username=signup_username)

            if user.exists():
                messages.error(request, "Invalid username.")
                return redirect("/login/")

            user = User.objects.create(
                first_name=f_name,
                last_name=l_name,
                email=email,
                username=signup_username
            )

            user.set_password(signup_password)
            user.save()


            return redirect("/login/")


    return render(request,"login.html", {})


@login_required(login_url="/login/")
def logout_page(request,*args,**kwargs):

    logout(request)

    return redirect("/login/")


