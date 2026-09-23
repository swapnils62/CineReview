from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
from Adminapp.models import Movie



class OTP(models.Model):
    code=models.CharField(max_length=128)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    attempts=models.IntegerField(default=0)
    used=models.BooleanField(default=False)

    def is_valid(self):
        return (not self.used 
                and timezone.now() < self.created_at+timedelta(minutes=10)
                and self.attempts < 5

                )


class Watchlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
