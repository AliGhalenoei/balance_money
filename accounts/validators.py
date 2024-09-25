from django.core.exceptions import ValidationError

def validate_phone(value):
    if not value.startswith('09'):
        raise ValidationError('Number phone invalid!!!')
    return value

def validate_len_phone(value):
    if len(value) != 11:
        raise ValidationError('The phone number must be 11 digits long.')
    
