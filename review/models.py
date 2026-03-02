from django.db import models
from users.models import User
from product.models import Product

class Review(models.Model):

    STATUS = {
        "HAQORATLI": "haqoratli",
        "YOLG'ON": "yolg'on",
        "WAITING": "waiting",
        "ACTIVE": "active"
    }


    rating = models.IntegerField()
    comment = models.TextField()
    status = models.CharField(choices=STATUS, max_length=20, default=STATUS["WAITING"])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="user_comment_image/", null=True, blank=True)

    def __str__(self):
        return f"{self.user} 's review"
