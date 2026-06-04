from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.postagens.services import validar_postagem
from apps.postagens.serializers import PostagemSerializer, PostagemInputSerializer
from apps.postagens.models import Postagem


class PostagemViewSet(ViewSet):
    queryset = Postagem.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    @extend_schema(
        summary="Rota de visualização de postagem única.",
        description="Aceita um ID numérico como parâmetro e retorna a postagem associada a esse.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: PostagemSerializer}
    )
    def retrieve(self, request, pk):
        postagem = get_object_or_404(
            Postagem, 
            pk=pk,
            usuario_id=request.user.id
        )

        return Response(PostagemSerializer(postagem).data, status=200)
    

    @extend_schema(
        summary="Rota de visualização de todas as postagens.",
        description="Retorna todas as postagens registradas.",
        responses={200: PostagemSerializer(many=True)}
    )
    def list(self, request):
        postagens = self.queryset.filter(
            usuario_id=request.user.id
        )

        return Response(PostagemSerializer(postagens, many=True).data, status=200)

    @extend_schema(
        summary="Rota de criação de notícia.",
        description="Recebe uma notícia e registra-a no sistema.",
        request=PostagemInputSerializer,
        responses={403: None, 201: PostagemSerializer}
    )
    def create(self, request):
        serializer = PostagemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_authorized:
            validacao = validar_postagem(
                serializer.validated_data.get('corpo')  # type: ignore
            )

            if not validacao:
                return Response(status=400)
        
        serializer.save(usuario=request.user)

        return Response(serializer.data, status=201)


    @extend_schema(
        summary="Rota de deleção de notícia.",
        description="Recebe o id de uma notícia e remove-a no sistema.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: None}
    )
    def destroy(self, request, postagem_id):
        postagem = get_object_or_404(Postagem, pk=postagem_id)
        if postagem.usuario_id != request.user.id:  # type: ignore
            return Response(status=404)
        
        postagem.delete()
        
        return Response(status=200)
