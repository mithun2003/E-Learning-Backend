from django.forms.models import model_to_dict
import json
# Create your views here.
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import ChatRoom, ChatMessage
from account.models import *
from .serializer import *
class ChatMessageView(APIView):
    def post(self, request):
        room_name = request.data.get('room_name')
        sender_id = request.data.get('sender_id')
        message = request.data.get('message')

        print(room_name)
        try:
            print(room_name)
            room = ChatRoom.objects.get(name=room_name)
            print(room)
            sender = UserAccount.objects.get(id=sender_id)

            chat_message = ChatMessage.objects.create(
                room=room,
                sender=sender,
                message=message
            )
            try:
                data_ = ChatMessage.objects.filter(sender=sender,message=message).first()
                # data_['sender']=sender.name
                serializer = ChatSerializer(data_)
                data = serializer.data
            except ChatMessage.DoesNotExist:
                data=None
            return JsonResponse({'success': True, 'message': 'Message added successfully.','data':data})
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Chat room does not exist.'})
        except UserAccount.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sender user does not exist.'})

    # def get(self, request):
    #     room_name = request.GET.get('room_name')
    #     print(room_name)
    #     try:
    #         room = ChatRoom.objects.get(name=room_name)
    #         messages = room.messages.all()

    #         # data = [{'sender': message.sender.name, 'message': message.message,'time':message.timestamp} for message in messages]
    #         data = [{'sender': {
    #                  'id': message.sender.id,
    #                  'name': message.sender.name,
    #                  'email': message.sender.email,
    #                  'is_teacher':message.sender.is_teacher,
    #                  'image':message.sender.image.url
    #                  # Include other fields you want to include
    #              },
    #              'message': message.message,
    #              'time': message.time}
    #             for message in messages]
    #         return JsonResponse({'success': True, 'messages': data})
    #     except ChatRoom.DoesNotExist:
    #         return JsonResponse({'success': False, 'message': 'Chat room does not exist.'})
    def get(self, request):
        room_name = request.GET.get('room_name')
        try:
            room = ChatRoom.objects.get(name=room_name)
            messages = room.messages.all().order_by('time')

            serializer = MessageSerializer(messages, many=True)
            data = serializer.data

            return JsonResponse({'success': True, 'messages': data})
        except ChatRoom.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Chat room does not exist.'})