from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.backends import ModelBackend
from django.views.generic import TemplateView,View
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.http import HttpResponseRedirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


class HomePage(View):
    # template_name = 'registration/login.html'
    def get(self,request,*args,**kwargs):
        return render(request,'registration/login.html')

    def post(self,request,*args,**kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = auth.authenticate(username=email,password=password)

        if user:
            print('in the login')
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,'Login failed')

        return render(request,'registration/login.html')


class Registration(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/signup.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(username,email,password1,password2)
        if password1 and password1 == password2:
            if User.objects.filter(username=username).exists():
                print('user')
                messages.info(request, 'User Already exists')
                return render(request, 'registration/signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already taken')
                return render(request, 'registration/signup.html')
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request, 'Password not matching')
            return render(request, 'registration/signup.html')


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

