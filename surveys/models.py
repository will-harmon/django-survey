from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# class User(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}|{}'.format(self.user.username, self.choice.choice_text)

class Survey(models.Model):
    survey_text = models.CharField(max_length=200)

    def __str__(self):
        return self.survey_text

    def get_absolute_url(self):
        return reverse('surveys:index')

class Choice(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
