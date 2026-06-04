from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.noticias.serializers import NoticiaSerializer, NoticiaInputSerializer
from apps.noticias.models import Noticia


class NoticiaViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Noticia.objects.all()


    @extend_schema(
        summary="Rota de visualização única de notícia.",
        description="Aceita um ID numérico como parâmetro e retorna a notícia associada a esse.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: NoticiaSerializer}
    )
    def retrieve(self, request, id):
        """Retorna uma notícia por id."""
        noticia = get_object_or_404(
            Noticia, 
            pk=id, 
            usuario_id=request.user.id
        )

        return Response(NoticiaSerializer(noticia).data, status=200)


    @extend_schema(
        summary="Rota de visualização de listagem de notícias.",
        description="Retorna todas as notícias.",
        responses={200: NoticiaSerializer(many=True)}
    )
    def list(self, request):
        """Retorna todas as notícias indexadas pelo usuário."""
        noticias = self.queryset.filter(
            usuario_id=request.user.id
        )

        return Response(NoticiaSerializer(noticias, many=True).data, status=200)


    @extend_schema(
        summary="Rota de criação de notícia.",
        description="Recebe uma notícia e registra-a no sistema.",
        request=NoticiaInputSerializer,
        responses={403: None, 201: NoticiaSerializer}
    )  
    def create(self, request):
        """Registra uma postagem de um usuário autorizado."""
        if not request.user.is_authorized:
            return Response(status=403)
        
        serializer = NoticiaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(usuario=request.user)

        return Response(serializer.data, status=201)   # type: ignore


    @extend_schema(
        summary="Rota de deleção de notícia.",
        description="Aceita um ID numérico como parâmetro e deleta a notícia associada a esse.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: str}
    )
    def destroy(self, request, noticia_id):
        """Deleta uma notícia do usuário pelo id."""
        noticia = get_object_or_404(Noticia, pk=noticia_id)

        if noticia.usuario_id != request.user.id:  # type: ignore
            return Response(status=404)

        noticia.delete()

        return Response({
            'success': 'Notícia deletada com sucesso.'
        }, status=200)
