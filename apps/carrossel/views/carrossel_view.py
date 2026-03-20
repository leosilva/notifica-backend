from rest_framework.views import APIView
from rest_framework.response import Response
from apps.noticias.models import Noticia
from apps.noticias.serializers import NoticiaSerializer
from apps.postagens.models import Postagem
from apps.postagens.serializers import PostagemSerializer
from datetime import datetime, timedelta


class CarrosselView(APIView):
    def get(self, request):
        noticias, postagens = self._get_content()

        # Se não tiver um, retorna o outro
        if not postagens:
            return Response(noticias, status = 200)
        if not noticias:
            return Response(postagens, status = 200)

        conteudo = []
        for i in range(max(len(postagens), len(noticias))):
            if not noticias and not postagens:
                break

            try:
                if i % 5 == 0:
                    conteudo.append(postagens[-1])
                    postagens.pop()     # type: ignore
                else:
                    conteudo.append(noticias[-1])
                    noticias.pop()      # type: ignore
            except IndexError:
                pass
        
        return Response(conteudo, status = 200)
    

    def _get_content(self):
        noticias = Noticia.objects.filter(
            data__gte = datetime.now() - timedelta(hours = 12),
            disponivel = True
        ).order_by('?')
        noticias_serial = NoticiaSerializer(noticias, many=True)

        postagens = Postagem.objects.filter(
            data__gte = datetime.now() - timedelta(hours = 12), 
        ).order_by('data')
        postagens_serial = PostagemSerializer(postagens, many=True)

        return noticias_serial.data, postagens_serial.data
    