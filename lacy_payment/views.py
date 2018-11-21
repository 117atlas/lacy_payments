import json
import urllib
import urllib.request as urllib2

from django.http import HttpResponse
from django.shortcuts import render, redirect
from pip.utils import logging

from .forms import CustomerForm

# Create your views here.
def pay(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return render(request, 'lacy_payment/page.html', locals())

def payViaMomo(request):
    #form = CustomerForm(request.POST or None)

    #if form.is_valid():
        #_name = form.cleaned_data['name']
        #_phone = form.cleaned_data['phone']
        #print(form.cleaned_data)
        #data = urllib.parse.urlencode({"service": "Je0J3wOesnqdkuRx4lIpBYipc1mkObGH", "phonenumber": "+237"+_phone, "amount": 500, "first_name": _name}).encode("utf-8")
        #_headers = {'Content-Type': 'application/json'}
        #req = urllib2.Request("https://api.monetbil.com/payment/v1/placePayment", data=data, headers=_headers);
        #res = urllib2.urlopen(req);
        #res_json = json.loads(res.read());

        #sres = json.dump(res_json, 2)
        #return render(request, 'lacy_payment/payment_accepted.html', sres);

    jdata = {"amount": 500, "currency":"XAF", "item_ref":"Item_bought",
             "payment_ref":"ref_payment_in_our_server", "first_name":"Samaritain", "last_name":"Sims",
             "return_url":"http://127.0.0.1/lacy/momopaymentsuccess",
             "notify_url":"http://127.0.0.1/lacy/feedbackmomo"}

    data = urllib.parse.urlencode(jdata).encode("utf-8");
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request("https://api.monetbil.com/widget/2.1/Je0J3wOesnqdkuRx4lIpBYipc1mkObGH", data=data, headers=headers);
    res = urllib2.urlopen(req)
    res_json = json.loads(res.read());

    if (res_json is None):
        return HttpResponse("""
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Error</title>
                </head>
                <body>
                    <pre> Res null </pre>
                </body>
            <html>
        """ % json.dump(res_json, 2))
    else:
        if 'payment_url' not in res_json:
            return HttpResponse("""
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Error - Payment url not sent</title>
                </head>
                <body>
                    <pre> %s </pre>
                </body>
            <html>
            """)
        else:
            return redirect(res_json['payment_url'])

    #return render(request, 'lacy_payment/page.html', locals())

def checkMoMoPaymentStatus(request, paymentId):
    data = urllib.urlencode({"paymentId": paymentId})
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request("POST https://api.monetbil.com/payment/v1/placePayment", data=data, headers=headers);
    res = json.loads(req.read());

    sres = json.dump(res, 2)
    return render(request, 'lacy_payment/see_momo_payment.html', sres);

def payViaCrypto(request):
    return render(request, 'lacy_payment/page.html', locals())