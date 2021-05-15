from django.shortcuts import render
from .models import Insurance, Policy
from user.models import Transaction
import datetime

#view showing all insurances offered
def insurance(request):

    insurance = Insurance.objects.all()
    return render(request, 'app/insurance.html', {'insurance' : insurance})

"""
cron job view that  which verifies the validity of the policies currently active
every day at 00.00 it check if there are policies that expire on that date
"""
def transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'app/transactions.html', {'transactions': transactions})

def transactionDetail(request, pk):
    transaction = Transaction.objects.get(pk = pk)
    return render(request, 'app/transactionDetail.html', {'transaction': transaction})



def checkPolicyValidity(request):

    now = datetime.date.today()
    activePolicy = Policy.objects.filter(active = True)
    for policy in activePolicy:
        if policy.expiration < now:
            policy.active = False
            policy.save()
    return render(request, 'app/checkPolicyValidity.html', {})