
from rest_framework.views import APIView
from .serializer import Signupserializer,Userserializer,Watchlistserailizer,Resportserializr
import random
from .models import OTP, Watchlist
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
# Create your views here.
from django.contrib.auth.hashers import check_password, make_password


from Reviewapp.serializer import Reviewserializer
from Reviewapp.models import Review,Reportreview

from .pagination import Mypagination


from Adminapp.models import Movie


class Signupviwe(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer=Signupserializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            otp=random.randint(100000,999999)
            OTP.objects.create(user=user,code=make_password(otp))

            send_mail(
                subject='Verify your CineReview account',
                message=f'Your OTP is {otp}. It expires in 10 minutes.',
                from_email='noreply@cinereview.com',
                recipient_list=[user.email],
            )
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Otpverify(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        email=request.data.get('email')
        code=request.data.get('code')

        if not email or not code:
            return Response(
                {"error": "Email and OTP code are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."},
                            status=status.HTTP_400_BAD_REQUEST)
        otp=OTP.objects.filter(user=user).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        otp.attempts+=1
        otp.save(update_fields=['attempts'])

        if not check_password(str(code),otp.code):
            return Response({'error': 'Invalid or expired OTP.'}, status=400)


        user.is_active=True
        otp.used=True
        otp.save()
        user.save()
        return Response({'message': 'Account verified. You can now log in.'}, status=status.HTTP_200_OK)



class Userprofile(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer=Userserializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer=Userserializer(request.user, data= request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserReview(ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin, GenericViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Reviewserializer
    pagination_class=Mypagination

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by("-Created_at")


class Watchlistviewset(ListModelMixin,DestroyModelMixin,GenericViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Watchlistserailizer
    pagination_class=Mypagination

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user).order_by('-created_at')
    


class Reports(ListModelMixin, GenericViewSet):
    serializer_class=Resportserializr
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Reportreview.objects.filter(report_user=self.request.user)
    