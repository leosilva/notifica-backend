from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import requests
from accounts.serializers import CredentialsSerializer
from accounts.models import User

SUAP_URL = 'https://suap.ifrn.edu.br/api'


class RegisterView(GenericAPIView):
    serializer_class = CredentialsSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = self._get_suap_token(serializer)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=400)

        user_data = self._get_user_data(token)

        if user_data.get('campus') != 'CM':
            return Response({
                'error': 'Campus não autorizado.'
            })
        
        try:
            user = User.objects.create(
                username=serializer.validated_data.get('username'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                email=user_data.get('email')
            )
            user.set_password(serializer.validated_data.get('password'))
            user.save()
        except:
            return Response({
                'error': 'Usuário já existente.'
            }, status=409)
        
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
            'first_name': nome[0],
            'last_name': nome[1],
        }