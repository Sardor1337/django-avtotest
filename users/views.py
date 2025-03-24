import random
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated  # Import permission
from .models import Category, Questions, Table, Correct
from .serializers import CategorySerializer, CorrectSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, QuestionIDSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Questions, Answers, Checkbox, CustomUser
from django.shortcuts import get_object_or_404


class GetQuestionView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Questions, id=question_id)
        answers = list(Answers.objects.filter(question=question))
        random.shuffle(answers)

        data = {
            "question": {
                "id": question.id,
                "LanUz": question.LanUz,
                "LanKrill": question.LanKrill,
                "LanRu": question.LanRu,
                "LanKarakalpak": question.LanKarakalpak,
                "Image": request.build_absolute_uri(question.Image.url) if question.Image else None
            },
            "answers": [
                {
                    "id": ans.id, "LanUz": ans.LanUz, "LanKrill": ans.LanKrill,
                    "LanRu": ans.LanRu, "LanKarakalpak": ans.LanKarakalpak,
                    "is_correct": ans.is_correct
                }
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
            correct_answer = Answers.objects.filter(question=question, is_correct=True).first()
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


class QuestionsByTableView(APIView):
    def get(self, request, table_id):
        # Berilgan table_id ga tegishli savollarni olish
        table = get_object_or_404(Table, id=table_id)
        questions = Questions.objects.filter(tableId=table)

        # Faqat savollarning IDlarini qaytarish
        question_ids = [question.id for question in questions]

        return Response({"questions": question_ids}, status=status.HTTP_200_OK)


class TableListView(APIView):
    permission_classes = [IsAuthenticated]  # Faqat token bilan kirish mumkin

    def get(self, request):
        tables = Table.objects.all()  # Barcha tablelarni olish
        table_list = [{"id": table.id, "name": table.name} for table in tables]

        return Response({"tables": table_list}, status=status.HTTP_200_OK)


class SaveOrUpdateCorrectAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')  # Foydalanuvchi ID si
        table_id = request.data.get('table_id')  # Table ID si
        correct_count = request.data.get('correct', 0)  # To'g'ri javoblar soni (default: 0)
        incorrect_count = request.data.get('incorrect', 0)  # Noto‘g‘ri javoblar soni (default: 0)

        # Foydalanuvchi va Table ni olish (Agar mavjud bo‘lmasa, 404 qaytaradi)
        user = get_object_or_404(CustomUser, id=user_id)
        table = get_object_or_404(Table, id=table_id)

        # Correct jadvalida mavjudligini tekshirish
        correct_record, created = Correct.objects.get_or_create(user=user, table=table, defaults={
            'correct': correct_count,
            'incorrect': incorrect_count
        })

        # Agar mavjud bo‘lsa, yangilash
        if not created:
            correct_record.correct = correct_count
            correct_record.incorrect = incorrect_count
            correct_record.save()

        return Response(
            {"message": "Correct data saved successfully"},
            status=status.HTTP_200_OK
        )


class GetUserCorrectAPIView(APIView):
    def get(self, request, user_id):
        # Userga tegishli barcha Correct yozuvlarini olish
        correct_records = Correct.objects.filter(user_id=user_id)

        # Agar hech qanday yozuv topilmasa, bo'sh ro‘yxat qaytaramiz
        if not correct_records.exists():
            return Response({"message": "Ma'lumot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        # Ma'lumotlarni serializer orqali JSON formatga o'tkazish
        serializer = CorrectSerializer(correct_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)