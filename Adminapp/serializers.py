from rest_framework import serializers
from .models import *
from django.db.models import Avg
from Reviewapp.models import Reportreview,Review


class Actorserializer(serializers.ModelSerializer):
    "This is a Actor list serializer"
    class Meta:
        model = Actor
        fields= "__all__"

    def validate_Name(self, value):
        actors = Actor.objects.filter(Name__iexact=value)
        if self.instance:
            actors = actors.exclude(pk=self.instance.pk)

        if actors.exists():
            raise serializers.ValidationError('Actor alrady present')
        return value

class Movieserializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields= "__all__"

    def validate_Runtime(self, value):
        if value<=0:
            raise serializers.ValidationError('Runtime should be grater then 0')
        return value


class Castserializer(serializers.ModelSerializer):
    class Meta:
        model= Cast
        fields= "__all__"

    def validate(self, data):
        actor = data.get('Actor_name', self.instance.Actor_name if self.instance else None)
        movie = data.get('Movie_name', self.instance.Movie_name if self.instance else None)

        casts = Cast.objects.filter(Actor_name=actor, Movie_name=movie)
        if self.instance:
            casts = casts.exclude(pk=self.instance.pk)

        if casts.exists():
            raise serializers.ValidationError('Actor alrady added in cast')
        return data



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields= ['id','Name']



class BulkCastListSerializer(serializers.ListSerializer):
    def validate(self, data):
        movie = self.context['movie']
        actor_ids = [item['Actor_name'].pk for item in data]

        if len(actor_ids) != len(set(actor_ids)):
            raise serializers.ValidationError(
                'The same actor cannot be added more than once.'
            )

        existing_actor_ids = set(
            Cast.objects.filter(
                Movie_name=movie,
                Actor_name_id__in=actor_ids,
            ).values_list('Actor_name_id', flat=True)
        )
        if existing_actor_ids:
            raise serializers.ValidationError(
                'One or more actors are already in this movie cast.'
            )

        return data


class Bulkaddserializer(serializers.ModelSerializer):
    class Meta:
        model=Cast
        fields=['Actor_name','Character']
        list_serializer_class = BulkCastListSerializer


class Reviewserializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"


class Reportserializer(serializers.ModelSerializer):
    reported_review=Reviewserializer(read_only=True)
    class Meta:
        model=Reportreview
        fields=['id','reason',"reasoncategorie","reported_review","report_user","created_at",'status']
        read_only_fields=['id','reason',"reasoncategorie","reported_review","report_user","created_at"]

