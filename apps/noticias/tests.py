from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.accounts.models import Usuario
from apps.noticias.models import Noticia
from apps.noticias.views import NoticiaViewSet


class NoticiaViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.usuario = Usuario.objects.create(
            username='usuario1',
            email='usuario1@example.com',
            nome='Usuario',
            sobrenome='Um',
            cargo=Usuario.Cargo.SERVIDOR,
        )
        self.outro_usuario = Usuario.objects.create(
            username='usuario2',
            email='usuario2@example.com',
            nome='Usuario',
            sobrenome='Dois',
            cargo=Usuario.Cargo.SERVIDOR,
        )
        self.noticia = Noticia.objects.create(
            titulo='Titulo original',
            corpo='Corpo original',
            link='https://example.com/original',
            imagem='https://example.com/original.jpg',
            usuario=self.usuario,
        )

    def test_update_atualiza_noticia_do_usuario(self):
        request = self.factory.put(f'/api/noticia/{self.noticia.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'link': 'https://example.com/atualizado',
            'imagem': 'https://example.com/atualizado.jpg',
            'disponivel': False,
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = NoticiaViewSet.as_view({'put': 'update'})(
            request,
            pk=self.noticia.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.noticia.refresh_from_db()
        self.assertEqual(self.noticia.titulo, 'Titulo atualizado')
        self.assertEqual(self.noticia.corpo, 'Corpo atualizado')
        self.assertEqual(self.noticia.link, 'https://example.com/atualizado')
        self.assertEqual(self.noticia.imagem, 'https://example.com/atualizado.jpg')
        self.assertFalse(self.noticia.disponivel)

    def test_update_nao_atualiza_noticia_de_outro_usuario(self):
        request = self.factory.put(f'/api/noticia/{self.noticia.pk}/', {
            'titulo': 'Titulo indevido',
            'corpo': 'Corpo indevido',
            'link': 'https://example.com/indevido',
            'imagem': 'https://example.com/indevido.jpg',
            'disponivel': False,
        }, format='json')
        force_authenticate(request, user=self.outro_usuario)

        response = NoticiaViewSet.as_view({'put': 'update'})(
            request,
            pk=self.noticia.pk,
        )

        self.assertEqual(response.status_code, 404)
        self.noticia.refresh_from_db()
        self.assertEqual(self.noticia.titulo, 'Titulo original')
        self.assertEqual(self.noticia.corpo, 'Corpo original')
        self.assertEqual(self.noticia.link, 'https://example.com/original')
        self.assertEqual(self.noticia.imagem, 'https://example.com/original.jpg')
        self.assertTrue(self.noticia.disponivel)

    def test_destroy_remove_noticia_do_usuario(self):
        request = self.factory.delete(f'/api/noticia/{self.noticia.pk}/')
        force_authenticate(request, user=self.usuario)

        response = NoticiaViewSet.as_view({'delete': 'destroy'})(
            request,
            pk=self.noticia.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Noticia.objects.filter(pk=self.noticia.pk).exists())

    def test_viewset_nao_implementa_patch(self):
        self.assertFalse(hasattr(NoticiaViewSet, 'partial_update'))
