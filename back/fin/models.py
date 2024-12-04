from django.db import models
from django.conf import settings
# Create your models here.
class DepositModel(models.Model):
    kor_co_nm=models.TextField()
    fin_prdt_nm=models.TextField()
    join_way=models.TextField()
    mtrt_int=models.TextField()
    spcl_cnd=models.TextField()
    etc_note=models.TextField()
    intr_rate=models.IntegerField(null=True)
    intr_rate2=models.IntegerField(null=True)
    intr_rate_type_nm=models.TextField()
    save_trm=models.TextField()

class SavingModel(models.Model):
    kor_co_nm=models.TextField()
    fin_prdt_nm=models.TextField()
    join_way=models.TextField(null=True)
    mtrt_int=models.TextField()
    spcl_cnd=models.TextField()
    etc_note=models.TextField()
    intr_rate=models.IntegerField(null=True)
    intr_rate2=models.IntegerField(null=True)
    intr_rate_type_nm=models.TextField()
    save_trm=models.TextField()
    rsrv_type_nm = models.TextField()
