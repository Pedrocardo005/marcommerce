import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from loja.models import ChatRoom
from loja.serializers import MensagemSerializer


def serialize_mensagem(mensagem):
    serializer = MensagemSerializer(mensagem)
    return serializer.data


class ChatRoomWebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.user = self.scope['user']

        self.chat_room = await self.get_chat_room()
        mensagens = await self.get_mensagens()

        if str(self.user.pk) not in self.room_name.split('_'):
            return
        # if mensagens.exists():
        #     return

        self.room_group_name = self.chat_room.nome

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        async for mensagem in mensagens.aiterator():
            data = await sync_to_async(serialize_mensagem)(mensagem)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat.message", **data},
            )

        await self.accept()

    @database_sync_to_async
    def get_chat_room(self):
        return ChatRoom.objects.filter(nome=self.room_name).first()

    @database_sync_to_async
    def get_mensagens(self):
        return self.chat_room.mensages.filter(
            Q(remetente_id=self.user.pk) | Q(destinatario_id=self.user.pk))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        serializer = MensagemSerializer(data=text_data_json)
        if serializer.is_valid():
            serializer.save()

            await self.channel_layer.group_send(
                # Chama o método chat_message, o '.' se transforma em '_'
                self.room_group_name,
                {"type": "chat.message", **serializer.data},
            )

    async def chat_message(self, event):
        event.pop('type')

        await self.send(text_data=json.dumps(event))
