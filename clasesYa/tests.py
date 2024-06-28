from django.test import TestCase
from clasesYa.models import Campo, TipoUsuario, Anuncio, User
from django.urls import reverse
class ModelStrTest(TestCase):
    def testStrCampo(self):
        campo = Campo.objects.create(nombre='Campo1')
        correct_str = 'Code: ' + str(campo.id) + ' | Nombre: Campo1'
        self.assertEqual(str(campo), correct_str)

    def testStrTipoUsuario(self):
        tipo_usuario = TipoUsuario.objects.create(nombre='Profesor')
        self.assertEqual(str(tipo_usuario), 'Code: ' + str(tipo_usuario.id) + ' | Nombre: Profesor')
class AnuncioViewTests(TestCase):

    def setUp(self):
        self.campo = Campo.objects.create(nombre='Ciencia')
        self.anuncio1 = Anuncio.objects.create(titulo='Clase de Física', subTitulo='Nivel avanzado',
            descripcion='Descripción de la clase', precio=200, campo=self.campo)
        self.anuncio2 = Anuncio.objects.create(titulo='Clase de Química', subTitulo='Nivel intermedio', 
            descripcion='Descripción de la clase', precio=150, campo=self.campo)
        
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword', email='superuser@example.com')
        self.client.login(username='superuser@example.com', password='superpassword')

    def test_anuncio_list_view_status_code(self):
        response = self.client.get(reverse('anuncio_list'))
        self.assertEqual(response.status_code, 200)

    def test_anuncio_list_view_template(self):
        response = self.client.get(reverse('anuncio_list'))
        self.assertTemplateUsed(response, 'anuncio_list.html')

    def test_anuncio_list_view_content(self):
        response = self.client.get(reverse('anuncio_list'))
        self.assertContains(response, 'Clase de Física')
        self.assertContains(response, 'Clase de Química')