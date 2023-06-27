from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from django.shortcuts import get_object_or_404


class QuizView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateQuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        course_id = request.query_params.get('course_id')
        print("course id", course_id)
        course = get_object_or_404(Course, pk=course_id)
        quizzes = Quiz.objects.filter(course=course)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizAttemptAPIView(APIView):
    def post(self, request, course_id):
        user = request.user
        submitted_answers = request.data.get('answers', [])

        # Retrieve all quizzes for the given course
        quizzes = Quiz.objects.filter(course_id=course_id)

        quiz_attempt, created = QuizAttempt.objects.get_or_create(
            user=user, course_id=course_id)
        score = 0
        for quiz in quizzes:
            correct_answers = quiz.correct_answer.split(',')
            score += 1
            # Update the quiz attempt
        quiz_attempt.score = score
        quiz_attempt.is_completed = True
        quiz_attempt.save()

        return Response({'message': 'Quiz attempts saved successfully.'}, status=status.HTTP_201_CREATED)