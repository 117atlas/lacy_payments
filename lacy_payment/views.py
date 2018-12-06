import json
import urllib
import urllib.request as urllib2

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
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



    """
        jdata = {"amount": 500, "currency":"XAF", "item_ref":"Item_bought",
             "payment_ref":"ref_payment_in_our_server", "first_name":"Samaritain", "last_name":"Sims",
             "return_url":"http://127.0.0.1/lacy/momopaymentsuccess",
             "notify_url":"http://127.0.0.1/lacy/feedbackmomo"}
        urlbase = "https://api.monetbil.com/widget/v2.1/Je0J3wOesnqdkuRx4lIpBYipc1mkObGH"

        data = urllib.parse.urlencode(jdata)#.encode("utf-8");
        print(urlbase + data);
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req = urllib2.Request(urlbase, jdata, headers=headers);
        res = urllib2.urlopen(req)
        res_json = json.loads(res.read());
    """

    url = "https://api.monetbil.com/widget/v2.1/Je0J3wOesnqdkuRx4lIpBYipc1mkObGH"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {"amount": "500", "currency": "XAF",
            "item_ref": "Item_bought", "locale": "fr", "country": "CM",
            "payment_ref": "ref_payment_in_our_server", "first_name": "Samaritain", "last_name": "Sims", "phone" : "697266488", "email" : "s@s.s",
            "return_url": "http://127.0.0.1/lacy/momopaymentsuccess",
            "notify_url": "http://127.0.0.1/lacy/feedbackmomo"}
    res = requests.post(url, headers=headers, data=urllib.parse.urlencode(data))
    res_json = res.json()
    print(res_json)

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

def payViaPayPal(request):
    # What you want the button to do.
    paypal_dict = {
        "business": "sfaysamaritan@gmail.com",
        "amount": "100.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('paypal_success')),
        "cancel_return": request.build_absolute_uri(reverse('paypal_error')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "lacy_payment/paypal_payment.html", context)

@csrf_exempt
def paypalReturnSuccess(request):
    return render(request, "lacy_payment/paypal_success.html", locals())

@csrf_exempt
def paypalReturnError(request):
    return render(request, "lacy_payment/paypal_error.html", locals())