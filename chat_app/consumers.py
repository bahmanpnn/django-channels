import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer

from .serializers import MessagesSerializer
from .models import Message

user = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data['message']
        author = data['username']
        user_model = user.objects.filter(username=author).first()
        new_message_model = Message.objects.create(author=user_model, content=message)
        result = eval(self.message_serializer(new_message_model))
        # result = self.message_serializer(new_message_model)
        # result = eval(result)['content']
        self.send_to_chat_message(result)

    def fetch_messages(self, data):
        query_set = Message.last_message(self)
        json_message = self.message_serializer(query_set)
        content = {
            'message': eval(json_message),  # eval() help us to django does not check data is bytes_data or no
            'command': 'fetch_message'
        }
        # now we must send content dic to chat_message method
        self.chat_message(content)

    def message_serializer(self, queryset):
        # queryset.__class__.__name_ when is from fetch method is Queryset other time(new_message method) is
        # new message model type from new_message method and lamda will be false!
        # print((lambda queryset: True if (queryset.__class__.__name__ == 'QuerySet') else False)(queryset))

        serialized = MessagesSerializer(queryset, many=(
            lambda queryset: True if (queryset.__class__.__name__ == 'QuerySet') else False)(queryset)
                                        )
        content = JSONRenderer().render(serialized.data)
        return content

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    commands = {
        'new_message': new_message,
        'fetch_message': fetch_messages
    }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_dict = json.loads(text_data)
        # message = text_data_dict.get('message', None)
        # username = text_data_dict.get('username', None)
        # this part of code is using for choose fetch_message method or new_message method
        command = text_data_dict['command']
        self.commands['command'](self, text_data_dict)

    def send_to_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                # 'message': message,
                'content':message['content'],
                'command': 'new_message',
                '__str__':message['__str__'],
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
        # message = event['message']
        # self.send() resend data to websocket to echo the message and show in textarea and room page

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

# _____________________________________________________________________________________________________

#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat{self.room_name}'
#
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_dict = json.loads(text_data)
#         message = text_data_dict['message']
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     async def chat_message(self, event):
#         message = event['message']
#         # self.send() resend data to websocket to echo the message and show in textarea and room page
#
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
