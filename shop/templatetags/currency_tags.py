from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def format_cop(value):
	"""Formatea un Decimal/numero al estilo '1.234.567,89'.

	- Convierte a Decimal, aplica 2 decimales y usa punto como separador de miles
	  y coma como separador decimal (formato colombiano/español visual).
	"""
	try:
		d = Decimal(value)
	except (InvalidOperation, TypeError, ValueError):
		return value

	sign = '-' if d < 0 else ''
	d = abs(d).quantize(Decimal('0.01'))
	s = f"{d:.2f}"  # p.ej. '1234567.89'
	int_part, dec_part = s.split('.')
	int_str = f"{int(int_part):,}".replace(',', '.')
	if dec_part == '00':
		return f"{sign}{int_str}"
	return f"{sign}{int_str},{dec_part}"
