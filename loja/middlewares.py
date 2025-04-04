from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication


class TokenAuthMiddleware:
    """
    Middleware de autenticação para Django Channels utilizando tokens do Django Knox.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Extrai o token da query string
        query_string = parse_qs(scope['query_string'].decode())
        token = query_string.get('token')

        if token:
            # Autentica o token de forma assíncrona
            user = await self.get_user(token[0])
            scope['user'] = user
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        knox_auth = TokenAuthentication()
        try:
            user, _ = knox_auth.authenticate_credentials(
                token.encode('utf-8'))
            return user
        except Exception:
            return AnonymousUser()
