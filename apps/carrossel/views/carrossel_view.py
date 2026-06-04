from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.noticias.models import Noticia
from apps.postagens.models import Postagem
from core.serializers import ConteudoSerializer

from collections import deque


class CarrosselView(APIView):

    @extend_schema(
        summary="Rota de carrossel.",
        description="Retorna as notícias e postagens das últimas 12 horas em uma proporção de 5 notícias para 1 postagem.",
        responses={200: ConteudoSerializer(many=True)}
    )
    def get(self, request):
        noticias, postagens = self._get_content()

        noticias = deque(noticias)
        postagens = deque(postagens)

        conteudo = []

        while noticias or postagens:
            for _ in range(5):
                if noticias:
                    conteudo.append(noticias.popleft())
                
            if postagens:
                conteudo.append(postagens.popleft())
        
        return Response(conteudo, status=200)
    
    def _get_content(self):
        noticias = Noticia.objects.filter(
            publicado_em__gte=datetime.now() - timedelta(hours=12),
            disponivel=True,
        ).order_by("?")
        noticias_serial = ConteudoSerializer(noticias, many=True)

        postagens = Postagem.objects.filter(
            publicado_em__gte=datetime.now() - timedelta(hours=12),
        ).order_by("publicado_em")
        postagens_serial = ConteudoSerializer(postagens, many=True)

        return list(noticias_serial.data), list(postagens_serial.data)
