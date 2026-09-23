from django.shortcuts import render

#serializer and model improt
from .serializers import Movieserializer, Castserializer, Actorserializer,GenreSerializer, Bulkaddserializer,Reportserializer
from .models import Movie, Cast, Genre, Actor

#viewset and views import
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin,DestroyModelMixin
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


#authentication and permission imports

from rest_framework.permissions import IsAdminUser


#filter import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import Mypagination



#from Review app import
from Reviewapp.models import Review,Reportreview
from Reviewapp.serializer import Reviewserializer



class Movieviewset(ModelViewSet):
    "This view is for admin to add , delete , update moviees "
    queryset = Movie.objects.all()
    serializer_class=Movieserializer
    permission_classes=[IsAdminUser]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields =['Genre_name','Director']
    search_fields=["Title"]
    ordering_fields=['Released_date']
    pagination_class=Mypagination
    

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def bulkcastadd(self, request, pk):
        movie=get_object_or_404(Movie, pk=pk)
        seralizer=Bulkaddserializer(
            data=request.data,
            many=True,
            context={'movie': movie},
        )
        if seralizer.is_valid():
            seralizer.save(Movie_name=movie)
            return Response(seralizer.data, status=status.HTTP_201_CREATED)
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class Castviewset(ModelViewSet):
    "This is a castview to add cast to movies"
    queryset= Cast.objects.all()
    serializer_class= Castserializer
    permission_classes=[IsAdminUser]
    filter_backends=[DjangoFilterBackend,SearchFilter]
    search_fields=['Movie_name','Actor_name']



class Actorviewset(ModelViewSet):
    queryset=Actor.objects.all()
    serializer_class= Actorserializer
    permission_classes=[IsAdminUser]
    


class Genreviewset(ModelViewSet):
    queryset=Genre.objects.all()
    serializer_class= GenreSerializer
    permission_classes=[IsAdminUser]



class AdminReviewViewset(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset=Review.objects.all()
    serializer_class=Reviewserializer
    permission_classes=[IsAdminUser]
    filter_backends=[DjangoFilterBackend,OrderingFilter]
    filterset_fields=['Movie']
    pagination_class=Mypagination

    def perform_destroy(self, instance):
        reports = Reportreview.objects.filter(reported_review=instance)
        reports.update(status="action_taken")
        instance.delete()


class Reports(ListModelMixin, RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset=Reportreview.objects.all()
    serializer_class=Reportserializer
    permission_classes=[IsAdminUser]
    filter_backends=[DjangoFilterBackend,OrderingFilter]
    filterset_fields=["reported_review",'status']
    ordering_fields=['created_at']