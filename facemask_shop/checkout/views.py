import logging

from django.urls import reverse
from django.utils import six

from oscar.apps.checkout import views as oscar_views
from oscar.apps.checkout import exceptions
from oscar.apps.payment.models import Source
from oscar.apps.payment.exceptions import RedirectRequired

from mollie_oscar.facade import Facade

from facemask_shop.checkout.forms import TermsAndConditionsForm

logger = logging.getLogger('oscar.checkout')


class PaymentDetailsView(oscar_views.PaymentDetailsView):
    template_name = 'checkout/payment_details.html'
    template_name_preview = 'checkout/preview.html'

    def get_skip_conditions(self, request):
        skip_conditions = super().get_skip_conditions(request)
        if not self.preview:
            skip_conditions += ['skip_no_payment_options']
        return skip_conditions

    def skip_no_payment_options(self, request):
        raise exceptions.PassedSkipCondition(
            url=reverse('checkout:preview')
        )

    def get_context_data(self, **kwargs):
        kwargs.setdefault('tc_form', TermsAndConditionsForm())
        return super().get_context_data(**kwargs)

    def handle_place_order_submission(self, request):
        tc_form = TermsAndConditionsForm(request.POST)
        if not tc_form.is_valid():
            return self.render_preview(request, tc_form=tc_form)
        submission_data = self.build_submission()
        submission_data['payment_kwargs']['submission'] = submission_data
        return self.submit(**submission_data)

    def handle_payment(self, order_number, total, **kwargs):
        submission = kwargs['submission']

        # Create new Mollie Payment!
        facade = Facade()
        payment_id = facade.create_payment(order_number=order_number,
                                           total=total.incl_tax,
                                           currency=total.currency,
                                           redirect_url=self.get_success_url())

        # Register the Oscar Source(Type)
        source = Source(
            source_type=facade.get_source_type(),
            amount_allocated=total.incl_tax,
            currency=total.currency,
            reference=payment_id
        )
        self.add_payment_source(source)

        # Record Payment event and create the Order(!)
        self.add_payment_event('pre-auth', total.incl_tax)
        self._save_order(order_number, submission)

        # Redirect to Mollie Payment Page
        url = facade.get_payment_url(payment_id)
        raise RedirectRequired(url)

    def _save_order(self, order_number, submission):
        # Oscar by default doesn't create an order after a RedirectRequired raise.
        # Overrule this by creating an Order before raising using this copy-pasted method
        # from the Oscar package.
        logger.info(u"Order #%s: payment started, placing order", order_number)
        try:
            return self.handle_order_placement(
                order_number, submission['user'],
                submission['basket'],
                submission['shipping_address'],
                submission['shipping_method'],
                submission['shipping_charge'],
                submission['billing_address'],
                submission['order_total'],
                **(submission['order_kwargs'])
            )
        except oscar_views.UnableToPlaceOrder as e:
            logger.error(u"Order #%s: unable to place order - %s", order_number, e, exc_info=True)
            msg = six.text_type(e)
            self.restore_frozen_basket()
            return self.render_to_response(self.get_context_data(error=msg))

    def send_confirmation_message(self, order, code, **kwargs):
        # Don't send the confirmation message before we know the Order is paid for.
        pass


class ThankYouView(oscar_views.ThankYouView):
    template_name = 'checkout/thank_you.html'
