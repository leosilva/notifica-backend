from types import SimpleNamespace
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.accounts.models import Usuario
from apps.postagens.models import Postagem
from apps.postagens.views import PostagemViewSet


class PostagemViewSetTests(TestCase):
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
        self.postagem = Postagem.objects.create(
            titulo='Titulo original',
            corpo='Corpo original',
            usuario=self.usuario,
        )

    def test_update_atualiza_postagem_do_usuario(self):
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'disponivel': False,
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.postagem.refresh_from_db()
        self.assertEqual(self.postagem.titulo, 'Titulo atualizado')
        self.assertEqual(self.postagem.corpo, 'Corpo atualizado')
        self.assertFalse(self.postagem.disponivel)

    def test_update_atualiza_gradiente_fundo(self):
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'gradiente_fundo': 'linear-gradient(red, blue)',
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.postagem.refresh_from_db()
        self.assertEqual(self.postagem.gradiente_fundo, 'linear-gradient(red, blue)')
        self.assertIsNone(self.postagem.imagem)
        self.assertEqual(response.data['gradiente_fundo'], 'linear-gradient(red, blue)')

    def test_update_atualiza_imagem_por_url(self):
        self.postagem.gradiente_fundo = 'linear-gradient(red, blue)'
        self.postagem.save()

        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'imagem': 'https://example.com/fundo.png',
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.postagem.refresh_from_db()
        self.assertIsNone(self.postagem.gradiente_fundo)
        self.assertEqual(self.postagem.imagem, 'https://example.com/fundo.png')
        self.assertEqual(response.data['imagem'], 'https://example.com/fundo.png')

    @patch('apps.postagens.serializers.postagem_input_serializer.upload_image')
    def test_update_atualiza_imagem_por_arquivo(self, upload_image_mock):
        upload_image_mock.return_value = SimpleNamespace(
            url='https://example.com/upload/fundo.png'
        )
        arquivo = SimpleUploadedFile(
            'fundo.png',
            b'conteudo-da-imagem',
            content_type='image/png',
        )
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'imagem': arquivo,
        }, format='multipart')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.postagem.refresh_from_db()
        self.assertEqual(
            self.postagem.imagem,
            'https://example.com/upload/fundo.png',
        )
        upload_image_mock.assert_called_once()

    def test_update_rejeita_gradiente_fundo_invalido(self):
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'gradiente_fundo': 'azul',
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 400)
        self.postagem.refresh_from_db()
        self.assertIsNone(self.postagem.gradiente_fundo)

    def test_update_rejeita_gradiente_fundo_e_imagem_juntas(self):
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo atualizado',
            'corpo': 'Corpo atualizado',
            'gradiente_fundo': 'linear-gradient(red, blue)',
            'imagem': 'https://example.com/fundo.png',
        }, format='json')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 400)
        self.postagem.refresh_from_db()
        self.assertIsNone(self.postagem.gradiente_fundo)
        self.assertIsNone(self.postagem.imagem)

    def test_update_nao_atualiza_postagem_de_outro_usuario(self):
        request = self.factory.put(f'/api/postagem/{self.postagem.pk}/', {
            'titulo': 'Titulo indevido',
            'corpo': 'Corpo indevido',
            'disponivel': False,
        }, format='json')
        force_authenticate(request, user=self.outro_usuario)

        response = PostagemViewSet.as_view({'put': 'update'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 404)
        self.postagem.refresh_from_db()
        self.assertEqual(self.postagem.titulo, 'Titulo original')
        self.assertEqual(self.postagem.corpo, 'Corpo original')
        self.assertTrue(self.postagem.disponivel)

    def test_destroy_remove_postagem_do_usuario(self):
        request = self.factory.delete(f'/api/postagem/{self.postagem.pk}/')
        force_authenticate(request, user=self.usuario)

        response = PostagemViewSet.as_view({'delete': 'destroy'})(
            request,
            pk=self.postagem.pk,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Postagem.objects.filter(pk=self.postagem.pk).exists())

    def test_viewset_nao_implementa_patch(self):
        self.assertFalse(hasattr(PostagemViewSet, 'partial_update'))
