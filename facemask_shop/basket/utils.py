from oscar.apps.basket.utils import BasketMessageGenerator as OscarBasketMessageGenerator


class BasketMessageGenerator(OscarBasketMessageGenerator):
    def get_new_total_messages(self, basket, include_buttons=True):
        # Disable new total messages, the basket is always displayed on the product page
        return []
