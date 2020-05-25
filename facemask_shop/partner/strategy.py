from decimal import Decimal as D

from oscar.apps.partner import strategy


class Selector(strategy.Selector):
    def strategy(self, request=None, user=None, **kwargs):
        return Belgium(request)


class Belgium(strategy.UseFirstStockRecord, strategy.StockRequired, strategy.FixedRateTax, strategy.Structured):
    rate = D('0.06')

