import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class Category(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    type = models.CharField(max_length=255, null=True)  # type maydoni varchar turida
    typeLanRu = models.CharField(max_length=255, null=True)  # type maydoni varchar turida
    typeLanKrill = models.CharField(max_length=255, null=True)  # type maydoni varchar turida
    typeLanKarakalpak = models.CharField(max_length=255, null=True)  # type maydoni varchar turida

    def __str__(self):
        return self.type  # type ni chiqarish

class Table(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    name = models.CharField(max_length=100, null=True)  # name maydoni integer turida
    nameLanRu = models.CharField(max_length=100, null=True)
    nameLanKrill = models.CharField(max_length=100, null=True)
    nameLanKarakalpak = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.name)  # name ni chiqarish

class Questions(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    LanUz = models.CharField(max_length=255)  # Uzbek tilidagi savol
    LanKrill = models.CharField(max_length=255)  # Kril alifbosidagi savol
    LanRu = models.CharField(max_length=255)  # Rus tilidagi savol
    LanKarakalpak = models.CharField(max_length=255)  # Qaraqalpoq tilidagi savol
    Image = models.ImageField(upload_to='questions_images/', null=True, blank=True)  # Rasm maydoni (null bo'lishi mumkin)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)  # ForeignKey for Category
    tableId = models.ForeignKey(Table, on_delete=models.CASCADE)  # ForeignKey for Table

    def __str__(self):
        return self.LanUz  # Uzbek tilidagi savolni chiqarish

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    role = models.CharField(max_length=255)  # role maydoni varchar turida

    def __str__(self):
        return self.role  # role ni chiqarish

class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    user_role =  models.ForeignKey(UserRole, null=True, blank=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=15, unique=True)  # phone_numberni username sifatida ishlatish
    create_time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255, unique=False, blank=True, null=True,
                                default="user_{}".format(str(uuid.uuid4())))
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = []  # phone_numberni bu yerda ko'rsatmaslik kerak
    USERNAME_FIELD = 'phone_number'  # phone_numberni USERNAME_FIELD sifatida belgilash
    objects = CustomUserManager()  # CustomUserManager'ni o'rnatish

    def __str__(self):
        return f"User {self.id} - {self.phone_number}"

class Correct(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  # ForeignKey to Table
    correct = models.IntegerField()  # correct maydoni integer turida
    incorrect = models.IntegerField()  # incorrect maydoni integer turida

    def __str__(self):
        return f"Correct for User {self.user.id} - Table {self.table.id}"

class Answers(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    LanUz = models.CharField(max_length=255)  # Uzbek tilidagi javob
    LanKrill = models.CharField(max_length=255)  # Kril alifbosidagi javob
    LanRu = models.CharField(max_length=255)  # Rus tilidagi javob
    LanKarakalpak = models.CharField(max_length=255)  # Qaraqalpoq tilidagi javob
    is_correct = models.BooleanField()  # Javobning to'g'riligi (True yoki False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)  # ForeignKey to Questions model

    def __str__(self):
        return self.LanUz  # Uzbek tilidagi javobni chiqarish

class Checkbox(models.Model):
    id = models.AutoField(primary_key=True)  # PK maydon
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    savol = models.ForeignKey(Questions, on_delete=models.CASCADE)  # ForeignKey to Questions
    is_correct = models.BooleanField()  # isCorrect maydoni boolean turida
    correct_answer = models.CharField(max_length=255)  # correct_answer maydoni varchar turida

    def __str__(self):
        return f"Checkbox for User {self.user.id} - Question {self.savol.id}"

