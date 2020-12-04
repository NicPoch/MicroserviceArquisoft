from django.shortcuts import render
from .logic.logic import createUser,verify
from django.http import JsonResponse,HttpResponse,request
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def incomingVerification(request):
    if request.method=='GET':
        requestValues=dict(request.GET.values('username','password'))
        data=verify(requestValues['username'],requestValues['password'])
        if(data==None):
            return HttpResponse(status=406)
        else:
            return JsonResponse(data=data,safe=True,status=201)
    else:
        return HttpResponse(status=400)
@csrf_exempt
def createAuthUser(request):
    if request.method=='POST':
        requestValues=dict(request.GET.values('username','password'))
        if(createUser(requestValues['username'],requestValues['password'],requestValues['rol'])):
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=406)
    else:
        return HttpResponse(status=400)