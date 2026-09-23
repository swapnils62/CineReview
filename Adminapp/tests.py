from django.test import TestCase

from .models import Actor, Cast, Movie
from .serializers import Actorserializer, Bulkaddserializer, Castserializer


class AdminSerializerValidationTests(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            Title='Test movie',
            Synopsis='Test synopsis',
            Runtime=120,
            Released_date='2026-01-01',
            Director='Test director',
        )
        self.actor = Actor.objects.create(Name='Actor One', Info='Test actor')
        self.other_actor = Actor.objects.create(Name='Actor Two', Info='Other actor')
        self.cast = Cast.objects.create(
            Actor_name=self.actor,
            Movie_name=self.movie,
            Character='Lead',
        )

    def test_actor_can_keep_its_own_name_when_updated(self):
        serializer = Actorserializer(
            self.actor,
            data={'Name': 'Actor One'},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_cast_can_update_only_character(self):
        serializer = Castserializer(
            self.cast,
            data={'Character': 'Updated lead'},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_bulk_cast_rejects_duplicate_actor_in_request(self):
        serializer = Bulkaddserializer(
            data=[
                {'Actor_name': self.other_actor.pk, 'Character': 'Role one'},
                {'Actor_name': self.other_actor.pk, 'Character': 'Role two'},
            ],
            many=True,
            context={'movie': self.movie},
        )

        self.assertFalse(serializer.is_valid())

    def test_bulk_cast_rejects_actor_already_in_movie(self):
        serializer = Bulkaddserializer(
            data=[{'Actor_name': self.actor.pk, 'Character': 'Another role'}],
            many=True,
            context={'movie': self.movie},
        )

        self.assertFalse(serializer.is_valid())
