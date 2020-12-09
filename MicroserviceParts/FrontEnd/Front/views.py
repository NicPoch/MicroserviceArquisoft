from django.shortcuts import render
from django.http import request
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import Form

# Create your views here.
def Index(request):
    return render(request,template_name="Front\index.html")

def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            user.last_login=datetime.datetime.now()
            user.email=form.data['email']
            user.first_name=form.data['first_name']
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            u=Usuario(password=raw_password,last_login=user.last_login,first_name=user.first_name,email=user.email,username=user.username,id=user.pk)
            u.save()
            return redirect('profile',id=u.id)
        else:
            form = Form()
            return render(request, 'Front\signup.html', {'form': form})
    else:
        form = Form()
        return render(request, 'Front\signup.html', {'form': form})

def LogIn(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print(form.__dict__)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile',id=user.id)
        else:
            form = AuthenticationForm()
            return render(request, 'Front\login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'Front\login.html', {'form': form})
