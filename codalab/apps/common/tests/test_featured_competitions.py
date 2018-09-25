'''
Test to check for featured competitions
'''

import mock

from django.test import TestCase
from django.contrib.auth import get_user_model

from ..competition_utils import get_featured_competitions
from apps.web.models import (Competition,
                             CompetitionParticipant,
                             ParticipantStatus)

User = get_user_model()


class CompetitionHelperTestCase(TestCase):

    def setUp(self):
        '''
        1. Create two different users
        2. Create few compettions where publised is True
        3. Add participants to competitions
        3. Return all competitions
        4. Return competitions with more participants
        '''

        self.user = User.objects.create(email="user1@tes.com", username="user1", password="pass")
        self.user1 = User.objects.create(email="user@test.com", username="user", password="pass")
        self.user2 = User.objects.create(email="user2@test.com", username="user2", password="pass")
        self.user3 = User.objects.create(email="user3@test.com", username="user3", password="pass")
        self.user4 = User.objects.create(email="user4@test.com", username="user4", password="pass")
        self.user5 = User.objects.create(email="user5@test.com", username="user5", password="pass")

        self.competition1 = Competition.objects.create(creator=self.user, modified_by=self.user, published=True)
        self.competition2 = Competition.objects.create(creator=self.user, modified_by=self.user, published=True)
        self.competition3 = Competition.objects.create(creator=self.user, modified_by=self.user, published=True)
        self.competition4 = Competition.objects.create(creator=self.user, modified_by=self.user, published=True)
        self.competition5 = Competition.objects.create(creator=self.user, modified_by=self.user, published=True)

        self.participant1 = CompetitionParticipant.objects.create(
            user=self.user,
            competition=self.competition1,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0]
        )

        self.participant2 = CompetitionParticipant.objects.create(
            user=self.user2,
            competition=self.competition1,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0]
        )

        self.participant3 = CompetitionParticipant.objects.create(
            user=self.user3,
            competition=self.competition1,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0]
        )

        self.participant4 = CompetitionParticipant.objects.create(
            user=self.user1,
            competition=self.competition2,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0]
        )

        self.participant5 = CompetitionParticipant.objects.create(
            user=self.user5,
            competition=self.competition2,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0]
        )

        self.participant6 = CompetitionParticipant.objects.create(
            user=self.user4,
            competition=self.competition4,
            status=ParticipantStatus.objects.get_or_create(name='approved', codename=ParticipantStatus.APPROVED)[0])
