from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.postagens.services import validar_postagem
from apps.postagens.serializers import PostagemInputSerializer, PostagemOutputSerializer
from apps.postagens.models import Postagem


class PostagemViewSet(ViewSet):
    queryset = Postagem.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]


    @extend_schema(
        summary="Rota de visualização de postagem única.",
        description="Aceita um ID numérico como parâmetro e retorna a postagem associada a esse.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: PostagemOutputSerializer}
    )
    def retrieve(self, request, pk):
        postagem = get_object_or_404(
            Postagem,
            pk=pk,
            usuario_id=request.user.id
        )

        return Response(PostagemOutputSerializer(postagem).data, status=200)


    @extend_schema(
        summary="Rota de visualização de todas as postagens.",
        description="Retorna todas as postagens registradas pelo usuário autenticado.",
        responses={200: PostagemOutputSerializer(many=True)}
    )
    def list(self, request):
        postagens = self.queryset.filter(
            usuario_id=request.user.id
        )

        return Response(PostagemOutputSerializer(postagens, many=True).data, status=200)

    @extend_schema(
        summary="Rota de criação de postagem.",
        description="Recebe uma postagem e registra-a no sistema. Aceita gradiente_fundo (linear-gradient CSS) ou imagem de fundo via URL ou arquivo.",
        request=PostagemInputSerializer,
        responses={400: None, 201: PostagemOutputSerializer}
    )
    def create(self, request):
        serializer = PostagemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_authorized:
            validacao = validar_postagem(
                serializer.validated_data.get('corpo')  # type: ignore
            )

            if not validacao:
                return Response(status=400)

        postagem = serializer.save(usuario=request.user)

        return Response(PostagemOutputSerializer(postagem).data, status=201)


    @extend_schema(
        summary="Rota de atualização de postagem.",
        description="Recebe uma postagem e atualiza-a se pertencer ao usuário autenticado. Aceita gradiente_fundo (linear-gradient CSS) ou imagem de fundo via URL ou arquivo.",
        request=PostagemInputSerializer,
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={400: None, 404: None, 200: PostagemOutputSerializer}
    )
    def update(self, request, pk):
        postagem = get_object_or_404(
            Postagem,
            pk=pk,
            usuario_id=request.user.id
        )

        serializer = PostagemInputSerializer(postagem, data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_authorized:
            validacao = validar_postagem(
                serializer.validated_data.get('corpo')  # type: ignore
            )

            if not validacao:
                return Response(status=400)

        postagem = serializer.save()

        return Response(PostagemOutputSerializer(postagem).data, status=200)


    @extend_schema(
        summary="Rota de deleção de postagem.",
        description="Recebe o id de uma postagem e remove-a no sistema.",
        parameters=[OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH)],
        responses={404: None, 200: None}
    )
    def destroy(self, request, pk):
        postagem = get_object_or_404(
            Postagem,
            pk=pk,
            usuario_id=request.user.id
        )

        postagem.delete()

        return Response(status=200)
