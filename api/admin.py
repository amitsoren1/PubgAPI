from django.contrib import admin
from .models import Tournament,Match,Player
# Register your models here.
admin.site.register(Tournament)
admin.site.register(Match)
admin.site.register(Player)