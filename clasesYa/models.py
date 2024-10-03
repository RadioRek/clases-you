from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

class CustomUserManager(UserManager):
    def _create_user(self, correo, password, **extra_fields):
        if not correo:
            raise ValueError('Ingresa un correo!')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_user(self, correo = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(correo, password, **extra_fields)
    
    def create_superuser(self, correo = None, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)  
        return self._create_user(correo, password, **extra_fields)  
    
class TipoUsuario(models.Model):
    opciones = [('1', 'Profesor'), ('2', 'Alumno')]
    nombreTipo = models.CharField(max_length = 20, blank=True, default='', choices=opciones)
    
    class Meta:
        verbose_name = 'Tipo de usuario'
        verbose_name_plural = 'Tipos de usuarios'
        
    def __str__(self):
        return self.get_nombreTipo_display()
    
class User(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(blank = True, default='', unique=True)
    nombre = models.CharField(max_length = 70, blank=True, default='')
    apellido = models.CharField(max_length = 70, blank=True, default='')
    rut = models.CharField(max_length = 10, blank=True, default='')
    dv = models.CharField(max_length = 1, blank=True, default='')
    telefono = models.CharField(max_length=15, blank=True, default='0')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, null=True)
    
    is_active = models.BooleanField(default = True)
    is_superuser = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'correo'
    EMAIL_FIELD = 'correo'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    def get_full_name(self):
        return self.nombre + ' ' + self.apellido   
    def get_short_name(self):
        return self.correo
    
    def __str__(self):
        return self.correo + ' | ' + self.nombre + ' ' + self.apellido
    
class Tag(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        
    def __str__(self):
        return self.nombre
    
class Anuncio(models.Model):
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    
    class Meta:
        verbose_name = 'Anuncio'
        verbose_name_plural = 'Anuncios'

    def __str__(self):
        return self.titulo
    
class Rating(models.Model):
    puntuacion = models.FloatField(blank=True, default=0)
    comentario = models.CharField(max_length = 255, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarioCalificado')
    usuarioCalificador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarioCalificador')
    
    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
    
    def __str__(self):
        return 'Usuario: ' + str(self.usuario) + ' | Calificador: ' + str(self.usuarioCalificador) + ' | Puntuacion: ' + str(self.puntuacion)
    
class ChatRoom(models.Model):
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profesorChat')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnoChat')
    
    class Meta:
        verbose_name = 'Chat Room'
        verbose_name_plural = 'Chat Rooms'
        
    def __str__(self):
        return 'Profesor: ' + str(self.profesor) + ' | Alumno: ' + str(self.alumno) + ' | Code: ' + str(self.id)

class ChatMessage(models.Model):
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return 'Usuario: ' + str(self.usuario) + ' | Mensaje: ' + str(self.message) + ' | Timestamp: ' + str(self.timestamp) + ' | ChatRoom: ' + str(self.chatRoom)
    
class Reserva(models.Model):
    estado = models.CharField(max_length = 20, blank=True, default='')
    fechaHora = models.DateTimeField()
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profesorReserva')
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnoReserva')
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        
    def __str__(self):
        return 'Fecha: ' + str(self.fechaHora) + ' | Profesor: ' + str(self.profesor) + ' | Alumno: ' + str(self.alumno) + ' | Estado: ' + str(self.estado)
    