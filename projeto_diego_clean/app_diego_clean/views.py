from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Servico, Cliente
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    servicos = Servico.objects.all().order_by('-data')
    total_servicos = servicos.count()
    faturamento = sum(s.valor for s in servicos)
    pendentes = servicos.filter(status="Pendente").count()
    faturamento_por_dia = {}
    for s in servicos:
        dia = s.data.strftime('%d/%m')
        if dia not in faturamento_por_dia:
            faturamento_por_dia[dia] = 0
        faturamento_por_dia[dia] += s.valor
    dias = list(faturamento_por_dia.keys())
    valores = list(faturamento_por_dia.values())
    recentes = servicos[:5]
    return render(request, 'dashboard.html', {
        'servicos': servicos,
        'total_servicos': total_servicos,
        'faturamento': faturamento,
        'pendentes': pendentes,
        'dias': dias,
        'valores': valores,
        'recentes': recentes,
    })
    

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
    if request.method == 'GET':
        return render(request, "cadastro.html")
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem!")
            return render(request, "cadastro.html")
        if User.objects.filter(username=username).first():
            messages.error(request, 'Já existe um usuário com esse username')
            return render(request, "cadastro.html")
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )
        user.save()
        return redirect('login')
    
def logout_view(request):
    logout(request)
    return redirect('login')

def cadastro_view(request):
    return redirect('cadastro')

def adicionar_servico(request):
    print("METHOD:", request.method)
    if request.method == "POST":
        print("POST:", request.POST)
        cliente_nome = request.POST.get("cliente")
        valor = request.POST.get("valor")
        status = request.POST.get("status")
        if not cliente_nome or not valor:
            return JsonResponse({'mensagem': 'Dados inválidos'})
        cliente, _ = Cliente.objects.get_or_create(nome=cliente_nome)
        Servico.objects.create(
            cliente=cliente,
            valor=float(valor),
            status=status,
            usuario=request.user,
        )
        return JsonResponse({'mensagem': 'Serviço adicionado com sucesso!'})
    return JsonResponse({'mensagem': 'Erro'})

def editar_servico(request):
    if request.method == "POST":
        servico_id = request.POST.get("id")
        valor = request.POST.get("valor")
        status = request.POST.get("status")
        servico = get_object_or_404(Servico, id=servico_id)
        if servico.usuario != request.user:
            return JsonResponse({'mensagem': 'Sem permissão'})
        servico.valor = float(valor)
        servico.status = status
        servico.save()
        return JsonResponse({'mensagem': 'Serviço atualizado com sucesso!'})
    return JsonResponse({'mensagem': 'Erro'})

def remover_servico(request):
    if request.method == "POST":
        servico_id = request.POST.get("id")
        if not servico_id:
            return JsonResponse({'mensagem': 'ID inválido'})
        servico = get_object_or_404(Servico, id=servico_id)
        if servico.usuario != request.user:
            return JsonResponse({'mensagem': 'Sem permissão'})
        servico.delete()
        return JsonResponse({'mensagem': 'Serviço removido com sucesso!'})
    return JsonResponse({'mensagem': 'Erro'})