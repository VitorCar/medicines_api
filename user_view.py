from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import os

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite acesso sem token JWT/Sessão
def create_superuser_secret(request):
    # Pega o segredo enviado na requisição e o segredo salvo no servidor
    client_secret = request.data.get('secret_key')
    server_secret = os.environ.get('ADMIN_CREATION_SECRET')

    # Proteção 1: Garante que a variável foi configurada no Render
    if not server_secret:
        return Response(
            {'error': 'A rota de criação está desativada no servidor.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Proteção 2: Valida se a senha enviada está correta
    if client_secret != server_secret:
        return Response(
            {'error': 'Credencial secreta inválida.'}, 
            status=status.HTTP_403_FORBIDDEN
        )

    # Coleta os dados do novo administrador
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response(
            {'error': 'Os campos username, email e password são obrigatórios.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verifica se o usuário já existe para não quebrar o banco
    if User.objects.filter(username=username).exists():
        return Response(
            {'message': f'O usuário {username} já existe.'}, 
            status=status.HTTP_200_OK
        )

    # Cria efetivamente o superusuário
    User.objects.create_superuser(username=username, email=email, password=password)
    
    return Response(
        {'message': 'Superusuário criado com sucesso!'}, 
        status=status.HTTP_201_CREATED
    )
