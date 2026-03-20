from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from apps.postagens.services import validar_postagem
from apps.postagens.serializers import PostagemSerializer
from apps.postagens.models import Postagem


class PostagemViewSet(ViewSet):
    def retrieve(self, request, postagem_id):
        postagem = get_object_or_404(
            Postagem, 
            pk=postagem_id, 
            usuario_id=request.user.id
        )

        return Response(PostagemSerializer(postagem).data, status=200)
    

    def list(self, request):
        postagens = Postagem.objects.filter(
            usuario_id=request.user.id
        )

        return Response(PostagemSerializer(postagens).data, status=200)


    def post(self, request):
        serializer = PostagemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_authorized:
            validacao = validar_postagem(
                serializer.validated_data.get('corpo')  # type: ignore
            )

            if not validacao:
                return Response({
                    'error': 'Sua postagem foi filtrada e não é adequada.'
                }, status=400)
        
        serializer.save(user=request.user)

        return Response(serializer.data, status=201)


    def destroy(self, request, postagem_id):
        postagem = get_object_or_404(Postagem, pk=postagem_id)
        if postagem.usuario_id != request.user.id:  # type: ignore
            return Response({
                'error': 'Postagem não encontrada.'
            }, status=404)
        
        postagem.delete()
        
        return Response({
            'success': 'Postagem deletada com sucesso.'
        }, status=200)
