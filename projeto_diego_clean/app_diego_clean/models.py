from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.cliente.nome} - {self.valor}"
