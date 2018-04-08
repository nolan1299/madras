import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest import skip

from .utils import get_metrics_github
from ..registration.models import User
from .views import NextApplication, Rating
from ..application.models import Application
from .models import RatingResponse


class UtilsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com', password='testing', is_staff=True)
        self.user2 = User.objects.create(email='test2@example.com', password='testing2')

        self.application = Application.objects.create(user=self.user)
        self.application2 = Application.objects.create(user=self.user2)

        self.factory = APIRequestFactory()

    @skip("This test reaches the GitHub API request limit too easily.")
    def test_github_metrics(self):
        metrics = get_metrics_github("ezwang")
        self.assertEquals(len(metrics), 4)

    def test_next_applicant(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user)
        response = NextApplication.as_view()(request)
        self.assertEquals(response.data["applicant_id"], self.application.id)

    def test_post_review(self):
        data = {"applicant_id": 1, "user_rating": 2, "comments": "hi"}
        request = self.factory.post('/reader/rating', json.dumps(data), content_type="application/json")
        force_authenticate(request, user=self.user)
        Rating.as_view()(request)
        self.assertEquals(1, RatingResponse.objects.count())

    def test_permission_denied(self):
        request = self.factory.get('/reader/next_application/')
        force_authenticate(request, user=self.user2)
        response = NextApplication.as_view()(request)
        self.assertEquals(403, response.status_code)
