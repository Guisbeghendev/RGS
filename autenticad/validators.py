# autenticad/validators.py
import re
from django.core.exceptions import ValidationError

def validate_whatsapp(value):
    pattern = r'^\+?\d{0,2}\s?\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    if not re.match(pattern, value):
        raise ValidationError('Número de WhatsApp inválido. Use o formato: +55 11 91234-5678 ou 11912345678.')
