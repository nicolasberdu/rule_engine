from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from .form import CustomAuthenticationForm


class Index(TemplateView):
    template_name = 'index.html'

class Login(View):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class() 
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            

        return render(request, self.template_name, {'form': form})
    

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')