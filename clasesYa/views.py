from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
import calendar
from datetime import datetime
import locale
from django.utils import timezone
from django.contrib import messages
from .models import TipoUsuario, Anuncio

User = get_user_model()

@login_required
def videollamada(request):
    return render(request, "videollamada.html", { 'name': request.user.email })

@login_required
def home(request):
    #Carga del usuario
    user = request.user

    #Carga del calendario
    cal, month, year, month_name = cargarCalendario()


    #Carga de usuarios y chats   
    #Funcion para la creacion de un anuncio
    if request.method == "POST":
        if 'anuncioForm' in request.POST:
            if registrarAnuncio(request, user):
                return render(request, 'home.html', {
                    'user': user, 
                    'calendar': cal, 
                    'month': month, 
                    'year': year, 
                    'monthName': month_name, 
                })
            else:
                return render(request, 'home.html', {
                    'user': user, 
                    'calendar': cal, 
                    'month': month, 
                    'year': year, 
                    'monthName': month_name, 
                })
        elif 'updateAnuncio' in request.POST:
            user = request.user
            anuncio_id = request.POST.get('updateAnuncio')
            campo = request.POST.get('inputCampo')
            return render(request, 'home.html', {
                'user': user, 
                'calendar': cal, 
                'month': month, 
                'year': year, 
                'monthName': month_name, 
            })  
        elif 'entrarVideo' in request.POST:
            inputUrl = request.POST['inputUrl']
            return redirect("/videollamada?roomID=" + inputUrl)
        if 'reservarClase' in request.POST:
            anuncioId = request.POST.get('anuncio')
            alumnoId = request.POST.get('idAlumno')
            alumno = User.objects.get(id=alumnoId)
            profesorId = User.objects.get(anuncio=anuncioId)
            return render(request, 'home.html', {
                'user': user, 
                'calendar': cal, 
                'month': month, 
                'year': year, 
                'monthName': month_name, 
            })           
        else:
            return render(request, 'home.html', {
                'user': user, 
                'calendar': cal, 
                'month': month, 
                'year': year, 
                'monthName': month_name, 
            })
    else:
        return render(request, 'home.html', {
            'user': user, 
            'calendar': cal, 
            'month': month, 
            'year': year, 
            'monthName': month_name, 
        })


def test(request):
    return render(request, "test.html")

def logoutUser(request):
    logout(request)
    return redirect('login')

def cargarCalendario():
    today = datetime.today()
    month = today.month
    year = today.year

    #nombre del mes en español
    locale.setlocale(locale.LC_TIME, 'es_ES.utf8')
    month_name = calendar.month_name[month]

    cal = calendar.monthcalendar(year, month)
    return cal, month, year, month_name

def registrarAnuncio(request, user):
    titulo = request.POST.get('inputTitulo')
    subTitulo = request.POST.get('inputSubTitulo')
    descripcion = request.POST.get('inputDescripcion')
    precio = request.POST.get('inputPrecio')
    campo = request.POST.get('inputCampo')
    campoReview = Campo.objects.filter(nombre=campo)
    if len(campoReview) == 0:
        nuevoCampo = Campo(nombre=campo)
        nuevoCampo.save()
        campo = nuevoCampo
    else:
        campo = campoReview[0]            
    anuncio = Anuncio(titulo=titulo, subTitulo=subTitulo, descripcion=descripcion, precio=precio, campo=campo)
    try:
        anuncio.save()
        user.anuncio = anuncio
        user.save()
        return True
    except:
        return False

def get_messages(request, room_id):
    messages = ChatMessage.objects.filter(idChatRoom=room_id).select_related('idUser')
    messages_list = []
    for msg in messages:
        formatted_time = timezone.localtime(msg.timestamp).strftime('%H:%M')
        message_dict = {'id': msg.id, 'idChatRoom': msg.idChatRoom.id, 'idUser': msg.idUser.email, 'message': msg.message, 'timestamp': formatted_time}
        messages_list.append(message_dict)
    return JsonResponse(messages_list, safe=False)


# Testing
def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def anuncio_list(request):
    anuncios = Anuncio.objects.all()
    return render(request, 'anuncio_list.html', {'anuncios': anuncios})

# remake
def registro(request):
    if request.method == 'POST':
        if registrarUsuario(request):
            return redirect('login')
        else:
            return redirect('registro')
    else:
        return render(request, "registro.html")

def registrarUsuario(request):
    correo = request.POST.get('inputEmail')
    password = request.POST.get('inputPassword')
    tipo = request.POST.get('selectTipoUsuario')
    tipoUsuario = TipoUsuario.objects.get(id=tipo)
    nombre = ""
    apellido = ""
    rut = ""
    dv = ""
    telefono = ""
    validacionUser = User.objects.filter(correo=correo)
    if len(validacionUser) > 0:
        messages.error(request, 'Correo ya registrado!')
        return False
    if correo == "" or password == "":
        messages.error(request, 'Correo y contraseña son obligatorios!')
        return False
    usuario = User(correo=correo, nombre=nombre, apellido=apellido, rut=rut, dv=dv, telefono=telefono, tipo=tipoUsuario)
    usuario.set_password(password)
    usuario.save()
    messages.success(request, 'Registro exitoso! ahora puedes iniciar sesion')       
    return True

def loginWebsite(request):
    if request.method == 'POST':
        if loginUsuario(request):
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, "login.html")

def loginUsuario(request):
    correo = request.POST.get('inputEmail')
    password = request.POST.get('inputPassword')
    user = authenticate(request, correo=correo, password=password)
    if user is not None:     
        login(request, user)
        return True
    else:
        user = User.objects.filter(correo=correo)
        if len(user) == 0:
            messages.error(request, 'Usuario no existe!')
            return False
        else:
            messages.error(request, 'Contraseña incorrecta!')
            return False

def homeBetter(request):
    user = request.user
    anuncio = Anuncio.objects.filter(usuario=user).first()
    if request.method == "POST":
        if 'actualizarPerfil' in request.POST:
            actualizarUsuario(request)
            return render(request, "homeBetter.html", { 'user': user, 'anuncio': anuncio })
        if 'crearAnuncio' in request.POST:
            crearAnuncio(request)
            return render(request, "homeBetter.html", { 'user': user, 'anuncio': anuncio })
    else:    
        return render(request, "homeBetter.html", { 'user': user, 'anuncio': anuncio })

def actualizarUsuario(request):
    user = request.user
    nombre = request.POST.get('inputNombre')
    apellido = request.POST.get('inputApellido')
    correo = request.POST.get('inputEmail')
    rut = request.POST.get('inputRut')
    dv = request.POST.get('inputDv')
    telefono = request.POST.get('inputTelefono')
    inputPassword = request.POST.get('inputPass')
    if not all([nombre, apellido, correo, rut, dv, telefono]):        
        messages.error(request, 'Todos los campos son obligatorios!')
        return False
    else:
        # validacion correo
        validacionCorreo = User.objects.filter(correo=correo)
        if len(validacionCorreo) > 0 and validacionCorreo[0].id != user.id:
            messages.error(request, 'Correo ya registrado!')
            return False
        # validacion nombre contiene numeros
        elif any(char.isdigit() for char in nombre):
            messages.error(request, 'Nombre no puede contener numeros!')
            return False
        # validacion apellido contiene numeros
        elif any(char.isdigit() for char in apellido):
            messages.error(request, 'Apellido no puede contener numeros!')
            return False
        # validacion rut
        elif not rut.isdigit():
            messages.error(request, 'Rut debe ser numerico!')
            return False
        # validacion dv numero o k
        elif dv != 'k' and not dv.isdigit():
            messages.error(request, 'Dv debe ser numerico o k!')
            return False
        # validacion telefono
        elif not telefono.isdigit():
            messages.error(request, 'Telefono debe ser numerico!')
            return False
        # validacion password para confirmar cambios
        elif not user.check_password(inputPassword):
            messages.error(request, 'Contraseña incorrecta!')
            return False
        else:
            user.nombre = nombre
            user.apellido = apellido
            user.correo = correo
            user.rut = rut
            user.dv = dv
            user.telefono = telefono
            user.save()
            messages.success(request, 'Cambios guardados exitosamente!')
            return True


def crearAnuncio(request):
    # metodo para agregar los tags pendiente
    user = request.user
    titulo = request.POST.get('inputTitulo')
    subtitulo = request.POST.get('inputSubtitulo')
    descripcion = request.POST.get('inputDescripcion')
    precio = request.POST.get('inputPrecio')
    
    if not all([titulo, descripcion, precio]):
        messages.error(request, 'Todos los campos son obligatorios!')
        return False
    else:
        anuncio = Anuncio(titulo=titulo, subtitulo=subtitulo, descripcion=descripcion, precio=precio, usuario=user)
        anuncio.save()
        messages.success(request, 'Anuncio creado exitosamente!')
        return True
    
    
