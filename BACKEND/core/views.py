from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm,ProfileForm
from django.contrib.auth import authenticate,login

# Create your views here.
def home(request):
    return render(request,'core/home.html')

@login_required
def services(request):
    return render(request,'core/services.html')

@require_POST
def exit(request):
    logout(request)
    return redirect('home')

@login_required
def config(request):
    if not request.user.groups.filter(name="gestor").exists():
        return redirect('home')
    return render(request,'core/config.html')

def register(request):
    data={
        'user_form':CustomUserCreationForm,
        'profile_form':ProfileForm
    }

    if request.method=='POST':
        user_creation_form=CustomUserCreationForm(data=request.POST)
        profile_creation=ProfileForm(request.POST,request.FILES)
        if user_creation_form.is_valid() and profile_creation.is_valid():
            user=user_creation_form.save()
            profile=profile_creation.save(commit=False)
            profile.id=user.profile.id
            profile.user=user
            profile.save()
            user=authenticate(username=user_creation_form.cleaned_data["username"],password=user_creation_form.cleaned_data["password1"])
            login(request,user)
            return redirect('home')
        else:
            return render(request,'registration/register.html',{
                    'user_form':user_creation_form,
                    'profile_form':profile_creation
                })
    return render(request,'registration/register.html',data)