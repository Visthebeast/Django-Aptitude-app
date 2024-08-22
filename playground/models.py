from django.db import models
import uuid
import random
# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    category_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category_name

class Questions(BaseModel):
    category = models.ForeignKey(Category,related_name='category_question', on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=5)

    def __str__(self) -> str:
        return self.question

    def get_answers(self):
        answer_objs = Answer.objects.filter(question=self)
        data=[]

        for answer_obj in answer_objs:
            data.append({
                'answer' : answer_obj.answer,
                'is_correct' : answer_obj.is_correct
            })
        random.shuffle(data)
        return data
    

class Answer(BaseModel):
    question = models.ForeignKey(Questions,related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.answer 
    

# #

class User(BaseModel):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.user_id})"

class UserResponse(BaseModel):
    user = models.ForeignKey(User, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, related_name='responses', on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, related_name='responses', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.question.question}"

class Score(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.category.category_name}: {self.score}"

# #