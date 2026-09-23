
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Movieviewset,Castviewset, Actorviewset,Genreviewset,AdminReviewViewset,Reports



router= DefaultRouter()
router.register('Movieview', Movieviewset, basename='Movieview')
router.register('Castview',Castviewset,basename='Castview')
router.register('Actorview',Actorviewset,basename='Actorview')
router.register('Genreview',Genreviewset,basename='Genreview')
router.register('Adminreview',AdminReviewViewset, basename='Adminreview')
router.register('report',Reports)


urlpatterns = [
    path('', include(router.urls)),
    path('',include('rest_framework.urls')),
]
