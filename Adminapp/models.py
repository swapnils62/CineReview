from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    Name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.Name

class Movie(models.Model):
    Title=models.CharField(max_length=100, null=False)
    Synopsis=models.TextField(null=False)
    Runtime=models.IntegerField()
    Poster=models.ImageField(null=True, blank=True)
    Released_date=models.DateField(null=False)
    Director=models.CharField(max_length=100,null=False)
    Genre_name=models.ManyToManyField(Genre,related_name='movies')

    def __str__(self):
        return self.Title

class Actor(models.Model):
    Name=models.CharField(max_length=100)
    Info=models.TextField()

    def __str__(self):
        return self.Name

class Cast(models.Model):
    Actor_name=models.ForeignKey(Actor, on_delete=models.CASCADE)
    Movie_name=models.ForeignKey(Movie, on_delete=models.CASCADE)
    Character=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.Actor_name.Name} as {self.Character} in {self.Movie_name.Title}"

    class Meta:
            unique_together = ('Actor_name', 'Movie_name')
    

