from rest_framework import serializers
from .models import CustomUser, Category
from rest_framework import serializers
from .models import CustomUser, UserRole, Table, Correct, Answers, Checkbox, Questions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.user_role.role if user.user_role else "No role"  # Token ichiga rol qo'shish
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class CorrectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Correct
        fields = '__all__'

class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = '__all__'

class CheckboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkbox
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuestionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id']