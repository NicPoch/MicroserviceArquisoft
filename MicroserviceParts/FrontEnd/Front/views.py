from django.shortcuts import render
from django.http import request
from django.forms import Form

# Create your views here.
def Index(request):
    return render(request,template_name="Front\index.html")

def SignUp(request):
    # Falta poner que Form sea de la forma que pide el microservicio de seguridad.
    form = Form()
    return render(request, 'Front\signup.html', {'form': form})
