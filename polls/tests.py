"""This module contains the tests for the polls.models."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Vote


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.localtime() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.localtime() - datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_in_the_future(self):
        """
        can_vote() returns False (voting not allowed)
        because it is not pub_date.
        """
        time = timezone.localtime() + datetime.timedelta(days=30)
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_after_end_date(self):
        """
        can_vote() return False (voting not allowed)
        because current time is after end_date.
        """
        time1 = timezone.localtime()
        time2 = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=time1, end_date=time2)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_no_time_limit(self):
        """
        can_vote() returns True (voting allowed)
        for no time limit case (no end_date).
        """
        time = timezone.localtime()
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), True)

    def test_is_published_in_the_future(self):
        """
        is_published() returns False means you cannot vote.
        """
        time = timezone.localtime() + datetime.timedelta(days=30)
        question = Question(pub_date=time)
        self.assertIs(question.is_published(), False)

    def test_is_published_in_the_current(self):
        """
        is_published() returns True means you can vote.
        """
        time = timezone.localtime()
        question = Question(pub_date=time)
        self.assertIs(question.is_published(), True)

    def test_is_published_in_the_past(self):
        """
        is_published() returns True means you can vote.
        """
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        question = Question(pub_date=time)
        self.assertIs(question.is_published(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        user = User.objects.create_user(
            username="someone", email="someone@example.com", password="1234"
        )
        user.save()

    def test_future_question(self):
        """
        The detail view of a question with a pub_date
        in the future returns a 302 not found.
        """
        future_question = create_question(question_text="Future question.",
                                          days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date
        in the past displays the question's text.
        """
        self.client.login(username="someone", password="1234")
        past_question = create_question(question_text="Past Question.",
                                        days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class VoteModelTest(TestCase):
    def setUp(self):
        """Setup before running a tests."""
        self.user = User.objects.create_user(
            username="someone", email="someone@example.com", password="1234"
        )
        self.user.save()

    def test_authenticated_can_vote(self):
        """Test authenticated users can vote."""
        self.client.login(username="someone", password="1234")
        question = create_question(question_text="test", days=1)
        response = self.client.post(reverse("polls:vote", args=(question.id,)))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_cannot_vote(self):
        """Test authenticated users can't vote."""
        question = create_question(question_text="test", days=1)
        response = self.client.post(reverse("polls:vote", args=(question.id,)))
        self.assertEqual(response.status_code, 302)

    def test_one_user_one_vote(self):
        """One user can vote once per question."""
        self.client.login(username="someone", password="1234")
        question = create_question(question_text="test", days=2)
        choice_1 = question.choice_set.create(choice_text="Good")
        choice_2 = question.choice_set.create(choice_text="Not Good")
        self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": choice_1.id}
        )
        self.assertEqual(
            Vote.objects.get(
                user=self.user, choice__in=question.choice_set.all()
            ).choice,
            choice_1,
        )
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.post(
            reverse("polls:vote", args=(question.id,)), {"choice": choice_2.id}
        )
        self.assertEqual(
            Vote.objects.get(
                user=self.user, choice__in=question.choice_set.all()
            ).choice,
            choice_2,
        )
        self.assertEqual(Vote.objects.all().count(), 1)
