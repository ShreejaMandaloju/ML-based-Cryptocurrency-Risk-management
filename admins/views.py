from admins.models import CurrencyUpdateModel
from users.models import UserBuyingCryptoModel
from django.db.models import Sum
from django.conf import settings
import os
import traceback
import csv

class GetData:
    def __init__(self):
        print("Invoke Once")

    def generateTrading(self):
        print("Trading Started")
        currency_updates = CurrencyUpdateModel.objects.all()
        trading_data = []

        for update in currency_updates:
            data = []
            date = update.changedate.strftime('%Y-%m-%d')
            original_value = update.originalCurrencyValue
            conversion_rate = update.conversionRate
            high = 0.0
            low = 0.0
            open_int = 0

            if conversion_rate > 0:
                high = original_value * conversion_rate
            else:
                low = original_value * abs(conversion_rate)
                open_int = 1

            close = update.newCurrencyValue
            currency_name = update.currencyname
            volume = UserBuyingCryptoModel.objects.filter(currencyname=currency_name).aggregate(Sum('quantity')).get("quantity__sum")
            print('Volume is ', volume)

            data.append(date)
            data.append(original_value)
            data.append(high)
            data.append(low)
            data.append(close)
            data.append(volume)
            data.append(open_int)
            trading_data.append(data)

        file_path = os.path.join(settings.MEDIA_ROOT, "ram.txt")
        return trading_data
'''
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from users.models import BitUserRegisterModel,BlockChainLedger
from agents.models import BitAgentRegisterModel
from .models import cryptcurrencyratemodel,CurrencyUpdateModel
import string
import random
import datetime
from django.db.models import Sum

# Create your views here.

def adminlogincheck(request):
    if request.method=='POST':
        usrid = request.POST.get('adminid')
        pswd  = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'admins/adminhome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'admins.html')

def viewusers(request):
    dict = BitUserRegisterModel.objects.all()
    return render(request, 'admins/userslist.html', {'objects': dict})

def viewagents(request):
    dict = BitAgentRegisterModel.objects.all()
    return render(request,'admins/agentslist.html',{'objects':dict})
def activatewaitedusers(request):
    if request.method=='GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        authkey = genSecretKey(8)
        BitUserRegisterModel.objects.filter(id=id).update(status=status,authkey=authkey)
        registerusers = BitUserRegisterModel.objects.all()
        return render(request, 'admins/userslist.html', {'objects': registerusers})
def activatewaitedagents(request):
    if request.method=='GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        authkey = genSecretKey(8)
        BitAgentRegisterModel.objects.filter(id=id).update(status=status, authkey=authkey)
        registerusers = BitAgentRegisterModel.objects.all()
        return render(request, 'admins/agentslist.html', {'objects': registerusers})

def genSecretKey(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def currentrate(request):
    dict = cryptcurrencyratemodel.objects.all()
    dict2 = CurrencyUpdateModel.objects.all()
    return render(request,'admins/cryptoratecurrent.html',{'objects':dict,'objects1':dict2})

def updatecryptocurrency(request,curr):
    rate = request.GET.get('rate')
    print('Rate = ',type(rate),' Currency ',type(curr))
    incrementRate = float(rate)
    if incrementRate>0:
        check = cryptcurrencyratemodel.objects.get(currencytype=curr)
        currentRate = check.doller
        currentRupee = check.rupee
        originalDollerrate = check.originalprice
        originalRupee = check.originalprice

        newRupee = (incrementRate * currentRupee) / 100
        newCurrencyVal = (incrementRate * currentRate) / 100
        print('Updated Currency ', newCurrencyVal)
        today = datetime.datetime.now()
        print("Today's date:", today)

        # changes = newCurrencyVal - originalDollerrate
        changes = newCurrencyVal + currentRate
        newRup = newRupee + currentRupee
        print("Chnages is ", changes)
        currencygain = ''

        if changes > currentRate:
            currencygain = 'Gain'
        else:
            currencygain = "loss"
        print('Currency is ', currencygain)
        CurrencyUpdateModel.objects.create(currencyname=curr, conversionRate=rate, newCurrencyValue=changes,
                                           originalCurrencyValue=originalDollerrate, chnageValue=changes,
                                           profitorloss=currencygain, changedate=today)
        cryptcurrencyratemodel.objects.filter(currencytype=curr).update(doller=changes, rupee=newRup)

        dict = cryptcurrencyratemodel.objects.all()
        dict2 = CurrencyUpdateModel.objects.all()
        return render(request, 'admins/cryptoratecurrent.html', {'objects': dict, 'objects1': dict2})
    elif incrementRate==0:
        print("Please Check Yhe Conversion rate")
    else:
        print("Currency Decrease Starts")
        check = cryptcurrencyratemodel.objects.get(currencytype=curr)
        currentRate = check.doller
        currentRupee = check.rupee
        originalDollerrate = check.originalprice
        originalRupee = check.originalprice

        newRupee = (abs(incrementRate) * currentRupee) / 100
        newCurrencyVal = (abs(incrementRate) * currentRate) / 100
        print('Updated Currency ', newCurrencyVal)
        today = date.now()
        print("Today's date:", today)

        # changes = newCurrencyVal - originalDollerrate
        changes =currentRate - newCurrencyVal
        newRup = currentRupee - newRupee
        print("Chnages is ", changes)
        currencygain = ''

        if changes > currentRate:
            currencygain = 'gain'
        else:
            currencygain = "loss"
        print('Currency is ', currencygain)
        CurrencyUpdateModel.objects.create(currencyname=curr, conversionRate=rate, newCurrencyValue=changes,
                                           originalCurrencyValue=originalDollerrate, chnageValue=changes,
                                           profitorloss=currencygain, changedate=today)
        cryptcurrencyratemodel.objects.filter(currencytype=curr).update(doller=changes, rupee=newRup)

        dict = cryptcurrencyratemodel.objects.all()
        dict2 = CurrencyUpdateModel.objects.all()
        return render(request, 'admins/cryptoratecurrent.html', {'objects': dict, 'objects1': dict2})



def AdminGetLedger(request):
    check = BlockChainLedger.objects.aggregate(Sum('blockchainmoney'))
    x = check.get("blockchainmoney__sum")
    x = round(x, 2)
    print('Totoal Ledger Sum ', x)
    dict = BlockChainLedger.objects.all()
    return render(request, 'admins/adminsblock.html', {'objects': dict, 'ledger': x})'
'''