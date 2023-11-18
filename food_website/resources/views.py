from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def home_page(request,*args,**kwargs):

    queryset = Resources.objects.all()
    context = {'recipes': queryset}

    return render(request,"index.html", context)


def delete_recipe(request, id):

    id_recipe = Resources.objects.get(id = id)
    id_recipe.delete()

    return redirect("/")

@login_required(login_url='/login/')
def addrecipe_page(request, *args, **kwargs):

    if request.method == "POST":

        data = request.POST
        image = request.FILES

        user           = request.user
        resource_name  = data.get('resource_name')
        description    = data.get('description')
        price          = data.get('price')
        resource_image = image.get('resource_image')

        Resources.objects.create(
            user = user,
            resource_name = resource_name ,
            description = description,
            price = price,
            resource_image = resource_image
        )

        return redirect('/add_recipe/')

    return render(request,"Add_recipe.html", {})

@login_required(login_url='/login/')
def search_page(request,*args,**kwargs):

    query = request.GET['search']
    search_results = Resources.objects.filter(resource_name__icontains=query)
    context = {'search_results': search_results}

    return render(request,"search.html", context )


def login_page(request,*args,**kwargs):

    if request.method == "POST":

        data = request.POST

        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username= username).exists():

            messages.error(request, "User does not exist.")
            return redirect("/login/")

        user = authenticate(username= username, password= password)

        if user is None:

            messages.error(request, "Invalid password")
            return redirect("/login/")

        else:

            login(request, user)

            return redirect("/")



    return render(request,"login.html", {})


def register_page(request):

    if request.method == "POST":

        data = request.POST

        f_name = data.get('first_name')
        l_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        user = User.objects.filter(username= username)

        if user.exists():

            messages.error(request, "Invalid username.")

            return redirect("/registration/")


        user = User.objects.create(
            first_name = f_name,
            last_name= l_name,
            email = email,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.info(request, "User successfully created.")

        return redirect("/registration/")

    return render(request,"register.html", {})


def logout_page(request,*args,**kwargs):

    logout(request)

    return redirect("/login/")