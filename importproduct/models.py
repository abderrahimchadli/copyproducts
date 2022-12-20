from django.db import models

# Create your models here.
# auth_demo/auth_app/models.py
from shopify_auth.models import AbstractShopUser

class AuthAppShopUser(AbstractShopUser):
    pass


class Billing(models.Model):
    user=models.IntegerField()
    charge_id=models.TextField(max_length=200,null=True,unique=True)
    createdAt=models.DateTimeField()
    currentPeriodEnd=models.DateTimeField(null=True)
