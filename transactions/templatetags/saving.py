from django import template
from transactions.models import SavingMoney

register = template.Library()

@register.simple_tag
def user_money(user_id):
    money_amount = SavingMoney.objects.get(user=user_id).money
    formatted_money = f"{money_amount:,}"
    return formatted_money

     