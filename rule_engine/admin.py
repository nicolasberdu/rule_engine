from django.contrib import admin

from .models import User, ActivationLink, Rule

admin.site.register(User)
admin.site.register(ActivationLink)
admin.site.register(Rule)
