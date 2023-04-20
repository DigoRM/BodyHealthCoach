from datetime import date
from accounts.models import Aluno

today = date.today()
expired_planos = Aluno.objects.filter(pago=True, vencimento_plano__lte=today)
for aluno in expired_planos:
    aluno.pago = False
    aluno.save()