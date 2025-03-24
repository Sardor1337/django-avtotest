import random
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated  # Import permission
from .models import Category, Questions
from .serializers import CategorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, QuestionIDSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Questions, Answers, Checkbox, CustomUser
from django.shortcuts import get_object_or_404


# 1️⃣ Savol va javoblarni olish
class GetQuestionView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Questions, id=question_id)
        answers = Answers.objects.filter(question=question)

        data = {
            "question": {
                "id": question.id,
                "LanUz": question.LanUz,
                "LanKrill": question.LanKrill,
                "LanRu": question.LanRu,
                "LanKarakalpak": question.LanKarakalpak,
                "Image": question.Image.url if question.Image else None
            },
            "answers": [
                {"id": ans.id, "LanUz": ans.LanUz, "LanKrill": ans.LanKrill,
                 "LanRu": ans.LanRu, "LanKarakalpak": ans.LanKarakalpak, "is_correct": ans.is_correct}
                for ans in answers
            ]
        }
        return Response(data, status=status.HTTP_200_OK)


class SubmitAnswerView(APIView):
    def post(self, request):
        user = request.user  # Foydalanuvchini olish (Token orqali)
        question_id = request.data.get('question_id')  # Frontenddan kelgan savol ID
        answer_id = request.data.get('answer_id')  # Frontenddan kelgan javob ID

        # 1️⃣ Savolni va foydalanuvchining tanlagan javobini topish
        question = get_object_or_404(Questions, id=question_id)
        selected_answer = get_object_or_404(Answers, id=answer_id, question=question)

        # 2️⃣ Javob to'g'ri yoki noto‘g‘ri ekanligini tekshirish
        if selected_answer.is_correct:
            is_correct = True
            correct_answer_id = None  # To'g'ri javob bo'lsa, boshqa javobni qaytarmaymiz
        else:
            is_correct = False
            correct_answer = Answers.objects.filter(question=question, is_correct=True).first()
            correct_answer_id = correct_answer.id if correct_answer else None  # Agar to‘g‘ri javob bo‘lsa, uning ID sini olamiz

        # 3️⃣ Checkbox jadvaliga natijani saqlash
        Checkbox.objects.create(
            user=user,
            savol=question,
            is_correct=is_correct,
            correct_answer=correct_answer.LanUz if correct_answer else "Noma'lum"
        )

        # 4️⃣ Frontendga natijani qaytarish
        return Response(
            {"is_correct": is_correct, "correct_answer_id": correct_answer_id},
            status=status.HTTP_200_OK
        )

# 3️⃣ Foydalanuvchi natijalarini olish
class UserResultsView(APIView):
    def get(self, request):
        user = request.user
        correct_count = Checkbox.objects.filter(user=user, is_correct=True).count()
        incorrect_count = Checkbox.objects.filter(user=user, is_correct=False).count()

        # Foydalanuvchiga tegishli natijalarni o'chirish
        Checkbox.objects.filter(user=user).delete()

        return Response({"correct": correct_count, "incorrect": incorrect_count}, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class QuestionsByCategoryView(APIView):
    def get(self, request, category_id):
        questions = Questions.objects.filter(categoryId_id=category_id)
        serializer = QuestionIDSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Token talab qilamiz


class RandomQuestionsView(APIView):
    def get(self, request, count):
        try:
            count = int(count)
            if count not in [20, 50]:
                return Response({"error": "Faqat 20 yoki 50 sonini kiriting!"}, status=status.HTTP_400_BAD_REQUEST)

            question_ids = list(Questions.objects.values_list("id", flat=True))  # Barcha savollar ID larini olish
            random.shuffle(question_ids)  # Tasodifiy tartiblash

            return Response({"question_ids": question_ids[:count]}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Noto'g'ri format, faqat son kiritilishi kerak!"},
                            status=status.HTTP_400_BAD_REQUEST)


