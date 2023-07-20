from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.generics import GenericAPIView
from .models import UserAccount, Teachers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from djoser.views import TokenCreateView
from rest_framework.decorators import permission_classes
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.conf import settings


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_403_FORBIDDEN)
            
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)

        if not user.is_staff:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        user_data = {
            'email': user.email,
            'name': user.name,
        }

        response_data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class RetrieveUserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = UserAccount.objects.filter(
            is_staff=False, is_student=True).order_by('-date_joined')
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class GetOneUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        # email = 'root@gmail.com'
        email = request.GET.get('email')
        user = UserAccount.objects.get(email=email)
        serializer = UserSerializer(user)
        print(request)
        return Response(serializer.data)


class ViewOneUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):

        # email = 'root@gmail.com'
        # email = request.GET.get('email')
        try:
            user = UserAccount.objects.get(id=user_id)
            serializer = UserSerializer(user)
            print(request)
            return Response(serializer.data)
        except UserAccount.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
          


class DeleteUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, id):
        user = UserAccount.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

# @permission_classes([IsAdminUser])


class BlockUser(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, id):
        try:
            user = UserAccount.objects.get(id=id)
            user.is_block = not user.is_block  # Toggle the value of `is_block`
            user.save()
            return Response(user.is_block,status=status.HTTP_202_ACCEPTED)
        except UserAccount.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


# class Login(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if email is None or password is None:
#             return Response({'error': 'Invalid email or password'}, status=status.HTTP_403_FORBIDDEN)
        
#         user = UserAccount.objects.get(email=email)
        
#         if user is not None:
#             if user.is_active:
#                 # Check if the user is blocked
#                 if user.is_block:
#                     return Response({'message': 'Your account has been blocked'}, status=status.HTTP_403_FORBIDDEN)
                
                
#                 user = authenticate(request, email=email, password=password)

#                 # Login the user
#                 login(request, user)

#                 # Generate JWT token
#                 refresh = RefreshToken.for_user(user)

#                 return Response({'message': 'Login successful', 'access': str(refresh.access_token), 'refresh': str(refresh)})
#             else:
#                 return Response({'message': 'Your account is inactive'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class Login(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        data = request.data 
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        

        return Response({'message': 'Login successful','email':user.email, 'access': str(refresh.access_token), 'refresh': str(refresh)})

# class Teacher(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         is_submit = request.data.pop('is_submit', False)
#         if is_submit == False:
#             pass
#         else:
#             is_submit = True
#         # Save the value of is_submit to the User model
#         user = request.user
#         user.is_submit = is_submit# Add the current datetime
#         user.save()
#         # Remove is_submit from request.data
#         request.data.pop('is_submit', None)
#         print(request.data)
#         serializer = TeacherCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Teacher(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data)
        data = request.data.copy()
        is_submit = data.pop('is_submit', False)
        mobile_number = data.pop('mobile_number', None)[0]
        country = data.pop('country', None)[0] 
        image = data.pop('image', None)[0]
        name = data.pop('name', None)[0]
        if is_submit == False:
            pass
        else:
            is_submit = True
        # Save the value of is_submit to the UserAccount model
        # Add the user id to the request data
        data['user'] = request.user.id
        print(request.data)
        print(is_submit,
              mobile_number,
              country,
              image,
              name)
        user = request.user
        user.is_submit = is_submit
        user.mobile_number = mobile_number
        user.country = country
        user.image = image
        user.name = name
        user.save()
        print(data)

        # Remove is_submit from request.data
        user_data = UserAccount.objects.get(id=user.id)
        user_data.is_pending = True
        user_data.save()
        data.pop('is_submit', None)
        data.pop('mobile_number', None)
        data.pop('country', None)
        data.pop('image', None)
        data.pop('name', None)
        data['user'] = user.id  # Add the user id to the data
        print(data)
        serializer = TeacherCreateSerializer(data=data)
        if serializer.is_valid():
            teacher = serializer.save(user=user)  # Assign the user instance to the user field
            query = UserAccount.objects.get(id=user.id)
            serializer_data = UserSerializer(query)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RequestTeacher(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # queryset = Teachers.objects.all()
#         queryset = Teachers.objects.filter(
#             is_verified=False).order_by('-created_at')
#         serializer = TeacherSerializer(queryset, many=True)
#         return Response(serializer.data)

class RequestTeacher(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Teachers.objects.filter(
            user__is_teacher=False,user__is_submit=True, user__is_verified=False
        ).order_by('-created_at')
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class RetrieveOneTeacherView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            teacher = Teachers.objects.get(user_id=id)
        except Teachers.DoesNotExist:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class OneTeacher(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            teacher = Teachers.objects.select_related('user').get(user_id=id)

            serializer = TeacherSerializer(teacher)
            print(request)
            return Response(serializer.data,status=200)
        except Teachers.DoesNotExist:
            return Response({'message': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)


class Verify(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, id):
        print(self)
        try:
            # teacher = Teachers.objects.select_related('user').get(user_id=id)
            user = UserAccount.objects.get(id=id)
            if user.is_teacher:
                return JsonResponse({'message': 'Teacher is already verified'})
            user.is_student = False
            user.is_teacher = True
            user.save()

            # Send email
            subject = 'Teacher Verification'
            message = 'Congratulations! You have been verified as a teacher.\n\n'
            message += 'Please click on the following link to access your account:\n\n'
            message += f'{settings.FRONT_END}/profile'

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            return JsonResponse({'message': 'Teacher verified successfully'})
        except Teachers.DoesNotExist:
            return JsonResponse({'message': 'Teacher not found'}, status=404)


class Reject(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, id):
    
            user = UserAccount.objects.get(id=id)

            teacher = Teachers.objects.get(user_id=id)
            if user.is_teacher:
                return JsonResponse({'message': 'Cannot reject an already verified teacher'})
            if teacher:
                # Perform rejection logic

                # Send email
                subject = 'Teacher Rejection'
                message = 'We regret to inform you that your teacher application has been rejected.'
                from_email = 'mithuncy65@gmail.com'
                to_email = user.email
                send_mail(subject, message, from_email, [to_email])

                # Delete the teacher
                user.is_submit = False
                user.save()
                teacher.delete()
                return JsonResponse({'message': 'Teacher rejected and deleted successfully'})
            else:
                return JsonResponse({'message': 'Teacher not found'}, status=404)


class RetrieveTeacherView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Teachers.objects.filter(
            user__is_teacher=True,user__is_submit=True
        ).order_by('-created_at')
        serializer = TeacherSerializer(queryset, many=True)
        return Response(serializer.data)


# class BlockTeacher(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, id):
#         try:
#             teacher = Teachers.objects.get(id=id)
#             teacher.is_block = not teacher.is_block  # Toggle the value of `is_block`
#             teacher.save()
#             return Response(status=status.HTTP_202_ACCEPTED)
#         except Teachers.DoesNotExist:
#             return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class EditUser(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id): 
        if int(id) == request.user.id:
            try:
                user = UserAccount.objects.get(pk=id)
            except UserAccount.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserEditSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            is_teacher = user.is_teacher

            if is_teacher:
                teacher = Teachers.objects.get(user=user)
                teacher_serializer = TeacherSerializer(
                    teacher, data=request.data, partial=True)
                if not teacher_serializer.is_valid():
                    return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                teacher_serializer.save()

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":"You have no permission to do this"}, status=status.HTTP_200_OK)

# class VerifyOtp(APIView):
#     permission_classes=[AllowAny]
#     def post(self,request):
#         print(request,request.data)
#         otp = request.data.get('otp')
#         user_id = request.data.get('id')



def verify_teacher(modeladmin, request, queryset):
    for teacher in queryset:
        user = teacher.user
        if user.is_teacher:
            return JsonResponse({'message': 'Teacher is already verified'})
        user.is_student = False
        user.is_teacher = True
        user.is_submit = True
        user.is_pending = False
        user.save()

        # Send email
        subject = 'Teacher Verification'
        message = 'Congratulations! You have been verified as a teacher.\n\n'
        message += 'Please click on the following link to access your account:\n\n'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    return JsonResponse({'message': 'Teachers verified successfully'})



def reject_teacher(modeladmin, request, queryset):
    for teacher in queryset:
        user = teacher.user
        if user.is_teacher:
            return JsonResponse({'message': 'Cannot reject an already verified teacher'})
        user.is_student = True
        user.is_teacher = False
        user.is_submit = False
        user.is_pending = False
        user.save()
        teacher.delete()

        # Send email
        subject = 'Teacher Rejection'
        message = 'We regret to inform you that your teacher application has been rejected.'
        from_email = 'mithuncy65@gmail.com'
        to_email = user.email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    return JsonResponse({'message': 'Teacher rejected and deleted successfully'})
