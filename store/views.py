from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm
from django.db.models.query import QuerySet
from django.views import generic

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('home')
        else:
            messages.info(request, f"Error! Incorrect Username or Password! Please Try Again!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home')

# def register_user(request):

#     return render(request, 'register.html', {})

def register_user(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # messages.info(request, f"Account created for {username}! You are now logged in.")
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/register')
    else:
        form = SignUpForm()
        # messages.error(request, "Please correct the error below.")
        return render(request, 'register.html', { 'form': form })
    

def product(request,pk):
    product = Product.objects.get(id=pk)
    print('message', product)
    return render(request, 'product.html', {'product': product})

# class DetailView(generic.DetailView):
#     # product = Product.objects.get(id=pk)
#     model = Product
#     template_name = 'product.html/'

#     def get_queryset(self):
#     # context_object_name = 'product'
#         return Question.objects.filter('product.html')


def category(request,string):
    string = string.replace('-', ' ')
    try:
        cat = Category.objects.get(name=string)
        products = Product.objects.filter(category=cat)
        return render(request,'category.html', {'category': cat, 'products' : products })

    except:
        messages.success(request, ("Not Available!"))
        return redirect('home')

def update_user(request):
    if request.method=='GET':
        return render (request, 'update_user.html', {'user_form': user_form})
    elif request.method=='POST':
        if request.user.is_authenticated:
            current_user = User.objects.get(id=request.user.id)
            user_form = UpdateUserForm(request.POST, instance=current_user)
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, 'Profile Updated Successfully')
                return redirect('home')
            return render (request, 'update_user.html', {'user_form': user_form})
        else:
            messages.success(request, 'You must be logged in!')
            return redirect('home')


