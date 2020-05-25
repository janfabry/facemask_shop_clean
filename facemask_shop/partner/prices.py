from oscar.apps.partner import prices


class TaxInclusiveBasedFixedPrice(prices.Base):
    exists = True
    is_tax_known = True

    def __init__(self, currency, excl_tax, incl_tax, tax):
        self.currency = currency
        self.excl_tax = excl_tax
        self.incl_tax = incl_tax
        self.tax = tax

    @property
    def effective_price(self):
        return self.incl_tax
