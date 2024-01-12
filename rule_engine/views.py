from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from .form import CustomAuthenticationForm
from .handlers.login_handlers import FormHandler, UserHandler, BlockedUserHandler, AuthHandler, InternalUserHandler


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