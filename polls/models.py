"""This module contains the Question and Choice models."""
import datetime
from secrets import choice
from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    """Question model for creating questions."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """Return readable string of each question."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        """Return boolean whether it was published recently."""
        now = timezone.localtime()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return boolean when the question was published."""
        now = timezone.localtime()
        return now >= self.pub_date

    def can_vote(self):
        """Return boolean when voting is allowed."""
        now = timezone.localtime()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Choice model for creating choice."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Return readable string of each choice."""
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def question(self):
        return self.choice.question