from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.views.generic import TemplateView, View, ListView, CreateView, DetailView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import transaction
from .form import CustomAuthenticationForm, UserForm, SetPasswordForm
from .handlers.login_handlers import FormHandler, UserHandler, BlockedUserHandler, AuthHandler, InternalUserHandler
from .models import User, ActivationLink


class Index(TemplateView):
    template_name = 'index.html'

class Login(View):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        
        form = self.form_class() 
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        form_handler = FormHandler()
        user_handler = UserHandler()
        blocked_user_handler = BlockedUserHandler()
        auth_handler = AuthHandler()
        internal_user_handler = InternalUserHandler()

        form_handler.set_next(user_handler)        
        user_handler.set_next(blocked_user_handler)
        blocked_user_handler.set_next(auth_handler)
        auth_handler.set_next(internal_user_handler)
        
        result = form_handler.handle(request, form)
        if result:
            return result

"""         
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                return redirect('index')
            

        return render(request, self.template_name, {'form': form})
     """

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    

class UserList(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'

class UserDetail(DetailView):
    model = User
    template_name = 'user/user_detail.html'  
    context_object_name = 'user'

class UserCreate(CreateView):
    model = User
    form_class = UserForm  
    template_name = 'user/user_form.html'  
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        activation_link = ActivationLink.generate_new_link(self.object)

        return response

class UserDelete(DeleteView):
    model = User
    template_name = 'user/user_delete.html'
    success_url = reverse_lazy('user_list')

class UserActivation(View):
    model = User
    template_name = 'user/user_active.html'

    form_class = SetPasswordForm


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        
        key = ActivationLink.objects.filter(key=kwargs.get('key')).first()
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'username': key.user})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        key = ActivationLink.objects.filter(key=kwargs.get('key')).first()
        user = key.user

        if form.is_valid():
            password = form.cleaned_data['password']

            try:
                with transaction.atomic():
                    user.password=make_password(password)
                    user.is_active=True
                    user.save()

                    key.delete()

                    return redirect('login')
            
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'username': user})
        else:
            return render(request, self.template_name, {'form': form, 'username': user})
        