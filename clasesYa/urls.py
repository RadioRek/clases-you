from django.urls import path
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    path("", views.loginUser),
    path("login/", views.loginUser, name='login'), 
    path("logout/", views.logoutUser, name='logout'),
    path("home/", views.home, name='home'),
    path("registro/", views.registro, name='registro'),
    path("test/", views.test),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    path('videollamada/', views.videollamada, name='videollamada'),
    # Testing
    path('anuncios/', views.anuncio_list, name='anuncio_list'),
]
