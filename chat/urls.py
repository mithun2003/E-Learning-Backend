from django.urls import path
from .views import ChatMessageView


urlpatterns = [
    path('', ChatMessageView.as_view(), name='chat_message_view'),
    # path('?room_name=<str:roomName>', ChatMessageView.as_view(), name='chat_message_view'),
]
