from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
import requests
from apps.accounts.serializers import CredentialsSerializer
from apps.accounts.models import Usuario

SUAP_URL = 'https://suap.ifrn.edu.br/api'


class RegisterView(GenericAPIView):
    serializer_class = CredentialsSerializer
    permission_classes = [AllowAny]


    @extend_schema(
        summary="Registro de usuários.",
        description="Registra um usuário baseado em sua matrícula e senha do SUAP.",
        request=CredentialsSerializer,
        responses={403: None, 409: None, 400: None, 201: None}
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = self._get_suap_token(serializer)
        except Exception as e:
            return Response(status=400)

        user_data = self._get_user_data(token)

        if user_data.get('campus') != 'CM':
            return Response(status=403)
        
        try:
            user = Usuario.objects.create(
                username=serializer.validated_data.get('username'),
                nome=user_data.get('nome'),
                sobrenome=user_data.get('sobrenome'),
                email=user_data.get('email'),
                cargo=user_data.get('cargo'),
            )
            user.set_password(serializer.validated_data.get('password'))
            user.save()
        except IntegrityError:
            return Response(status=409)
        
        return Response(status=201)
        

    def _get_suap_token(self, serializer) -> str:
        response = requests.post(f'{SUAP_URL}/token/pair', json={
            'username': serializer.validated_data.get('username'),
            'password': serializer.validated_data.get('password')
        })

        if response.status_code != 200:
            raise Exception(
                'Matrícula ou senha não foram digitados corretamente.'
            )
        
        body = response.json()
        token = body.get('access')

        return token


    def _get_user_data(self, token: str) -> dict[str, str]:
        response = requests.get(f'{SUAP_URL}/rh/eu/', headers={
            'Authorization': f'Bearer {token}'
        })

        body = response.json()
        nome: list[str] = body.get('nome_usual').split()

        return {
            'email': body.get('email_google_classroom'),
            'campus': body.get('campus'),
            'nome': nome[0],
            'sobrenome': nome[1],
            'cargo': body.get('tipo_usuario').lower(),
        }
