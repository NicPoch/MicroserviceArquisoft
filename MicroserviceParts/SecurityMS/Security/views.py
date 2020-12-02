from django.shortcuts import render
from .logic.logic import createUser,verify
from django.http import JsonResponse,HttpResponse,request,Http404, HttpResponseNotFound
# Create your views here.

def incomingVerification(request):
    if request.method=='GET':
        requestValues=dict(request.GET.values('username','password'))
        data=verify(requestValues['username'],requestValues['password'])
        if(data==None):
            return HttpResponseNotFound()
        else:
            return JsonResponse(data=data,safe=True)
    else:
        return Http404()

def createAuthUser(request):
    if request.method=='POST':
        return HttpResponse(status=201)
    else:
        return Http404()