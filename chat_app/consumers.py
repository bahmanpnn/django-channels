import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_dict = json.loads(text_data)
        message = text_data_dict['message']

        # self.send() resend data to websocket to echo the message and show in textarea and room page
        self.send(text_data=json.dumps({
            'message': message
        }))
