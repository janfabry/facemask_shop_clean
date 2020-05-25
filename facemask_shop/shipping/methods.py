from decimal import Decimal as D

from oscar.apps.shipping.methods import FixedPrice


class Standard(FixedPrice):
    charge_excl_tax = D('5.00')
    charge_incl_tax = D('5.00')
