from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Publicmovieviewset, Reviewviewset,Castviewset,Watchlistviewset,Reportviewset
router= DefaultRouter()

router.register('Movie', Publicmovieviewset, basename='Movie')



urlpatterns=[
    path('',include(router.urls)),
    path('Movie/<int:movie_pk>/reviews/',Reviewviewset.as_view({'get':'list','post':'create'})),
    path('Movie/<int:pk>/cast/',Castviewset.as_view({'get':'list'})),
    path('Movie/<int:movie_pk>/Watchlist/',Watchlistviewset.as_view({'post':'create'})),
    path('reviews/<int:review_pk>/report/',Reportviewset.as_view({'post':'create'})),
]