from typing import Any

from app.moderacao.providers import DeepseekClient
from app.postagens.models import Estado


def moderar_postagem(conteudo: str) -> Any:
    return Estado(DeepseekClient.chat([
        {
            'role': 'system',
            'content': 'Classifique a mensagem APENAS sob uma dessas palavras, em uppercase, sem markdown ou acentuação [`aprovada`, `negada` e `revisao`].'
        },
        {
            'role': 'user',
            'content': conteudo
        }
    ]))
