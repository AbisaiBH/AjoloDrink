from django.contrib.auth.models import User
from django.db import models
import uuid

class Cocktail(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image = models.URLField()
    name = models.CharField(max_length=120)
    description = models.JSONField()
    SEASON_CHOICES = (
        (0, 'All Seasons'),
        (1, 'Spring'),
        (2, 'Summer'),
        (3, 'Fall'),
        (4, 'Winter')
    )
    ALCOHOL_CHOICES = (
        (1, 'LOW'),
        (2, 'MID'),
        (3, 'HIGH')
    )
    season = models.IntegerField(choices=SEASON_CHOICES)
    alcohol_lvl = models.IntegerField(choices=ALCOHOL_CHOICES)
    tags = models.JSONField()
    liquor = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name

class Cocktail_detail(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    images = models.JSONField()
    name = models.CharField(max_length=120)
    description = models.JSONField()
    ingredients = models.JSONField()
    instructions = models.JSONField()
    
class RelevationCocktails():
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    favs = models.IntegerField(default=0)

class Profile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorites =  models.JSONField()

class ProfileReviews(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    REVIEW_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    calification = models.IntegerField(choices=REVIEW_CHOICES)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
