from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.noticias.serializers import NoticiaSerializer
from apps.noticias.models import Noticia


class NoticiaViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Noticia.objects.all()


    def retrieve(self, request, pk):
        """Retorna uma notícia por id."""
        noticia = get_object_or_404(
            Noticia, 
            pk=pk, 
            usuario_id=request.user.id
        )

        return Response(NoticiaSerializer(noticia).data, status=200)


    def list(self, request):
        """Retorna todas as notícias indexadas pelo usuário."""
        noticias = self.queryset.filter(
            usuario_id=request.user.id
        )

        return Response(NoticiaSerializer(noticias, many=True).data, status=200)


    def create(self, request):
        """Registra uma postagem de um usuário autorizado."""
        if not request.user.is_authorized:
            return Response({
                'error': 'Usuário não autorizado.'
            }, status=403)
        
        serializer = NoticiaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(usuario=request.user)

        return Response(serializer.data, status=201)   # type: ignore


    def destroy(self, request, noticia_id):
        """Deleta uma notícia do usuário pelo id."""
        noticia = get_object_or_404(Noticia, pk=noticia_id)

        if noticia.usuario_id != request.user.id:  # type: ignore
            return Response({
                'error': 'Essa notícia não foi postada por você.'
            }, status=400)

        noticia.delete()

        return Response({
            'success': 'Notícia deletada com sucesso.'
        }, status=200)
