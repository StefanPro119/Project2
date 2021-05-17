from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class Category(models.Model):
#     name = models.CharField(max_length=60)
#
#     def __str__(self):
#         return f"{self.name}"

#klasa za prodavanje proizvoda
class Auction(models.Model):
    seller = models.CharField(max_length=64)
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=120)
    start_bit = models.IntegerField()
    image = models.ImageField()
    data = models.DateTimeField(auto_now=True)
    # select_category =

    def __str__(self):
        return f"{self.seller} is selling {self.title}"


#klasa za licitiranje proizvoda
class Bid(models.Model):
    buyer = models.CharField(max_length=64)
    bid_value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer} is offering {self.bid_value}"

#klasa za komentarisanje proizvoda
class Comment(models.Model):
    commments = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commments}"