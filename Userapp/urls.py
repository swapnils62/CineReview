from rest_framework.routers import DefaultRouter
from .views import Userprofile,UserReview,Watchlistviewset,Reports
from django.urls import path,include



router=DefaultRouter()

router.register('review',UserReview, basename='review')
router.register('watchlist',Watchlistviewset, basename='watchlist')
router.register('reports',Reports, basename='reports')


urlpatterns=[
    path('',include(router.urls)),
    path('profile/',Userprofile.as_view()),
]