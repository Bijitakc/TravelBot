from django.contrib import admin
from .models import Place, BotMessage,BotReply

# Register your models here.
admin.site.register(Place)
admin.site.register(BotMessage)
admin.site.register(BotReply)