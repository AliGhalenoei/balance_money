from .models import Transaction , SavingMoney


def filter_transaction(trans_type):
    transactions = Transaction.objects.filter(transaction_type=trans_type)
    return transactions

def get_from_object(cls,cls_id):
    transaction = cls.objects.get(id=cls_id)
    return transaction

def adjust_money(user , transaction):
    money_user = SavingMoney.objects.get(user=user)
    if transaction.transaction_type == 'income':
        money_user.money += transaction.transaction
        
    elif transaction.transaction_type == 'cost':
        money_user.money= max(0,money_user.money - transaction.transaction)  

    money_user.save()

def delete_or_trans(user , transaction):
    money_user = SavingMoney.objects.get(user=user)

    if transaction.transaction_type == 'income':
        money_user.money = money_user.money - transaction.transaction

    elif transaction.transaction_type == 'cost':
        money_user.money += transaction.transaction

    money_user.save()
    
