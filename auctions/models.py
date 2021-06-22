from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField

STATUS = [
    ('active','active'),
    ('sold','sold'),
]

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"

#klasa za prodavanje proizvoda
class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=1200)
    start_bit = models.IntegerField()
    image = ResizedImageField(size=[500, 500], quality=100, null=True, blank=True, upload_to="images/")
    data = models.DateTimeField(auto_now=True)
    select_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories', default=None)
    status = models.CharField(max_length=7, choices=STATUS, default='active')

    def __str__(self):
        return f"{self.seller} is selling {self.title}"


#klasa za licitiranje proizvoda
class Bid(models.Model):
    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='customer')
    bid_value = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer} is offering {self.bid_value}"

#klasa za komentarisanje proizvoda
class Comment(models.Model):
    commments = models.TextField()
    comment_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='user_comment')
    commment_auctions = models.ForeignKey(Auction, blank=True, null=True, on_delete=models.CASCADE, related_name='auctions_comment')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.commments}"

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_idd')
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction_idd')

    def __str__(self):
        return f"{self.user_id}, {self.auction_id}"
