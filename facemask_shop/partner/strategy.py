from decimal import Decimal as D

from oscar.apps.partner import strategy

from facemask_shop.partner.prices import TaxInclusiveBasedFixedPrice


class Selector(strategy.Selector):
    def strategy(self, request=None, user=None, **kwargs):
        return Belgium(request)


class Belgium(strategy.UseFirstStockRecord, strategy.StockRequired, strategy.FixedRateTax, strategy.Structured):
    rate = D('0.06')

    def pricing_policy(self, product, stockrecord):
        if not stockrecord or stockrecord.price_excl_tax is None:
            return strategy.UnavailablePrice()
        rate = self.get_rate(product, stockrecord)
        exponent = self.get_exponent(stockrecord)
        tax = (stockrecord.price_excl_tax * rate).quantize(exponent)
        return TaxInclusiveBasedFixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            incl_tax=stockrecord.price_retail,
            tax=tax)
