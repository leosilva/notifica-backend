from datetime import date, datetime

from django.test import SimpleTestCase

from apps.noticias.models import Noticia
from apps.postagens.models import Postagem
from core.serializers import ConteudoSerializer


class ConteudoSerializerTest(SimpleTestCase):
    def test_define_tipo_para_noticia(self):
        noticia = Noticia(
            id=1,
            titulo="Notícia teste",
            corpo="Resumo da notícia",
            link="https://example.com/noticia",
            imagem="https://example.com/imagem.jpg",
            publicado_em=date(2026, 6, 2),
            disponivel=True,
        )

        data = ConteudoSerializer(noticia).data

        self.assertEqual(data["tipo"], "noticia")
        self.assertEqual(data["publicado_em"], "2026-06-02")

    def test_define_tipo_para_postagem(self):
        postagem = Postagem(
            id=2,
            titulo="Postagem teste",
            corpo="Corpo da postagem",
            gradiente_fundo="linear-gradient(red, blue)",
            publicado_em=datetime(2026, 6, 2, 10, 30),
            disponivel=True,
        )

        data = ConteudoSerializer(postagem).data

        self.assertEqual(data["tipo"], "postagem")
        self.assertEqual(data["publicado_em"], "2026-06-02T10:30:00")
        self.assertEqual(data["gradiente_fundo"], "linear-gradient(red, blue)")
