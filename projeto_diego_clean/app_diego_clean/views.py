from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.contrib.auth.models import User



def login(request):
    if request.method =="GET":
        return render(request, "login.html")
    else:
        username=request.POST.get('username')
        senha=request.POST.get('senha')
        
        user=authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username ou senha invalidos')
            return render(request, 'login.html')
        
def cadastro(request):
    if request.method=='GET':
        return render(request, "cadastro.html")
    else:
        email=request.POST.get('email')
        username=request.POST.get('username')
        senha=request.POST.get('senha')
        confirmar_senha=request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem!")
            return render(request, "cadastro.html")
        
        if User.objects.filter(username=username).first():
            messages.error(request,'Já existe um usuário com esse username')
            return render(request, "cadastro.html")
        user=User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return redirect('login')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro_view(request):
    return redirect('cadastro')