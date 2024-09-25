from django.db.models.signals import post_save
from django.dispatch import receiver

from transactions.models import SavingMoney , Transaction
from accounts.models import User

from .modules import adjust_money

@receiver(post_save , sender = User)
def create_saving(sender , *args , **kwargs):
    if kwargs['created']:
        SavingMoney.objects.create(
            user = kwargs['instance'],
        )

@receiver(post_save, sender=Transaction)
def update_saving(sender, **kwargs):
    if kwargs['created']:
        transaction = kwargs['instance']
        adjust_money(transaction.user , transaction)