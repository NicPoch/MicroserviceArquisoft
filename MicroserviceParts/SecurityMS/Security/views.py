from django.shortcuts import render
from .logic.logic import createUser,verify
from django.http import JsonResponse,HttpResponse,request
from django.views.decorators.csrf import csrf_exempt
import json

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
        try:
            data = request.body.decode('utf-8')
            requestValues = json.loads(data)
            if(createUser(requestValues)):
                return HttpResponse(status=201)
            else:
                return HttpResponse(status=406)
        except Exception as e:
            print("fuck")
            e.with_traceback()
            return HttpResponse(status=406)        
    else:
        return HttpResponse(status=400)