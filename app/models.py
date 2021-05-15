from django.db import models
from user.models import Profile


#model for insurence offered
class Insurance(models.Model):
    name = models.TextField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()
    maxRepayment = models.IntegerField(default= 0)
    duration = models.IntegerField(default= 365)

    def __str__(self):
        return self.name
#model for policies purchased
class Policy(models.Model):
    insured = models.ForeignKey(Profile, on_delete= models.CASCADE)
    policy = models.ForeignKey(Insurance, on_delete= models.CASCADE)
    date = models.DateTimeField(auto_now_add=True )
    active = models.BooleanField(default=True)
    expiration = models.DateTimeField(auto_now_add=True)