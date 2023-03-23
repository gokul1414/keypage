from django.shortcuts import render,redirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import content_data
from . import forms
from django.shortcuts import redirect




def handler404(request, exception):
    # response = render_to_response('/not-found')
    response = "not.html"

    response.status_code = 404
    return render(request, response)


def handler500(request, *args, **argv):
    return render(request, 'not.html', status=500)


@login_required(login_url='login')
def home(request):
   
    data = content_data.objects.all()
    context={
        'postleft':data
    }
    return render(request,'Base.html',context)

def page_about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def base_about(request):
    return render(request,'baseabout.html')


def welcome_page(request):
    return render(request,'welcome.html')



def user_register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        my_user=User.objects.create_user(username,email,pass1)
        my_user.save()
        return redirect('home')
        print(username,email,pass1,pass2)
        # auth.login(request,user)
    return render(request,'register.html')
        


def user_login(request):
    
    if request.method == "POST":
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error' : 'Incorrect Details!'})
        # print(username,pass1)
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    response = redirect('home')
    response.delete_cookie('sessionid')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@login_required(login_url='login')
def newpost(request):
    if request.method=='POST':
        form=forms.CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.author=request.user
            instance.save()
            return redirect('home')

    else:
        form=forms.CreatePostForm()
    return render(request,'newpost.html',{'form':form})


    