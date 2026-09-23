
from rest_framework.viewsets import GenericViewSet,ReadOnlyModelViewSet,ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny,IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin,RetrieveModelMixin

# Review app import
from .models import Review,Reportreview
from .serializer import Reviewserializer, MovielistSerializer,Watchlistserailizer,Resportserializr,Movieserializer

# Admin app imports
from Adminapp.serializers import Castserializer
from Adminapp.models import Movie,Cast

#filter imports
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import Mypagination

from django.db.models import Avg


# Create your views here.



class Publicmovieviewset(ReadOnlyModelViewSet):
    '''
    this is used to get the list of all movies 
    
    '''
    queryset = Movie.objects.annotate(average_rating=Avg('review__Rating'))
    serializer_class=Movieserializer
    permission_classes=[AllowAny]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields =['Genre_name']
    search_fields = ["Title"]
    ordering_fields = ["Released_date"]
    pagination_class=Mypagination


    def get_serializer_class(self):
        if self.action == 'list':
            return MovielistSerializer      #it use to list all the movies      
        return Movieserializer              #it is used to get the details of a sinegl movie



class Reviewviewset(ListModelMixin,CreateModelMixin,GenericViewSet):
    serializer_class=Reviewserializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=Mypagination


    def get_movie(self):
        return get_object_or_404(Movie, pk=self.kwargs['movie_pk'])

    def get_queryset(self):
        return (Review.objects.filter(Movie_id=self.kwargs['movie_pk'])
                .select_related('user','Movie').order_by('-Created_at'))

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['movie']=self.get_movie()
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            Movie=self.get_movie()
        )

class Castviewset(ReadOnlyModelViewSet):
    "This is a castview to add cast to movies"
    serializer_class= Castserializer
    permission_classes=[AllowAny]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['Movie_name','Actor_name']

    def get_queryset(self):
        return Cast.objects.filter(Movie_name=self.kwargs['pk'])





class Watchlistviewset(CreateModelMixin,GenericViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Watchlistserailizer

    def get_movie(self):
        return get_object_or_404(Movie, pk=self.kwargs['movie_pk'])


    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['movie']=self.get_movie()
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user,movie=self.get_movie())



class Reportviewset(CreateModelMixin, GenericViewSet):
    serializer_class=Resportserializr
    permission_classes=[IsAuthenticated]

    def get_review(self):
        return get_object_or_404(Review,pk=self.kwargs['review_pk'])

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['review']=self.get_review()
        return context

    def perform_create(self, serializer):
        serializer.save(report_user=self.request.user,reported_review=self.get_review())


