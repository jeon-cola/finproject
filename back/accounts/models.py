# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from fin.models import SavingModel,DepositModel
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30,unique=True,null= True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    asset = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    saving = models.ManyToManyField(SavingModel,null=True)
    deposit = models.ManyToManyField(DepositModel,null=True)

    def __str__(self):
        return self.username
    
