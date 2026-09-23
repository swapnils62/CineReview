from rest_framework import serializers
from .models import Review,Reportreview


#Admin app imports
from Adminapp.models import Movie
from django.db.models import Avg


from Userapp.models import Watchlist


class Reviewserializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model=Review
        fields = [
            "id", "Title", "Review", "Rating",
            "Created_at", "user", "Movie", "user_name",
        ]
        read_only_fields=['user','Movie']

    def validate(self, data):

        request=self.context['request']
        movie=self.context.get('movie')

        if movie and Review.objects.filter(Movie=movie, user=request.user).exists():
            raise serializers.ValidationError('You Alrady Given The Review')
        return data



class MovielistSerializer(serializers.ModelSerializer):
    average_rating=serializers.FloatField(read_only=True)

    class Meta:
        model=Movie
        fields=['id','Title','Poster','Released_date','average_rating']


class Movieserializer(serializers.ModelSerializer):
    average_rating=serializers.FloatField(read_only=True)
    class Meta:
        model = Movie
        fields= ['Title','Synopsis','Runtime','Poster','Released_date',"Director",'average_rating','Genre_name']

class Watchlistserailizer(serializers.ModelSerializer):
    class Meta:
        model=Watchlist
        fields = ['id', 'movie', 'created_at']
        read_only_fields = ['id', 'movie', 'created_at']

    def validate(self, data):
    
        request=self.context['request']
        movie=self.context['movie']
    
        if movie and Watchlist.objects.filter(movie=movie,user=request.user).exists():
            raise serializers.ValidationError('Movie is alrady in watchlist')
        return data


class Resportserializr(serializers.ModelSerializer):
    reported_review=Reviewserializer(read_only=True)
    class Meta:
        model=Reportreview
        fields=['id','reason',"reasoncategorie","reported_review","report_user","created_at","status"]
        read_only_fields=["reported_review","report_user","status"]

    def validate(self, data):
        request=self.context['request']
        review=self.context['review']

        if review and Reportreview.objects.filter(reported_review=review,report_user=request.user).exists():
            raise serializers.ValidationError('you alrady report this review')
        return data

