from ..models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login


class LoginHandler:
    
    def set_next(self, handler):
        self.next_handler = handler

    def handle(self, request, form, **kwargs):
        if self.next_handler:
            return self.next_handler.handle(request, form, **kwargs)
        return None
    

class FormHandler(LoginHandler):

    def handle(self, request, form, **kwargs):
        if form.is_valid():
            return super().handle(request, form)
        else:    
            return redirect('login')
        

class UserHandler(LoginHandler):

    def handle(self, request, form, **kwargs):
        username = form.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()

        if user is not None:
            return super().handle(request, form, user=user)
        else:
            return redirect('login')
        
        
class BlockedUserHandler(LoginHandler):

    def handle(self, request, form, **kwargs):
        user = kwargs["user"]
        if user.is_blocked:
            return redirect('login')
        else:
            return super().handle(request, form, user = user)
        
        
class AuthHandler(LoginHandler):

    def handle(self, request, form, **kwargs):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        auth_user = authenticate(request, username=username, password=password)
        
        if auth_user is not None:
            login(request, auth_user)
            return super().handle(request, form, user=auth_user)
        else:
            failed_login_handler = FailedLoginHandler()
            self.set_next(failed_login_handler)
            return super().handle(request, form, user=kwargs['user'])
        

class FailedLoginHandler(LoginHandler):
    _attempts_allowed = 5

    def handle(self, request, form, **kwargs):
        user = kwargs['user']
        user.failed_logins += 1

        if user.failed_logins > self._attempts_allowed:
            user.is_blocked = True

        user.save()

        return redirect('login')


class InternalUserHandler(LoginHandler):
    def handle(self, request, form, **kwargs):
        if kwargs['user'].internal_user:
            return redirect(reverse('admin:index'))
        else:
            return redirect('index')

