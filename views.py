from django.shortcuts import render
from django.utils.timezone import now
from .models import Servico
from django.db.models import Sum
from collections import defaultdict

def dashboard(request):
    hoje = now()

    servicos = Servico.objects.all()

    servicos_mes = servicos.filter(
        data__month=hoje.month,
        data__year=hoje.year
    )

    faturamento = servicos_mes.filter(status='pago').aggregate(
        total=Sum('valor')
    )['total'] or 0

    total_servicos = servicos_mes.count()
    pendentes = servicos_mes.filter(status='pendente').count()

    # gráfico
    dados = defaultdict(float)

    for s in servicos_mes:
        if s.status == 'pago':
            dados[s.data.day] += float(s.valor)

    dias = list(dados.keys())
    valores = list(dados.values())

    recentes = servicos.order_by('-data')[:5]

    return render(request, 'dashboard.html', {
        'faturamento': faturamento,
        'total_servicos': total_servicos,
        'pendentes': pendentes,
        'dias': dias,
        'valores': valores,
        'recentes': recentes
    })