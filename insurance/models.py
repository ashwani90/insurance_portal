from django.db import models
from datetime import datetime

# Create your models here.
class Insurance(models.Model):
    # Model fields
    policy_id = models.IntegerField()
    purchase_date = models.DateTimeField(default=datetime.now, blank=True)
    customer_id = models.IntegerField()
    fuel = models.CharField(max_length=10)
    vehicle_segment = models.CharField(max_length=5)
    premium_amount = models.IntegerField()
    bodily_injury_liability = models.BooleanField(default=False)
    personal_injury_protection = models.BooleanField(default=False)
    property_damage_liability = models.BooleanField(default=False)
    collision = models.BooleanField(default=False)
    comprehensive = models.BooleanField(default=False)
    customer_gender = models.BooleanField(default=False)
    income_group = models.CharField(max_length=20)
    customer_region = models.CharField(max_length=10)
    maritial_status = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the model class
        """
        return self.customer_region + "-" + str(self.policy_id) + "-" + str(self.customer_id)