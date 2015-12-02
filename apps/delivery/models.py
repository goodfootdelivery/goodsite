from django.db import models
from django.contrib.auth.models import User

# All Models Related to the Delivery Logic


class Order(models.Model):
    STAT_CHOICES = (
        ('RE', 'Recieved'),
        ('AS', 'Assigned'),
        ('TR', 'In Transit'),
        ('DE', 'Delivered'),
        ('PD', 'Paid'))

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, blank=False, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STAT_CHOICES, default='RE')
    courier = models.ForeignKey(User,
                limit_choices_to={'groups__name': 'Couriers'}, related_name='courier')
    price = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return "Order: %s, \tUserID: %s, \tDate: %s, \tStatus: %s" \
            % (str(self.order_id), str(self.user_id), str(self.date),
                str(self.status))


class OrderMeta(models.Model):
    pass
