from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Review(models.Model):
    RATING_CHOICES =[
        (1,'1 Star'),
        (2,'2 Star'),
        (3,'3 Star'),
        (4,'4 Star'),
        (5, '5 Star')
        ]
    Title=models.CharField(max_length=100 ,null=False)
    Review=models.TextField(max_length=400, null=False)
    Rating=models.IntegerField(choices=RATING_CHOICES)
    Created_at=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    Movie=models.ForeignKey('Adminapp.Movie',on_delete=models.CASCADE,related_name='review')

    class Meta:
        unique_together = ('user', 'Movie')



class Reportreview(models.Model):
    Reasonchoice=[
        ('spam', 'Spam'),
        ('offensive', 'Offensive Language'),
        ('spoiler', 'Spoilers'),
    ]
    statuschoice=[
        ('pending','pendign'),
        ('dismissed',"dismissed"),
        ('action_taken',"action_taken")
    ]

    reason=models.TextField()
    reasoncategorie=models.CharField(max_length=20,choices=Reasonchoice)
    reported_review=models.ForeignKey(Review,on_delete=models.SET_NULL,null=True,blank=True,related_name='report')
    report_user =models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(choices=statuschoice,default='pending')
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        unique_together =['reported_review','report_user']