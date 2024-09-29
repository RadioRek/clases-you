from django.contrib import admin
from .models import TipoUsuario, User, Tag, Anuncio, Rating, ChatRoom, ChatMessage, Reserva

admin.site.register(User)
admin.site.register(TipoUsuario)
admin.site.register(Tag)
admin.site.register(Anuncio)
admin.site.register(Rating)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(Reserva)


