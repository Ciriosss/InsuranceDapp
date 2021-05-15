from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
from app.models import Insurance , Policy
from django.contrib import messages
from datetime import datetime, timedelta
from .blockchainConnection import buyToken,newAccount, getTokenBalance, transaction, getEthBalance, buyPolicy, supply
from .models import Profile, Transaction
from .forms import SetUpAccount,BuyToken
from django.db.models import Q


# user registration view

def register( request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Congratulations {}! your account has been created successfully, now you are able to log-in'.format(username))
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


# personal page of user

def profile(request):

    profile = Profile.objects.get(username = request.user)
    balanceHMS = 0
    userPolicies = []
    balanceEth = 0
    l = 0

    #check if the user has set up an ethereum account
    if profile.address:
        balanceHMS = getTokenBalance(profile)
        #filtering the user policies & transactions
        userPolicies = Policy.objects.filter(insured = profile)
        balanceEth = getEthBalance(profile.address)
        l = len(userPolicies)

    return render(request, 'user/profile.html', {'profile':profile,'balanceHMS':balanceHMS,'balanceEth':balanceEth, 'userPolicies': userPolicies, 'l' :l})


def insuranceDetail(request, pk):
    policy = get_object_or_404(Insurance, pk=pk)
    return render(request, 'user/policyDetail.html', {'policy' : policy})


#view that confirm purchase of the insurance policy,the policy is inserted in the "Policy" model

def orderCompleted(request, pk):

    profile = request.user
    policy = Insurance.objects.get(pk=pk)
    _from = profile.address
    _value = policy.price

    try:
        # function that connects with the smart contract to make the token transaction
        buyPolicy(_from, _value)

        #obtaining the expiry date of the policy
        duration = timedelta(days=policy.duration)
        date = datetime.today()
        expiration = date + duration

        newPolicy = Policy.objects.create(insured=profile, policy=policy)
        newPolicy.expiration = expiration
        newPolicy.save()

    except:

        messages.warning(request,'Something went wrong, check your balance')
        return redirect('profile')

    return render(request, 'user/orderCompleted.html', {'expiration' : expiration})


#view where users can import them ethereum account

def setUpAccount(request):

    if request.method == 'POST':
        form = SetUpAccount(request.POST)

        if form.is_valid():
            profile = request.user
            privateKey = form.cleaned_data.get('privateKey')

            try:
                newAccount(profile,privateKey)
            except:
                messages.warning(request, 'Not valid Private Key, try again')
                return redirect('profile')

            return redirect('profile')
    else:
        form = SetUpAccount()
    return render(request, 'user/setUpAccount.html', {"form" : form})


#view related to the token some information related to it

def token(request):
    if request.method == 'POST':

        #form to insert eth to convert in token
        form = BuyToken(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            profile = request.user
            try:
                tx = transaction(profile, amount)
                _value = amount * 100
                address = profile.address
                buyToken(_to = address, _value=_value)
                Transaction.objects.create(addressFrom = profile.address, addressTo = "0x0f60aeD92A41eA3aEc0354fB2668C38A02b7Fa2e",amount = amount, tx = tx)
                return redirect('profile')
            except:
                messages.warning(request,'Something went wrong, check your balance')
                return redirect('profile')
    else:
        form = BuyToken()

    tokenSupply = supply()
    return render(request, 'user/token.html', {'form' : form, 'tokenSupply' : tokenSupply})